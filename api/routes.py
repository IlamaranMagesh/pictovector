from flask import request, Blueprint
from uuid import uuid4
from pathlib import Path
from urllib.parse import urlparse
from vercel.blob import list_objects, put

from .constants import COLLECTION
from .clients import genai_client, qdb_client
from .qdb import Image, Qdb
from .llm import LLM

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/images/upload', methods=['POST'])
def upload():
    """
    Images upload route handler.
    Multiform is not implemented.
    Takes the first file, if multiple files are sent.
    """
    file = request.files['file']
    extension = '.bin' if Path(file.filename).suffix == '' else Path(file.filename).suffix
    id = uuid4().__str__()
    filepath = f"images/{id}{extension}"
    file_data = file.read()

    db = Qdb(qdb_client)
    model = LLM(genai_client)

    try:
        response = put(
            path=filepath,
            body=file_data,
            access="public",
        ) # Caution: Assuming only one image is uploaded.

        image = Image(image_bytes=file_data, url=response.url, id=id)
        db.upload(model, [image])

        return {"id":id, "filename": f"{id}{extension}", "url": response.url,
                "tags": db.payloads[0]["tags"]}

    except Exception as msg:
        print(msg)
        return f"{msg}", 500


@bp.route('/images', methods=['GET'])
def getall_images():
    """
    Returns the first 1000 images stored in the vercel blob.
    """
    blobresult = list_objects(limit= 1000) # Caution: Sends only the first 1000 images
    data: list[dict] = []

    for item in blobresult.blobs:
        path = Path(item.pathname)

        if path.suffix:
            id = path.stem
            records = qdb_client.retrieve(
                collection_name=COLLECTION,
                ids=[id],
                with_payload=True,
                with_vectors=False,
            )
            if records:
                data.append(
                    {
                        "id": id,
                        "filename": path.name,
                        "url":item.url,
                        "tags":records[0].payload['tags'],
                    }
                )
    data_dict = {"images": data}
    return data_dict


@bp.route('/search', methods=['GET'])
def search():
    """
    Text query search handler.
    Images are retrieved by similarity between the description of images stored and the query.
    """
    db = Qdb(qdb_client)
    model = LLM(genai_client)
    query = request.args.get('query')
    results = db.query_by_text(model, query)

    data: list[dict] = []
    for result in results:
        payload = result['payload']
        score = result['confidence']
        path = Path(urlparse(payload['url']).path)
        if path.suffix:
            data.append(
                {
                    "id": payload['uuid'],
                    "filename": path.name,
                    "url": payload['url'],
                    "confidence": score,
                    "tags":payload['tags'],
                }
            )

    data_dict = {"images": data}
    return data_dict

@bp.route("/tags", methods=['GET'])
def get_tags():
    """
    Returns the first 100 unique tags stored.
    """
    points, offset = qdb_client.scroll(
        collection_name=COLLECTION,
        limit=100,
        with_payload=True,
        with_vectors=False,
    )
    tags = list({tag for point in points for tag in point.payload['tags']})

    return tags

@bp.route("/images/<string:img_id>", methods=["DELETE"])
def delete_image():
    ...



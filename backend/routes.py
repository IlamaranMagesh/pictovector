from crypt import methods

from dotenv import load_dotenv
import requests
from qdrant_client import QdrantClient
from google.genai import Client
from flask import request, Blueprint, g, jsonify
import vercel_blob
from uuid import uuid4

from . import clients
from .qdb import Image, Qdb
from .llm import LLM

genai_client: Client | None = None
qdb_client: QdrantClient | None = None

#Load environment and client
def load_env():
    load_dotenv()
    global genai_client
    global qdb_client
    genai_client = clients.get_genai_client()
    qdb_client = clients.get_qdb_client()

def _wrap_image(urls: list[str]):
    images = [Image(requests.get(url).content, url) for url in urls]
    return images

load_env()
bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/images/upload', methods=['POST'])
def upload():
    file = request.files['file']
    id = uuid4().__str__()
    extension = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    filepath = f"images/{id}.{extension}"
    file_data = file.read()

    db = Qdb(qdb_client)
    model = LLM(genai_client)

    try:
        response = vercel_blob.put(filepath, file_data)  # assuming only one image is uploaded
        image = Image(image_bytes=file_data, url=response.get("url"), id=id)  # Todo: uuid should be added to Image
        #db.upload(model, [image])
        return jsonify({f"Images uploaded successfully. url: {response.get('url')}"}), 200
    except Exception as msg:
        return jsonify({f"{msg}"}), 500

@bp.route('/search', methods=['GET'])
def search():
    pass

if __name__ == '__main__':
    load_env()



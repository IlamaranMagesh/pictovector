"""
Instantiates the flask api application for vercel
"""
from api import create_app

if __name__ == '__main__':
    app = create_app()
# TODO(Project 1): Implement Backend according to the requirements.
# Imprts flask Response library
from flask import Response
# Imports the Google Cloud client library
from google.cloud import storage
# Instantiates a client
storage_client = storage.Client()
# Bucket names
content_wiki_name = "content-wiki"
# bucket instanttiation
content_wiki_bucket = storage_client.create_bucket(content_wiki_name)
"""
TODO delete these notes when no longer needed.
Sice the requirement is to just get an uploaded page from the bucket,
I think that means that we can just store the contents of the page and 
use jinja to display its contents.
"""
class Backend:

    def __init__(self):
        pass
        
    def get_wiki_page(self, name):
        return content_wiki_bucket.blob(name)

    def get_all_page_names(self):
        page_names = []
        blobs = storage_client.list_blobs(content_wiki_name)
        for blob in blobs: # TODO maybe add an if statement for filtering?
            page_names.append(blob.name)
        return page_names

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self, image_name): # TODO delete: I don't think it makes sense to not have a name parameter
        """Gets image from GCS and generates a response in order to be able to 
           display the image."""
        image_blob = content_wiki_bucket.blob(image_name)
        image = image_blob.download_as_bytes()
        # IDK if this is correct but:
        return Response(image, mimetype='image/jpeg')


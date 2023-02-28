# TODO(Project 1): Implement Backend according to the requirements.

# Imports flask Response library in order to dispay images.
from flask import Response
# Imports the Google Cloud client library
from google.cloud import storage
# Imports library for hashing the passwords
import hashlib

# Instantiates a client
storage_client = storage.Client()
# Bucket names
content_wiki_name = "content-wiki"
users_pswd_name = "password-users"
# bucket instanttiation
content_wiki_bucket = storage_client.bucket(content_wiki_name)
users_pswd_bucket = storage_client.bucket(users_pswd_name)
"""
TODO delete these notes when no longer needed.
Sice the requirement is to just get an uploaded page from the bucket,
I think that means that we can just store the contents of the page and 
use jinja to display its contents.
"""
# Password hashing
# hash = hashlib.blake2b("Your password".encode()).hexdigest()
secret = "Super Secret Key"
class Backend:

    def __init__(self, storage=storage_client):
        self.storage = storage
        
    def get_wiki_page(self, name):
        # TODO parse the file, this is probably going to be just text
        return self.storage.bucket("content-wiki").blob(name)

    def get_all_page_names(self):
        page_names = []
        blobs = storage_client.list_blobs(content_wiki_name)
        for blob in blobs: # TODO maybe add an if statement for filtering?
            page_names.append(blob.name)
        return page_names

    def upload(self):
        pass

    def sign_up(self):
        # TODO 2 possibilities: take the values from a sign up page or make
        # this the fuction that handles the sign up page and then redirects
        # to another page like the main page or something
        username = "dummy"
        password = "dummy"
        hash = hashlib.blake2b(f"{username}{password}{secret}".encode()).hexdigest()

    def sign_in(self):
        # TODO this will need the flask login class and tools
        username = "dummy"
        password = "dummy"
        hash = hashlib.blake2b(f"{username}{password}{secret}".encode()).hexdigest()

    def get_image(self, image_name): # TODO delete: I don't think it makes sense to not have a name parameter
        """Gets image from GCS and generates a response in order to be able to 
           display the image."""
        # Image name has to be complete: "james.jpg"
        image_blob = self.storage.bucket("content-wiki").blob(f"images/{image_name}")
        image = image_blob.download_as_bytes()
        # Apparently eliminating this does not cause problems
        # if image_name.endswith('.jpg') or image_name.endswith('.jpeg'):
        #     mimetype = 'image/jpeg'
        # elif image_name.endswith('.png'):
        #     mimetype = 'image/png'
        # else:
        #     mimetype = 'image/jpg'
        return Response(image) # , mimetype=mimetype


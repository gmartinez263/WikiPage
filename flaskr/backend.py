# Imports flask Response library in order to dispay images.
from flask import Response
# Imports the Google Cloud client library
from google.cloud import storage
# Imports library for hashing the passwords
import hashlib
# Importing User class and methods
from user_module import User

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
# TODO maybe use flask's secret for hashing?
secret = "Super Secret Key"


class Backend:

    def __init__(self, storage=storage_client,user_m=User):
        self.storage = storage
        self.user_m = user_m    
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

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
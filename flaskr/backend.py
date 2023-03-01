# TODO(Project 1): Implement Backend according to the requirements.

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
        # TODO parse the file, this is probably going to be just text
        return self.storage.bucket("content-wiki").blob(f"pages/{name}")

    def get_all_page_names(self):
        page_names = []
        blobs = storage_client.list_blobs(content_wiki_name, delimiter="pages")
        for blob in blobs: # TODO maybe add an if statement for filtering?
            page_names.append(blob.name)
        return page_names

    def upload(self): # TODO for now I think the users will just upload text
        self.storage.bucket.blob()

    def sign_up(self, usrname, pswd):
        usr = self.user_m.get_user_from_usrname(self.storage, usrname)
        hashed_password = hashlib.blake2b(f"{usrname}{pswd}{secret}".encode()).hexdigest()
        if usr:
            return None
        blob = self.storage.bucket("content-wiki").blob("usrname")
        with blob.open("w") as b:
            b.write(hashed_password)
        return self.user_m(usrname, hashed_password)

    def sign_in(self, usrname, pswd):
        usr = self.user_m.get_user_from_usrname(self.storage, usrname)
        hashed_password = hashlib.blake2b(f"{usrname}{pswd}{secret}".encode()).hexdigest()
        if usr:
            if usr.pswd == hashed_password:
                return usr
        return 

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

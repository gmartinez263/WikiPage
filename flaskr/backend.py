# TODO(Project 1): Implement Backend according to the requirements.

# Imports the Google Cloud client library
from google.cloud import storage
# Imports library for hashing the passwords
import hashlib
# Importing User class and methods
from user import User

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

class Backend:
    def __init__(self, storage=storage_client, user_m=User):
        self.storage = storage
        self.user_m = user_m
        
    def get_wiki_page(self, name): # TODO
        # TODO parse the file, this is probably going to be just text
        blob = self.storage.bucket(content_wiki_name).blob(f"pages/{name}")
        page = list()
        with blob.open() as page_blob:
            page = page_blob.readlines()
        return page

    def get_user(self, usrname):
        usr = self.user_m.get_user_from_usrname(self.storage, usrname)
        return usr

    def get_all_page_names(self):
        page_names = list()
        blobs = storage_client.list_blobs(content_wiki_name)
        for blob in blobs:
            if(len(blob.name)!=6 and blob.name.startswith("pages/")):
                page_names.append(blob.name)
        return page_names

    def upload(self, folder, fname,file):
        # for now we will use images and pages as folders
        blob = self.storage.bucket(content_wiki_name).blob(f"{folder}/{fname}")
        blob.upload_from_file(file)
        return True

    """
    Notes on signup and sign in:
    They return a user data class instance on success.
    """
    def hash_password(self, usrname, pswd):
        # TODO maybe use flask's secret for hashing?
        secret_key = "Team404 super secret key!"
        return hashlib.blake2b(f"{usrname}{pswd}{secret_key}".encode()).hexdigest()

    def sign_up(self, usrname, pswd):
        """ 2 Possible returns
            returns None if the user name exists, since we can't have 2 of the same usernames.
            returns a user objet if the signup was successful.
        """
        usr = self.user_m.get_user_from_usrname(self.storage, usrname)
        hashed_password = self.hash_password(usrname, pswd)
        if usr: 
            return None
        blob = self.storage.bucket(users_pswd_name).blob(usrname)
        with blob.open("w") as b: # Store user in our storage solution
            b.write(hashed_password)
        return self.user_m(usrname, hashed_password)

    def sign_in(self, usrname, pswd):
        """ 2 Possible returns
            returns a user object if the sign in was succesful.
            returns None if the signup failed.
        """
        usr = self.user_m.get_user_from_usrname(self.storage, usrname)
        hashed_password = self.hash_password(usrname, pswd)
        if usr:
            if usr.pswd == hashed_password:
                return usr
        return None

    def get_image(self, image_name):
        """Gets image from GCS and generates a response in order to be able to 
           display the image."""
        # Image name has to be complete: "james.jpg"
        image_blob = self.storage.bucket(content_wiki_name).blob(f"images/{image_name}")
        image = image_blob.download_as_bytes()
        return image
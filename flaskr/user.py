from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id, pswd):
        self.id = id
        self.pswd = pswd
    @staticmethod
    def get_user_from_usrname(storage_client, username):
        blobs = storage_client.list_blobs("password-users")
        for blob in blobs:
            if blob.name == username:
                with b.open() as b:
                    password = blob.read()
                return User(username, password)
        return 
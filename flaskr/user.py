from flask_login import UserMixin
# TODO DELETE: this is a data class
class User(UserMixin):
    def __init__(self, id, pswd):
        self.id = id
        self.pswd = pswd
        
    @staticmethod
    def get_user_from_usrname(storage_client, username):
        blobs = storage_client.list_blobs("password-users")
        for blob in blobs:
            if blob.name == username:
                with blob.open() as b:
                    password = b.read()
                return User(username, password)
        return 
from flask import render_template, redirect, request, flash
from flask_login import login_required, logout_user, login_user, login_manager, current_user
from backend import Backend
from user import User
from flask_login import LoginManager
login_manager = LoginManager()

def make_endpoints(app):
    login_manager.init_app(app)
    backend = Backend()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/pages")
    def pages():
        return render_template("pages.html")

    @app.route("/about") # TODO make sure this does not break when get author images is changed to make requirements
    def about():
        return render_template("about.html", authors = ["James", "Ale", "Geovanny"])

    """
    You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session.
    It should take the str ID of a user, and return the corresponding user object. For example:
    """
    # Docstrings need to be properly indented

    @login_manager.user_loader
    def load_user(user_id): # TODO
        return User.get(user_id) # TODO, i don't know if this must be changed yet.

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            uname = request.form.get("Usrname") 
            pswd = request.form.get("Password") 
            usr = backend.sign_in(uname, pswd)
            login_user(usr)
            if usr: 
                flash('Logged in successfully.')
                redirect("/")                
            if not usr:
                flash('Logged failed!')
        return render_template('login.html')

    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        return render_template("signup.html")
  
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route("/images/<img_name>")
    def get_author_images(img_name): # TODO this must be changed to use the functions in Backend class
        from google.cloud import storage
        from flask import Response
        
        # Instantiates a client
        storage_client = storage.Client()
        # Bucket names
        content_wiki_name = "content-wiki"
        # bucket instanttiation
        content_wiki_bucket = storage_client.bucket(content_wiki_name)
        # Hopefully getting the image
        image_blob = content_wiki_bucket.blob(f"images/{img_name}")
        image = image_blob.download_as_bytes()
        return Response(image)
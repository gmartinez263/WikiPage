from flask import render_template, redirect, flask 
from flask_login import login_required, logout_user, login_user, login_manager, current_user
from user import User

def make_endpoints(app):

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/pages")
    def pages():
        return render_template("pages.html")

    @app.route("/about")
    def about():
        return render_template("about.html", authors = ["James", "Ale", "Geovanny"])

    @app.route("/login", methods = ["POST", "GET"])
    def login():
        return render_template("login.html")

    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        return render_template("signup.html")
  
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(somewhere)

    @app.route("/images/<img_name>")
    def get_author_images(img_name):
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
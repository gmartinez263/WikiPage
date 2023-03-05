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

    @app.route("/about") # TODO make sure this does not break when get author images is changed to make requirements
    def about():
        return render_template("about.html", authors = ["James", "Ale", "Geovanny"])

"""
You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session.
 It should take the str ID of a user, and return the corresponding user object. For example:
"""
    @login_manager.user_loader
    def load_user(user_id): # TODO
        return User.get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        form = LoginForm()
        if form.validate_on_submit():
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        return flask.render_template('login.html', form=form)

    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        return render_template("signup.html")
  
    @app.route("/logout")
    @login_required
    def logout(): # TODO This should redirect to the main page or to the login page
        logout_user()
        return redirect(somewhere)

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
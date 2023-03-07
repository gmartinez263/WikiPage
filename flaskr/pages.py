from flask import render_template, redirect, request, flash, Response
from flask_login import login_required, logout_user, login_user, login_manager, current_user
from backend import Backend

from flask_login import LoginManager
login_manager = LoginManager()

def make_endpoints(app):
    login_manager.init_app(app)
    hood = Backend()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/pages")
    def pages(): # TODO """Implement parameterized routes for pages the user uploads, displaying text associated with the page from the GCS content bucket (route: /pages/, 3 pt.s)."""
        return render_template("pages.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @login_manager.user_loader
    def load_user(user_id): # TODO
        usr = hood.get_user(user_id)
        return usr

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            uname = request.form.get("Usrname") 
            pswd = request.form.get("Password") 
            usr = hood.sign_in(uname, pswd)
            if usr: 
                login_user(usr)
                flash('Logged in successfully.')
                return redirect("/")                
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
    def get_image(img_name): 
        img = hood.get_image(img_name)
        return Response(img)
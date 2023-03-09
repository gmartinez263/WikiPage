from flask import render_template, redirect, request, flash, Response, session, make_response
from flask_login import login_required, logout_user, login_user, login_manager, current_user
from backend import Backend

from flask_login import LoginManager
login_manager = LoginManager()

def make_endpoints(app):
    login_manager.init_app(app)
    hood = Backend()

    @app.route("/")
    def home():
        session.pop('_flashes', None)
        response = make_response(render_template("home.html"))
        response.status_code = 200
        return response

    @app.route("/pages")
    def pages():
        session.pop('_flashes', None)
        pgs = hood.get_all_page_names()
        return render_template("pages.html", pgs = pgs)
    
    @app.route("/pages/<page_name>")
    def page(page_name):
        pg = hood.get_wiki_page(page_name)
        return render_template("page.html",page_contents = pg )

    @app.route("/about")
    def about():
        session.pop('_flashes', None)
        return render_template("about.html")

    @login_required
    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        session.pop('_flashes', None)
        # My attempt
        if request.method == "POST":
            if 'file' not in request.files:
                flash("No file part!")
                return render_template("upload.html")
            file = request.files['file']
            if file.filename == '':
                flash("No file selected!")
                return render_template("upload.html")
            # There actually is a file
            name = ''
            if request.form.get("filename"): # If the user renamed the file
                name = request.form.get("filename")
            else: 
                name = file.filename
            if hood.upload("pages", name, file): # If the upload was succesful
                flash("File was uploaded succesfully!")
        return render_template("upload.html")            
        # # My attempt
        # if request.method == 'POST':
        # # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # If the user does not select a file, the browser submits an
        # # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('download_file', name=filename))
        # return render_template("upload.html")

    @login_manager.user_loader
    def load_user(user_id): # TODO
        usr = hood.get_user(user_id)
        return usr

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        session.pop('_flashes', None)
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
        response = make_response(render_template('login.html'))
        return response

    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        session.pop('_flashes', None)
        if request.method == "POST":
            uname = request.form.get("Usrname") 
            pswd = request.form.get("Password") 
            usr = hood.sign_up(uname, pswd)
            if usr: # User does not exist
                login_user(usr)
                flash('Signed in successfully.')
                return redirect("/")                
            if not usr:
                flash('Signup failed! Please select another username.')
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
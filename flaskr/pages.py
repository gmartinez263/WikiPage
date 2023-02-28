from flask import render_template


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.

    # TODO DELETE
      # Imports the Google Cloud client library
    @app.route("/image/james")
    def get_james():
        from google.cloud import storage
        # Instantiates a client
        storage_client = storage.Client()
        # Bucket names
        content_wiki_name = "content-wiki"
        # bucket instanttiation
        content_wiki_bucket = storage_client.bucket(content_wiki_name)
        # Hopefully getting the image
        image_blob = content_wiki_bucket.blob("images/james.jpg")
        image = image_blob.download_as_bytes()
        # Imprts flask Response library
        from flask import Response
        return Response(image, mimetype='image/jpeg')
    # TODO DELETE

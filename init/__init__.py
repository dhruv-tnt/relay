import os
from flask import Flask

class initialize:
    #create app
    def create_app():
        app=Flask(__name__, template_folder='../templates')
        return app

    #register bluepint
    def register_bp(app):
        import route.bp as bp
        app.register_blueprint(bp.new_bp)
        return app
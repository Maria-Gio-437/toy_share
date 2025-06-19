from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .routes.usuario_routes import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api')

    @app.route('/health')
    def health_check():
        return "API está funcionando!"

    return app
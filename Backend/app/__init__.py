from flask import Flask

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)

    from .routes.usuario_routes import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api')

    @app.route('/health')
    def health_check():
        return "API está funcionando!"

    return app
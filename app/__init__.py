from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here-make-it-very-long-and-random'
    
    # Import and register blueprints
    from .routes import home_bp, books_bp, about_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(about_bp)
    
    return app
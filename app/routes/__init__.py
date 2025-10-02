from .home import bp as home_bp
from .books import bp as books_bp  
from .about import bp as about_bp

# This makes the blueprints available to the main app
__all__ = ['home_bp', 'books_bp', 'about_bp']
# app.py
from flask import Flask, g
from config import Config
from models import get_db
from routes.auth_routes import auth_bp
from routes.file_routes import file_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_bp, url_prefix='/file')

# Database teardown on app context end
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True)

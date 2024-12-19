from flask import Flask
from data.database_functions import initialize_db
from blueprints import register_blueprints
from flask_cors import CORS

app = Flask(__name__)
register_blueprints(app)
CORS(app, supports_credentials=True)
initialize_db()
@app.route('/')
def route_default():
    return 'Welcome'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
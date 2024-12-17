from flask import Flask
from quiz_system.data.database_functions import initialize_db
from quiz_system.blueprints import register_blueprints

app = Flask(__name__)

initialize_db()
register_blueprints(app)

@app.route('/')
def route_default():
    return 'Welcome'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
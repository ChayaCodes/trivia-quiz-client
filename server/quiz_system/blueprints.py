# blueprints.py

from quiz_system.api.auth_api import auth_api
from quiz_system.api.quizzes_interface_api import quizzes_interface_api
from quiz_system.api.quiz_service import quiz_service_api


def register_blueprints(app):
    app.register_blueprint(auth_api)
    app.register_blueprint(quizzes_interface_api)
    app.register_blueprint(quiz_service_api)
    

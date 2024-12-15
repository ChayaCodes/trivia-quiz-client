# blueprints.py
from havruta import havruta_api
from tremp import tremp_api
from free_items import free_items_api
from temporary_position import temporary_position_api
from zmanim import zmanim_api
from private_teacher import private_teacher_api
from quiz_system.auth_api import auth_api
from quiz_system.quizzes_interface_api import quizzes_interface_api
from quiz_system.quiz_service import quiz_service_api


def register_blueprints(app):
    app.register_blueprint(havruta_api)
    app.register_blueprint(tremp_api)
    app.register_blueprint(free_items_api)
    app.register_blueprint(temporary_position_api)
    app.register_blueprint(zmanim_api)
    app.register_blueprint(private_teacher_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(quizzes_interface_api)
    app.register_blueprint(quiz_service_api)
    
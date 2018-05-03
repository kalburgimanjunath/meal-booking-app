from flask import Blueprint

main = Blueprint('main', __name__, template_folder='pages')
from .import views  # noqa

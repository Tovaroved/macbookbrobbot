from flask import Blueprint
from apps.shipper.views import shipperRouter
from apps.parsing.gsheet import gsheetRouter

routers = Blueprint('routes', __name__)

routers.register_blueprint(shipperRouter)
routers.register_blueprint(gsheetRouter)

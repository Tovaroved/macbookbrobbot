from flask import Blueprint
from apps.shipper.views import shipperRouter

routers = Blueprint('routes', __name__)

routers.register_blueprint(shipperRouter)
from flask import Blueprint
from utils.extensions import db
from ..utils import encode_date, arriving_date
from .service import get_list
from .models import Shipper
import json

shipperRouter = Blueprint('shipper', __name__, url_prefix='/shipper')


@shipperRouter.route('/packages', methods=['GET','POST'])
def get_data():
    data = get_list()
    for iter in range(len(data)):
        if not Shipper.query.get(data[iter].get('id')):
            obj = Shipper(id=data[iter].get('id'),
                        title=data[iter].get('description'),
                        track_number=data[iter].get('tracking_number'),
                        created_date=encode_date(data[iter].get('created_at')),
                        coming_date=arriving_date(data[iter].get('created_at'))
                        )
            db.session.add(obj)
            db.session.commit()
    return {"status":"success", "data": data}
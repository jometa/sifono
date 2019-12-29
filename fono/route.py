import json
from flask import (
    Blueprint,
    request,
    current_app
)
from fono.mongo import mongo_db
from fono.config import Encoder


bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route('kata/<kata>', methods=['GET'])
def get_kata(kata : str):
    result = mongo_db.data.find_one({
        'word': kata
    })
    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

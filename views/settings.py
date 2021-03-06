import json

from bson import json_util
from flask import request, Response
from models.setting import Setting


class Settings:
    @staticmethod
    def last_settings():
        settings = Setting()

        return Response(json.dumps(settings.all(section=request.args.get('name')), default=json_util.default), mimetype='application/json')

    @staticmethod
    def store(data): ## TODO: Data viene de request.get_json(), se puede obtener auqí mismo
        setting = Setting()
        res_data = setting.store(data)

        if res_data is None:
            response = Response(json.dumps({'error': 'Item not added - {}'}), status=400, mimetype='application/json')
            return response

        return Response(json.dumps(res_data, default=json_util.default), status=201, mimetype='application/json')
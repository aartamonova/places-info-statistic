import functools
import json
import logging

import requests
from flask import request, make_response, jsonify
from flask_api.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN
from flask_restful import fields, marshal, Resource

from config import Config
from statistic.statistic_model import ActionData

action_fields = {'id': fields.Integer,
                 'timestamp': fields.String,
                 'login': fields.String,
                 'type': fields.String,
                 'description': fields.String,
                 'result': fields.String}

action_list_fields = {'count': fields.Integer,
                      'actions': fields.List(fields.Nested(action_fields))}

logging.basicConfig(filename="log_data.log", level=logging.WARNING, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def access_token_required(foo):
    @functools.wraps(foo)
    def wrapper(*args, **kwargs):
        if 'Gui-Token' in request.headers:
            access_token = request.headers['Gui-Token']
            # Проверить токен
            response = requests.get(Config.AUTH_SERVICE_URL + '/token/validate', 'source_app=' +
                                    str(Config.SOURCE_APP) + '&request_app=' + str(Config.REQUEST_APP) +
                                    '&access_token=' + str(access_token))

            if response.status_code != HTTP_200_OK:
                return make_response(jsonify({'error': 'Invalid authorization data'}), HTTP_403_FORBIDDEN)

            return foo(*args, **kwargs)
        else:
            return make_response(jsonify({'error': 'Invalid authorization data'}), HTTP_403_FORBIDDEN)

    return wrapper


class ActionAddResource(Resource):
    @staticmethod
    def post():
        try:
            login = json.loads(request.data.decode("utf-8"))['login']
            action_type = json.loads(request.data.decode("utf-8"))['type']
            description = json.loads(request.data.decode("utf-8"))['description']
            result = json.loads(request.data.decode("utf-8"))['result']
        except:
            return make_response(jsonify({'error': 'Invalid action data'}), HTTP_400_BAD_REQUEST)

        action = ActionData.create(login, action_type, description, result)
        logging.warning('Добавление в статистику действия пользователя %s' % login)

        if not action:
            return make_response(jsonify({'error': 'The action not created'}), HTTP_404_NOT_FOUND)
        else:
            try:
                content = make_response(marshal(action, action_fields), HTTP_200_OK)
            except:
                return make_response(jsonify({'error': 'Corrupted database data'}), HTTP_500_INTERNAL_SERVER_ERROR)
            return make_response(content, HTTP_200_OK)


class ActionListResource(Resource):
    @staticmethod
    @access_token_required
    def get():
        login = request.args.get('login', type=str, default='')
        action_type = request.args.get('type', type=str, default='')

        actions = ActionData.get_all(login, action_type)
        logging.warning('Получение статистики действий пользователя %s' % login)
        if not actions:
            return make_response(jsonify({'error': 'The action database is empty'}), HTTP_404_NOT_FOUND)
        else:
            try:
                content = marshal({'count': len(actions), 'actions': [marshal(a, action_fields) for a in actions]},
                                  action_list_fields)
            except:
                return make_response({'error': 'Corrupted database data'}, HTTP_500_INTERNAL_SERVER_ERROR)

            return make_response(content, HTTP_200_OK)

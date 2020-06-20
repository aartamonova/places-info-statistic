import datetime as datetime

from sqlalchemy import DateTime

from statistic import db


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    login = db.Column(db.String(20))
    description = db.Column(db.String(128))
    result = db.Column(db.String(20))
    timestamp = db.Column(DateTime, default=datetime.datetime.utcnow)


class ActionData:
    @staticmethod
    def get_all(login, action_type):
        '''Получить список действий по логину пользователя и по типу действия'''
        actions = Action.query.filter_by(login=login, type=action_type).all()
        return actions

    @staticmethod
    def create(login, action_type, description, result):
        '''Добавить действие пользователя'''
        action = Action(login=login, type=action_type, description=description, result=result)
        if action:
            db.session.add(action)
            db.session.commit()
        else:
            return None
        return action

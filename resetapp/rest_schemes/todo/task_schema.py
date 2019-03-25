import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_rest_jsonapi import ResourceList, ResourceDetail, JsonApiException
from marshmallow_enum import EnumField
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from pgmagic import session

from resetapp.models.todo import Task as TaskModel

log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_fmt, level=logging.WARNING)
logger = logging.getLogger(__name__)


class TaskSchema(Schema):
    class Meta:
        type_ = 'task'
        self_view = 'task_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'task_list'

    """ marshalling rules
    """
    id = fields.Integer(as_string=True, dump_only=True)
    title = fields.Str(required=True)
    uid = fields.Integer(dump_only=True)
    desc = fields.Str()
    status = EnumField(TaskModel.Status)


with session() as s:
    """ Single session pool for this scope, that can be one of:
         - NullPool
         - QueuePool
         - SingletonThreadPool
         - StaticPool
    """

    class TaskList(ResourceList):
        schema = TaskSchema

        def before_create_object(self, data, view_kwargs):
            current_user = get_jwt_identity()
            if current_user is not None:
                data['uid'] = current_user.get("uid")
            else:
                raise JsonApiException(detail="You are not authorized to use this resource.",
                                       status=403,
                                       title="Authorization Error")
        data_layer = {'session': s,
                      'model': TaskModel,
                      'methods': {'before_create_object': before_create_object}}

        decorators = (jwt_required,)

        @staticmethod
        def route():
            return '/api/v1/tasks'

        @staticmethod
        def rest_desc():
            return "task_list"


    class TaskDetail(ResourceDetail):
        schema = TaskSchema

        def before_get_object(self, view_kwargs):
            current_user = get_jwt_identity()

            with session() as s:
                obj = s.query(TaskModel) \
                    .filter(TaskModel.id == view_kwargs.get("id")) \
                    .filter(TaskModel.uid == current_user.get("uid")) \
                    .first()
            if not obj:
                raise JsonApiException(detail="You are not authorized to use this resource.",
                                       status=403,
                                       title="Authorization Error")

        data_layer = {'session': s,
                      'model': TaskModel,
                      'methods': {'before_get_object': before_get_object}}

        decorators = (jwt_required,)

        @staticmethod
        def route():
            return '/api/v1/task/<int:id>'

        @staticmethod
        def rest_desc():
            return "task_details"

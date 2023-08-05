# -*- coding: utf-8 -*-
from inspect import isclass

import funcy
from flask import g, request
from flask_restful import Resource, abort

# from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..metrics.exception import ProViewError, ViewErrorCode
from ..metrics.mock import MockResp
from ..model.base import db, get_session


class BaseResource(Resource):
    decorators = []
    default_exist = True
    MODEL = None

    def __init__(self, *args, **kwargs):
        super(BaseResource, self).__init__(*args, **kwargs)
        self._user = None

    def dispatch_request(self, *args, **kwargs):
        return super(BaseResource, self).dispatch_request(*args, **kwargs)

    def get_by_id(self, target_id):
        return self.MODEL.object().filter_by(id=target_id).first()

    def delete_by_id(self, target_id):
        return self.MODEL.object().filter_by(id=target_id).delete()

    def update_by_id(self, target_id, data):
        return self.MODEL.object().filter_by(id=target_id).update(data)

    @property
    def model(self):
        obj = self.MODEL.object()
        if not self.is_admin:
            obj = obj.filter_by(author_id=self.author_id)
        # return self.MODEL.object().filter_by(author_id=self.author_id)
        # TODO: 先支持所有人都可以查看
        return obj

    def get_obj(self, target_id, get_only_oneself=True):
        no_can_all = get_only_oneself and not self.is_admin
        if self.default_exist:
            obj = self.MODEL.object()
        else:
            obj = self.MODEL.query
        obj = obj.filter_by(id=target_id)
        if no_can_all:
            obj = obj.filter_by(author_id=self.author_id)
        return obj

    @property
    def current_user(self):
        # return current_user._get_current_object()
        return g.current_user

    @property
    def is_admin(self):
        return self.current_user.is_has_admin

    @property
    def author_id(self):
        return self.current_user.ding_talk_id

    @property
    def author(self):
        return self.current_user.real_name
    #
    # def record_event(self, options):
    #     record_event(self.current_org, self.current_user, options)
    #
    # # TODO: this should probably be somewhere else
    # def update_model(self, model, updates):
    #     for k, v in updates.items():
    #         setattr(model, k, v)


def paginate(query_set, page, page_size, serializer, **kwargs):
    if not hasattr(query_set, "paginate"):
        if isinstance(query_set, (list, tuple)):
            total = page_size = len(query_set)
            results = query_set
        else:
            total = page_size = 0
            results = []
        return {
            'total': total,
            'page': 1,
            'page_size': page_size,
            'results': results,
        }

    total = query_set.count()

    if page < 1:
        abort(400, message='Page must be positive integer.')

    if (page - 1) * page_size + 1 > total > 0:
        abort(400, message='Page is out of range.')

    if page_size > 250 or page_size < 1:
        abort(400, message='Page size is out of range (1-250).')

    results = query_set.paginate(page, page_size)

    # support for old function based serializers
    if isclass(serializer):
        items = serializer(results.items, **kwargs).serialize()
    else:
        items = [serializer(result) for result in results.items]

    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'results': items,
    }


class ViewRs(BaseResource):
    methods = ("get", "post")
    MODEL = None
    request_fields = ()
    ORDER_BY_FIELD = "id"
    SUPPORT_SEARCH = True

    @classmethod
    def pretreat(cls, data):
        return data

    @classmethod
    def postreat(cls, instance):
        return

    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 25, type=int)
        query = self.MODEL.query
        if self.SUPPORT_SEARCH:
            options = funcy.project(request.args.to_dict(), self.request_fields)
            query = query.filter_by(**options)

        data = paginate(query.order_by(getattr(self.MODEL, self.ORDER_BY_FIELD).desc()), page, page_size,
                        lambda x: x)
        return MockResp.success(data=data, desc="载入列表")

    def post(self):
        rcv = funcy.project(request.json, keys=self.request_fields)
        rcv = self.pretreat(rcv)
        with get_session() as session:
            obj = self.MODEL(**rcv)
            db.session.add(obj)
        self.postreat(obj)
        return MockResp.success(data=obj.to_dict(), desc="添加资源")


class ViewTargetRs(BaseResource):
    methods = ("get", "put", "delete")
    MODEL = None
    request_fields = ()

    @classmethod
    def pretreat(cls, data, instance):
        return data

    @classmethod
    def postreat(cls, instance):
        return

    def get(self, target_id):
        obj = self.get_by_id(target_id=target_id)

        return MockResp.success(data=obj.to_dict(), desc="目标任务详情")

    def put(self, target_id):
        rcv = funcy.project(request.json, keys=self.request_fields)
        rcv = self.pretreat(rcv, instance=None)
        count = self.update_by_id(target_id=target_id, data=rcv)
        if count == 1:
            db.session.commit()
            self.postreat(instance=None)
            return MockResp.success(message="update success")
        else:
            return MockResp.fail(message="update fail")

    def pull_put(self, target_id):
        rcv = funcy.project(request.json, keys=self.request_fields)
        obj = self.get_by_id(target_id=target_id)
        if not obj:
            raise ProViewError(ViewErrorCode.no_found, f"target(id={target_id}) no found!")
        rcv = self.pretreat(rcv, instance=obj)
        with get_session() as session:
            obj.update_data(rcv)
            self.postreat(obj)

        return MockResp.success(data=obj.to_dict(), message="update success")

    def delete(self, target_id):
        obj = self.get_by_id(target_id=target_id)
        count = obj.delete()
        db.session.commit()
        if count == 0:
            return MockResp.fail(message="删除失败：资源不存在", desc="删除指令")
        else:
            return MockResp.success(message="删除成功", desc="删除指令")


class ViewFileUpload(BaseResource):
    """
    文件上传
    """
    FILE_FIELD = "file"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._filename = None
        self._etag = None
        self.size = 0

    @classmethod
    def get_secure_filename(cls, filename) -> str:
        """
        为处理中文名字，无法正常显示
        """
        from unicodedata import normalize
        return secure_filename(normalize('NFKD', filename).encode('utf-8', 'strict').decode('utf-8'))

    def handle_file(self):
        from flask import request
        fr = request.files.get(self.FILE_FIELD)
        if not fr:
            raise ProViewError(ViewErrorCode.no_found, "上传文件不存在")

        self._filename = self.get_secure_filename(fr.filename)
        return fr

    def load_file_model(self, model, all_create=True):
        fr = self.handle_file()
        return model.select_save_file(fr.filename, stream=fr, all_create=all_create)

    def filename(self) -> str:
        return self._filename

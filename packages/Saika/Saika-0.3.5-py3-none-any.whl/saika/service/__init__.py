from saika.database import db
from .forms import FieldOperateForm
from .. import common


def with_auto_commit(f):
    def wrapper(*args, **kwargs):
        self = args[0]  # type: Service
        result = f(*args, **kwargs)
        self._do_auto_commit()
        return result

    return wrapper


def with_pk_filter(f):
    def wrapper(*args, **kwargs):
        self = args[0]  # type: Service
        self.__class__._append_pk_filter(*args, **kwargs)
        return f(*args, **kwargs)

    return wrapper


class Service:
    def __init__(self, model_class):
        self.model_class = model_class
        self.model_pks = db.get_primary_key(model_class, False)

        self._orders = []
        self._filters = []

        self._processes = []
        self._auto_commit = True
        self._without_pk_filter = False

    @property
    def without_pk_filter(self):
        self._without_pk_filter = True
        return self

    def associate_do(self, f):
        pks = self.get_pks()
        if pks:
            return f(pks)

    def associate_edit(self, **kwargs):
        return self.associate_do(
            lambda pks: self.edit(*pks, **kwargs)
        ) or 0

    def associate_delete(self, **kwargs):
        return self.associate_do(
            lambda pks: self.delete(*pks, **kwargs)
        ) or 0

    def set_orders(self, *orders):
        self._orders = orders

    def set_filters(self, *filters):
        self._filters = filters

    def orders(self, *orders):
        return self.processes(lambda query: query.order_by(*orders))

    def join(self, target, *props, outer=False, **kwargs):
        if outer:
            return self.processes(lambda query: query.outerjoin(target, *props, **kwargs))
        else:
            return self.processes(lambda query: query.join(target, *props, **kwargs))

    def filters(self, *filters, **model_eq_filters):
        if model_eq_filters:
            filters = list(filters)
            for k, v in model_eq_filters.items():
                filters.append(getattr(self.model_class, k).__eq__(v))

        return self.processes(lambda query: query.filter(*filters))

    def processes(self, *query_processes):
        self._processes += query_processes
        return self

    def set_auto_commit(self, enable=True):
        self._auto_commit = enable

    @property
    def query(self):
        return db.query(self.model_class, commit=self._auto_commit)

    @property
    def pk_field(self):
        [pk] = self.model_pks
        field = getattr(self.model_class, pk)
        return field

    def pk_filter(self, *ids):
        if len(ids) == 1:
            return self.pk_field.__eq__(*ids)
        else:
            return self.pk_field.in_(ids)

    def process_query(self, query=None, filters=True, orders=True, clear=True):
        if query is None:
            query = self.query
        if filters:
            query = query.filter(*self._filters)
        if orders:
            query = query.order_by(*self._orders)

        for process in self._processes:
            query = process(query) if callable(process) else process
        if clear:
            self.processes_clear()

        if self._auto_commit:
            db.session.commit()

        return query

    def processes_clear(self):
        self._processes.clear()
        self._without_pk_filter = False

    @with_auto_commit
    def list(self, page, per_page, **kwargs):
        return self.process_query().paginate(page, per_page, **kwargs)

    @with_auto_commit
    def get_one(self, **kwargs):
        return self.process_query(**kwargs).first()

    @with_auto_commit
    def get_all(self, **kwargs):
        return self.process_query(**kwargs).all()

    @with_auto_commit
    def get_pks(self, **kwargs):
        return list(map(lambda item: item[0], self.process_query(**kwargs).values(self.pk_field)))

    @with_auto_commit
    def count(self, **kwargs):
        kwargs.setdefault('orders', False)
        return self.process_query(**kwargs).count()

    def item(self, pk, pk_field=None, **kwargs):
        if pk_field is None:
            self.filters(self.pk_filter(pk))
        else:
            if isinstance(pk_field, str):
                pk_field = getattr(self.model_class, pk_field)

            self.filters(pk_field == pk)

        return self.get_one()

    def items(self, *pks, pk_field=None, **kwargs):
        if pk_field is None:
            self.filters(self.pk_filter(*pks))
        else:
            if isinstance(pk_field, str):
                pk_field = getattr(self.model_class, pk_field)

            self.filters(pk_field.in_(pks))

        return self.get_all()

    @with_auto_commit
    def add(self, **kwargs):
        model = self.model_class(**kwargs)
        db.session.add(model)
        return model

    @with_pk_filter
    @with_auto_commit
    def edit(self, *ids, **kwargs):
        return self.process_query(
            orders=False
        ).update(kwargs)

    @with_pk_filter
    @with_auto_commit
    def delete(self, *ids, **kwargs):
        return self.process_query(
            orders=False
        ).delete()

    def _do_auto_commit(self):
        if self._auto_commit:
            db.session.commit()

    def _append_pk_filter(self, *ids, **kwargs):
        if self._without_pk_filter:
            return

        ids = self.collect_ids(ids, kwargs)
        self.filters(self.pk_filter(*ids))

    @staticmethod
    def collect_ids(ids, kwargs):
        id_ = kwargs.pop('id', None)
        if id_ is not None:
            ids = [id_, *ids]

        return common.list_group_by(ids)

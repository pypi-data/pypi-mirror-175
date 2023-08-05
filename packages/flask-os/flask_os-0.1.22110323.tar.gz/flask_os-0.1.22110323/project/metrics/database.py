import logging
import time

from flask import g, has_request_context

from sqlalchemy.engine import Engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm.util import _ORMJoin
from sqlalchemy.sql.selectable import Alias

logger = logging.getLogger(__name__)


def _table_name_from_select_element(elt):
    t = elt.froms[0]

    if isinstance(t, Alias):
        try:
            t = t.original.froms[0]
        except AttributeError:
            t = t.original.element.froms[0]

    while isinstance(t, _ORMJoin):
        t = t.left

    return t.name


@listens_for(Engine, "before_execute")
def before_execute(conn, elt, multiparams, params):
    conn.info.setdefault('query_start_time', []).append(time.time())


@listens_for(Engine, "after_execute")
def after_execute(conn, elt, multiparams, params, result):
    duration = 1000 * (time.time() - conn.info['query_start_time'].pop(-1))
    action = elt.__class__.__name__

    if action == 'Select':
        name = 'unknown'
        try:
            name = _table_name_from_select_element(elt)
        except Exception:
            logging.exception('Failed finding table name.')
    elif action in ['Update', 'Insert', 'Delete']:
        name = elt.table.name
    else:
        # create/drop tables, sqlalchemy internal schema queries, etc
        return

    action = action.lower()

    logger.debug("table=%s query=%s duration=%.2f", name, action,
                 duration)
    logger.debug("sql=%s", elt.__str__())

    if has_request_context():
        g.setdefault('queries_count', 0)
        g.setdefault('queries_duration', 0)
        g.queries_count += 1
        g.queries_duration += duration

    return result

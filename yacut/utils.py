from random import choice

from yacut import db
from yacut.constants import (
    GENERATION_ATTEMPTS, RESERVED_PATHS, SHORT_ID_CHARS, SHORT_LINK_LENGTH
)
from yacut.models import URLMap


def get_unique_short_id():
    for _ in range(GENERATION_ATTEMPTS):
        short_id = ''.join(
            choice(SHORT_ID_CHARS) for _ in range(SHORT_LINK_LENGTH)
        )
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
    raise RuntimeError(
        'Не удалось сгенерировать уникальный короткий идентификатор.'
    )


def save_url_map(original, short=None):
    if short is None:
        short = get_unique_short_id()
    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()
    return url_map


def get_url_map_by_short(short_id):
    return URLMap.query.filter_by(short=short_id).first()


def is_short_id_available(short_id):
    return (
        short_id not in RESERVED_PATHS and
        URLMap.query.filter_by(short=short_id).first() is None
    )

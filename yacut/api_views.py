import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (
    DUPLICATE_MESSAGE, ID_NOT_FOUND_MESSAGE, INVALID_SHORT_ID_MESSAGE,
    MAX_SHORT_ID_LENGTH, NO_BODY_MESSAGE, NO_URL_FIELD_MESSAGE,
    SHORT_ID_PATTERN
)
from yacut.utils import (
    get_unique_short_id, get_url_map_by_short, save_url_map
)


@app.route('/api/id/', methods=['POST'])
def api_create_id():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(
            {'message': NO_BODY_MESSAGE}
        ), HTTPStatus.BAD_REQUEST

    if 'url' not in data:
        return jsonify(
            {'message': NO_URL_FIELD_MESSAGE}
        ), HTTPStatus.BAD_REQUEST

    custom_id = data.get('custom_id')

    if custom_id:
        if (len(custom_id) > MAX_SHORT_ID_LENGTH or
                not re.match(SHORT_ID_PATTERN, custom_id)):
            return jsonify(
                {'message': INVALID_SHORT_ID_MESSAGE}
            ), HTTPStatus.BAD_REQUEST

        if get_url_map_by_short(custom_id):
            return jsonify(
                {'message': DUPLICATE_MESSAGE}
            ), HTTPStatus.BAD_REQUEST

        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = save_url_map(data['url'], short_id)

    return jsonify({
        'url': url_map.original,
        'short_link': request.host_url + url_map.short,
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def api_get_url(short_id):
    url_map = get_url_map_by_short(short_id)
    if url_map is None:
        return jsonify(
            {'message': ID_NOT_FOUND_MESSAGE}
        ), HTTPStatus.NOT_FOUND
    return jsonify({'url': url_map.original}), HTTPStatus.OK

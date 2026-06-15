import asyncio
from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from yacut import app
from yacut.constants import DUPLICATE_MESSAGE, RESERVED_PATHS
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import (
    get_unique_short_id, get_url_map_by_short, save_url_map
)
from yacut.yandex_disk import upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            if custom_id in RESERVED_PATHS or \
                    URLMap.query.filter_by(short=custom_id).first():
                flash(DUPLICATE_MESSAGE, 'error')
                return render_template('index.html', form=form)
            short_id = custom_id
        else:
            short_id = get_unique_short_id()

        url_map = save_url_map(original_link, short_id)
        short_link = request.host_url + url_map.short
        return render_template(
            'index.html', form=form, short_link=short_link
        )
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileUploadForm()
    uploaded_files = None

    if form.validate_on_submit():
        files = []
        for file_storage in form.files.data:
            filename = file_storage.filename
            file_bytes = file_storage.read()
            files.append((filename, file_bytes))

        loop = asyncio.new_event_loop()
        try:
            disk_results = loop.run_until_complete(
                upload_files_to_disk(files)
            )
        finally:
            loop.close()

        uploaded_files = []
        for filename, download_link in disk_results:
            short_id = get_unique_short_id()
            url_map = save_url_map(download_link, short_id)
            uploaded_files.append({
                'name': filename,
                'short_link': request.host_url + url_map.short,
            })

    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = get_url_map_by_short(short_id)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)

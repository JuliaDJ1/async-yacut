import os

import aiohttp

from yacut.constants import YANDEX_DISK_BASE_URL


def get_headers():
    token = os.getenv('DISK_TOKEN')
    return {'Authorization': f'OAuth {token}'}


async def get_upload_link(session, filename):
    url = f'{YANDEX_DISK_BASE_URL}/resources/upload'
    path = f'/{filename}'
    params = {'path': path, 'overwrite': 'true'}
    async with session.get(
        url, headers=get_headers(), params=params
    ) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data['href'], path


async def upload_file(session, upload_href, file_bytes):
    async with session.put(upload_href, data=file_bytes) as resp:
        if resp.status not in (200, 201, 202):
            resp.raise_for_status()


async def get_download_link(session, path):
    url = f'{YANDEX_DISK_BASE_URL}/resources/download'
    params = {'path': path}
    async with session.get(
        url, headers=get_headers(), params=params
    ) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data['href']


async def upload_single_file(session, filename, file_bytes):
    upload_href, path = await get_upload_link(session, filename)
    await upload_file(session, upload_href, file_bytes)
    download_link = await get_download_link(session, path)
    return download_link


async def upload_files_to_disk(files):
    results = []
    async with aiohttp.ClientSession() as session:
        for filename, file_bytes in files:
            download_link = await upload_single_file(
                session, filename, file_bytes
            )
            results.append((filename, download_link))
    return results

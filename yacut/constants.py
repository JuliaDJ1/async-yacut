import string

ORIGINAL_MAX_LENGTH = 2048
SHORT_LINK_LENGTH = 6
MAX_SHORT_ID_LENGTH = 16
SHORT_ID_CHARS = string.ascii_letters + string.digits
SHORT_ID_PATTERN = r'^[a-zA-Z0-9]+$'

RESERVED_PATHS = ('files',)

GENERATION_ATTEMPTS = 10

DUPLICATE_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
NO_BODY_MESSAGE = 'Отсутствует тело запроса'
ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'
NO_URL_FIELD_MESSAGE = '"url" является обязательным полем!'

YANDEX_DISK_BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
YANDEX_DISK_UPLOAD_FOLDER = 'YaCut_files'

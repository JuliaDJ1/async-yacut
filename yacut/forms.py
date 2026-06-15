from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL
)

from yacut.constants import MAX_SHORT_ID_LENGTH, SHORT_ID_PATTERN


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректный URL'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                max=MAX_SHORT_ID_LENGTH,
                message='Короткое имя не может быть длиннее 16 символов'
            ),
            Regexp(
                SHORT_ID_PATTERN,
                message='Указано недопустимое имя для короткой ссылки'
            ),
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл')]
    )
    submit = SubmitField('Загрузить')

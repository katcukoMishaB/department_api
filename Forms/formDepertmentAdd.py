from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp

class DepartmentAdd(FlaskForm):
    department_name = StringField('Название департамента', validators=[DataRequired(),
        Regexp(r'^[a-zA-Zа-яА-Я0-9]+$', message='Название должно быть без пробелов'),
        Regexp(r'[a-zA-Zа-яА-Я]+', message='Название не должно состоять только из цифр')]),
    submit = SubmitField('Добавить департамент')
"""Regexp(r'^\S+$', message='Название не должно содержать пробелов'),
        Regexp(r'^[a-zA-Zа-яА-Я\s]+$', message='Название должно содержать только буквы'),
        Regexp(r'^[0-9\s]+$', message='Название должно содержать только цифры'),"""
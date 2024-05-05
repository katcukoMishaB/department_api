from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class DepartmentAdd(FlaskForm):
    department_name = StringField('Название департамента', validators=[DataRequired()])
    submit = SubmitField('Добавить департамент')
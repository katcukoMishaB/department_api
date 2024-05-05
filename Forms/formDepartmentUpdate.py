"""from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DepartmentUpdate(FlaskForm):
    current_department_name = StringField('Текущее название подразделения', validators=[DataRequired()])
    new_department_name = StringField('Новое название подразделения', validators=[DataRequired()])
    submit = SubmitField('Обновить')
"""
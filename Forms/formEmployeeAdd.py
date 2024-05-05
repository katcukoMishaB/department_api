from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class EmployeeAdd(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    patronimic = StringField('Отчество', validators=[DataRequired()])
    salary = IntegerField('Зарплата', validators=[DataRequired()])
    hire_date = DateField('Дата приема на работу', validators=[DataRequired()])
    department_name = StringField('Название департамента', validators=[DataRequired()])

    submit = SubmitField('Добавить')
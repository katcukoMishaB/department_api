from app import app, db
from Forms.formEmployeeAdd import EmployeeAdd

from Models.employeeModel import Employee
from Models.departmentModel import Department

from flask import render_template, flash, redirect, url_for, jsonify
from flask_restful import Resource, request



class EmployeeController(Resource):
    @staticmethod
    @app.route('/employees', methods=['GET'])
    def all_employees():
        employees = Employee.query.all()
        return render_template('employees.html', employees=employees)
    
    @staticmethod
    @app.route('/employees/add', methods=['GET', 'POST'])
    def add_employee():
        form = EmployeeAdd()
        if form.validate_on_submit():
            department_name = form.department_name.data
            department = Department.query.filter_by(department_name=department_name).first()
            if not department:
                flash('Департамент не найден.')
                return redirect(url_for('add_employee'))

            try:
                existing_employee = Employee.query.filter_by(
                last_name=form.last_name.data,
                first_name=form.first_name.data,
                patronimic=form.patronimic.data,
                department_id=department.id
                ).first()
                if existing_employee:
                    flash('Сотрудник с такими данными уже существует.')
                    return redirect('/employees/add')

                employee = Employee(
                    last_name=form.last_name.data,
                    first_name=form.first_name.data,
                    patronimic=form.patronimic.data,
                    salary=form.salary.data,
                    hire_date=form.hire_date.data,
                    department_id=department.id,
                )
                db.session.add(employee)
                db.session.commit()
                flash('Работник успешно добавлен.')
                return redirect('/employees/add')
            except Exception as err:
                flash(f'Ошибка при добавлении работника: {str(err)}')
                db.session.rollback()

        return render_template('employee_add.html', form=form)

    
    @staticmethod
    @app.route('/employees/search', methods=['GET', 'POST'])
    def search_employee():
        if request.method == 'POST':
            last_name = request.form.get('last_name')
            first_name = request.form.get('first_name')
            patronimic = request.form.get('patronimic')
            department_name = request.form.get('department_name')
            department = Department.query.filter_by(department_name=department_name).first()
            if not department:
                flash('Департамент не найден.')
                return redirect(url_for('search_employee'))

            employee = Employee.query.filter_by(
            last_name=last_name,
            first_name=first_name,
            patronimic=patronimic,
            department_id=department.id
            ).first()


            if employee:
                return redirect(url_for('search_employee_results', employee_id=employee.id))
            else:
                flash('Работник не найден')

        return render_template('employee_search.html')
        

    @staticmethod
    @app.route('/employees/search/<int:employee_id>', methods=['GET'])
    def search_employee_results(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        return render_template('employee_search_results.html', employee=employee)
    

    """@staticmethod
    @app.route('/employees/update', methods=['GET','PUT'])
    def update_department():
        if request.method == 'PUT':
            data = request.json
            current_department_name = data.get('current_department_name')
            new_department_name = data.get('new_department_name')

            department = Department.query.filter_by(department_name=current_department_name).first()
            department_2 = Department.query.filter_by(department_name=new_department_name).first()
            if department and not department_2:
                department.department_name = new_department_name
                db.session.commit()
                flash(f'Подразделение "{current_department_name}" успешно обновлено на "{new_department_name}".')
                return jsonify({'error': f'Подразделение "{current_department_name}" не найдено.'}), 200
            else:
                flash(f'Подразделение "{current_department_name}" не найдено или название на которые вы пытаетесь сменить уже существует')
                return jsonify({'error': f'Подразделение "{current_department_name}" не найдено.'}), 200
        
        return render_template('department_update.html')
    

    @staticmethod
    @app.route('/employees/delete', methods=['GET','DELETE'])
    def delete_department():
        if request.method == 'DELETE':
            data = request.json
            department_name = data.get('department_name')
            department = Department.query.filter_by(department_name=department_name).first()
            print(department)
            if department:
                try:
                    Employee.query.filter_by(department_id=department.id).delete()
                    db.session.delete(department)
                    db.session.commit()

                    flash(f'Подразделение "{department_name}" и все его работники успешно удалены.')
                    return jsonify({'message': f'Подразделение "{department_name}" и все его работники успешно удалены.'}), 200
                except Exception as e:
                    flash(f'Ошибка удаления подразделения: {str(e)}')
                    db.session.rollback()
                    return jsonify({'error': 'Ошибка удаления подразделения'}), 500
            else:
                flash(f'Подразделение "{department_name}" не найдено...')
                return jsonify({'error': f'Подразделение "{department_name}" не найдено.'}), 200

        return render_template('department_delete.html')"""
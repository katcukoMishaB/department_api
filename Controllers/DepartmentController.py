from app import app, db
from Forms.formDepertmentAdd import DepartmentAdd


from Models.departmentModel import Department
from Models.employeeModel import Employee
from flask import render_template, flash, redirect, url_for, jsonify
from flask_restful import Resource, request


class DepartmentController(Resource):
    
    @staticmethod
    @app.route('/departments/add', methods=['GET','POST'])
    def add_department():
        form = DepartmentAdd()
        if form.validate_on_submit():
            if request.content_type == 'application/json':
                data = request.json
            else:
                data = request.form
            
            print(data)
            department_name = data.get('department_name')

            existing_department = Department.query.filter_by(department_name=department_name).first()

            if existing_department:
                flash('Подразделение с таким названием уже существует.')
                return redirect(url_for('add_department'))

            new_department = Department(
                department_name = department_name
            )

            db.session.add(new_department)
            db.session.commit()

            print('добавлен')
            flash(f'Подразделение "{department_name}" успешно удалено.')
            return redirect(url_for('add_department'))
        return render_template('department_add.html', title='Department Add', form=form)
    

    @staticmethod
    @app.route('/departments', methods=['GET'])
    def all_departments():
        departments = Department.query.all()
        return render_template('departments.html', departments=departments)
    

    @staticmethod
    @app.route('/departments/search', methods=['GET', 'POST'])
    def search_department():
        if request.method == 'POST':
            department_name = request.form.get('department_name')
            department = Department.query.filter_by(department_name=department_name).first()
            if department:
                return redirect(url_for('search_department_results', department_id=department.id))
            else:
                flash('Подразделение не найдено')
        return render_template('department_search.html')

    @staticmethod
    @app.route('/departments/search/<int:department_id>', methods=['GET'])
    def search_department_results(department_id):
        department = Department.query.get_or_404(department_id)
        employees = Employee.query.filter_by(department_id=department_id).all()
        return render_template('department_search_results.html', department=department, employees=employees)

    


    @staticmethod
    @app.route('/departments/update', methods=['GET','PUT'])
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
    @app.route('/departments/delete', methods=['GET','DELETE'])
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

        return render_template('department_delete.html')
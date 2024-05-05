from app import app, db
from Forms.formDepertmentAdd import DepartmentAdd


from Models.departmentModel import Department
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
                print(f'уже есть')
                return jsonify({'message': 'Tags for this user already exist'}), 200

            new_department = Department(
                department_name = department_name
            )

            db.session.add(new_department)
            db.session.commit()

            print('добавлен')
            return redirect('/index')
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
        return render_template('department_search_results.html', department=department)

    

    @staticmethod
    @app.route('/departments/update', methods=['GET','POST'])
    def update_department():
        if request.method == 'POST':
            current_department_name = request.form.get('current_department_name')
            new_department_name = request.form.get('new_department_name')

            department = Department.query.filter_by(department_name=current_department_name).first()

            if department:
                department.department_name = new_department_name
                db.session.commit()
                flash(f'Подразделение "{current_department_name}" успешно обновлено на "{new_department_name}".')
                return redirect('/departments')
            else:
                flash(f'Подразделение "{current_department_name}" не найдено.')
                return redirect('/departments/update')

        return render_template('department_update.html')
    

    @staticmethod
    @app.route('/departments/delete', methods=['GET','POST'])
    def delete_department():
        if request.method == 'POST':
            department_name = request.form.get('department_name')

            department = Department.query.filter_by(department_name=department_name).first()
            print(department)
            if department:
                db.session.delete(department)
                db.session.commit()
                flash(f'Подразделение "{department_name}" успешно удалено.')
                return redirect('/departments')
            else:
                flash(f'Подразделение "{department_name}" не найдено.')
                return redirect('/departments')

        return render_template('department_delete.html')
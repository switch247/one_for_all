from flask import Blueprint, jsonify, request,flash,abort,redirect,url_for
from app import db
import json
# from app.models import user.User, employee.Employee ...
from app.models.employee import Employee



main = Blueprint('main', __name__)





@main.route('/check_db_connection')
def check_db_connection():
    try:
        db.session.execute("SELECT 1")
        return 'Database connected!'
    except Exception as e:
        return 'Database connection failed: ' + str(e)


@main.route('/', methods=['GET'])
def hello():
    return 'Hello World '

@main.route('/employees', methods=['GET'])
def get_employees():
    employees =Employee.query.all()  
    def r (x):
        x.pop('_sa_instance_state')
        return x
    x = [r(employee.__dict__) for employee in employees]
    print(x)
    # .with_entities(Employee.id,Employee.name,Employee.email,Employee.phone_number)
    # flash('Succesful')
    return jsonify(x), 200
# /dd824ec3-7c23-4714-9cb5-0b0a529166fc
@main.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    # print( data)
    # print(data['email'])
    employee1 = Employee.query.filter( Employee.email== data['email'] ).all()
    # print(employee)
    if employee1:
        return (jsonify({'error': 'user already exists'}),409)
    # 409 conflict
    else:
        try:
            employee = Employee(name=data['name'], phone_number=data['phone_number'], email=data['email'])
            # return employee.__dir__()
            db.session.add(employee)
            db.session.commit()
            model_dict = (employee.__dict__)
            # x  = {
            #     'id':employee.id,
            #     'name' : employee.name,
            #     'email':employee.email,
            #     'phone_number':employee.phone_number
            # }
            model_dict.pop('_sa_instance_state')
            # flash('Succesful')
            return jsonify(model_dict  ), 201
            
            
            # 201 = created
        except Exception as e:
            # print(e)
            return jsonify({"error":str(e.__dict__)}), 500
    
@main.route('/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        # print(employee.__dict__)
        model_dict = (employee.__dict__)
        try:
            # Removing a key using the pop() method
            model_dict.pop("_sa_instance_state")
        except Exception as e:
            pass
        return jsonify(model_dict), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

@main.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get(employee_id)
    # print(employee)
    if employee:
        data = request.get_json()
        employee.name = data['name']
        employee.phone_number = data['phone_number']
        # employee.email = data['email']
       
        db.session.commit()
        return redirect(url_for('main.get_employee', employee_id=employee_id))
    else:
        return jsonify({'message': 'Employee not found'}), 404,

@main.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted'}), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

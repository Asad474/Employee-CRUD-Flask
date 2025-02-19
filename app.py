from flask import Flask, jsonify, request
from json import loads
from models import create_employees
from db import conn

app = Flask(__name__)

create_employees()

@app.route('/')
def home():
    return 'Welcome to Flask'

@app.route('/employees', methods=['GET'])
def getEmployee():
    with conn.cursor() as curr:
        curr.execute('SELECT * FROM employees')
        rows = curr.fetchall()
    return jsonify(rows)

@app.route('/employees/<int:id>', methods=['GET'])
def getEmployeeById(id: int):
    with conn.cursor() as curr:
        curr.execute('SELECT * FROM employees WHERE id = %s', (id,))
        obj = curr.fetchone()
    
    if obj is None:
        return jsonify({'message': 'Employee not found'}), 404

    return jsonify(obj)

@app.route('/employees', methods=['POST'])
def createEmployee():
    new_employee = loads(request.data)

    if not all([new_employee.get('id'), new_employee.get('name'), new_employee.get('email'), new_employee.get('salary'), new_employee.get('position')]):
        return jsonify({'message': 'All input fields are required.'}), 400

    new_obj = {
        'id': new_employee['id'],
        'name': new_employee['name'],
        'email': new_employee['email'],
        'salary': new_employee['salary'],
        'position': new_employee['position'],
    }

    with conn.cursor() as curr:
        curr.execute(
            'INSERT INTO employees (id, name, email, salary, position) VALUES (%s, %s, %s, %s, %s)',
            (new_obj['id'], new_obj['name'], new_obj['email'], new_obj['salary'], new_obj['position'])
        )
        conn.commit()

    return jsonify(new_obj), 201

@app.route('/employees/<int:id>', methods=['PATCH'])
def updateEmployee(id: int):
    obj = loads(request.data)

    with conn.cursor() as curr:
        curr.execute('select * from employees where id=(%s)', (id,))
        existing_employee = curr.fetchone()
        print('E', existing_employee)

        if existing_employee is None:
            return jsonify({'message': 'Employee not found'}), 404

        if not obj:
            return jsonify({'message': 'No fields provided, returning existing employee', 'employee': existing_employee}), 200

        update_fields = []
        values = []

        if 'name' in obj:
            update_fields.append("name = %s")
            values.append(obj['name'])
        
        if 'email' in obj:
            update_fields.append("email = %s")
            values.append(obj['email'])

        if 'salary' in obj:
            update_fields.append("salary = %s")
            values.append(obj['salary'])

        if len(update_fields) > 0 and len(values) > 0:
            values.append(id)
            query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = %s"
            curr.execute(query, values)
            conn.commit()

    return jsonify({'message': 'Employee updated successfully'}), 200

@app.route('/employees/<int:id>', methods=['DELETE'])
def deleteEmployee(id: int):
    with conn.cursor() as curr:
        # Check if employee exists
        curr.execute('SELECT * FROM employees WHERE id = %s', (id,))
        existing_employee = curr.fetchone()

        if existing_employee is None:
            return jsonify({'message': 'Employee not found'}), 404

        # Delete the employee
        curr.execute('DELETE FROM employees WHERE id = %s', (id,))
        conn.commit()

    return jsonify({'message': 'Employee deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import IntegrityError

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            studentID TEXT PRIMARY KEY,
            studentName TEXT NOT NULL,
            course TEXT NOT NULL,
            presentDate TEXT NOT NULL
        )
    ''')
    conn.close()

@app.route('/students', methods=['GET'])
def get_students(): 
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM students')
    rows = cursor.fetchall()

    conn.close()

    students = [dict(row) for row in rows]

    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_students():
    added_student = request.get_json()

    id = added_student.get('studentID')
    name = added_student.get('studentName')
    course = added_student.get('course')
    present_date = added_student.get('presentDate')

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO students (studentID, studentName, course, presentDate) VALUES (?, ?, ?, ?)',
            (id, name, course, present_date)
        )
        conn.commit()
    except IntegrityError:
        conn.close()
        return jsonify({'error': 'Student already exists'}), 409
    conn.close()

    return jsonify({'message': 'Student added successfully' }), 201

@app.route('/students', methods=['DELETE']) 
def delete_student():
    student_id = request.get_json().get('studentID')

    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE studentID = ?', (student_id,))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student deleted successfully'}), 200

@app.route('/students', methods=['PUT'])
def update_student():
    data = request.get_json()
    student_id = data.get('studentID')
    name = data.get('studentName')

    conn = get_db_connection()
    cursor = conn.execute(
        'UPDATE students SET studentName = ? WHERE studentID = ?',
        (name, student_id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify({'message': 'Student updated successfully'}), 200


if __name__ == '__main__':
    init_db()
    app.run(host= '0.0.0.0', port=5000) 

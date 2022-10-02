from app import app
from flask import render_template

from app.database import db
from app.models import Students
from app.constants import class_letters

from datetime import datetime


@app.route('/select_students', methods=['GET', 'POST'])
def select_students():
    students = Students.query
    date = datetime.now().date()
    year = date.year - (1 if date.month < 9 else 0)
    return render_template("docs/select_students.html",
                           db=db,
                           students=students,
                           letters=class_letters,
                           year=year, let=1)

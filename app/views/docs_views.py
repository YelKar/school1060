import os

from docx2pdf import convert

from app import app
from flask import render_template, request, redirect, \
    url_for, send_file

from app.database import db
from app.models import Students
from app.constants import class_letters, year_to_classroom

from datetime import datetime
from app.documents import docs

doc_names = [
    name[:-5] for name
    in os.listdir("app/documents/templates")
    if name[-5:] == ".docx"
]


@app.route('/select_students', methods=['GET', 'POST'])
def select_students():
    students = Students.query
    date = datetime.now().date()
    year = date.year - (1 if date.month < 9 else 0)
    return render_template("docs/select_students.html",
                           db=db,
                           students=students,
                           letters=class_letters,
                           year=year, let=1,
                           title=f'Выбор учеников для документа "{request.args.get("doc")}"')


@app.route('/select_documents', methods=['GET', 'POST'])
def select_documents():
    if request.method == "POST":
        doc = request.form.get("docs")
        return redirect(url_for("select_students", doc=doc))
    return render_template("docs/select_documents.html",
                           docs=doc_names,
                           title="Выбор документов для печати")


@app.route('/generate')
def generate_docs():
    doc_name = request.args.get("doc")
    doc_type = request.args.get("type")
    students_id = filter(
        lambda x: x,
        request.args.getlist("students")
    )
    students = [
        Students.query.filter_by(id=int(student_id)).first()
        for student_id in students_id
    ]
    generated = docs.generate(doc_name, *docs.query2context(students))
    if doc_type == "docx":
        return send_file(generated, as_attachment=True)
    elif doc_type == "pdf":
        return send_file(docs.to_pdf(generated), as_attachment=True)
    elif doc_type == "print":
        return send_file(docs.to_pdf(generated))


@app.route('/generate_table', methods=['GET', 'POST'])
def generate_table():
    students = Students.query
    date = datetime.now().date()
    year = date.year - (1 if date.month < 9 else 0)
    return render_template("tables/select_students.html",
                           db=db,
                           students=students,
                           letters=class_letters,
                           year=year, let=1,
                           title=f'Выбор учеников для генерации таблицы')

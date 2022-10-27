import os

import tables
from app import app
from flask import render_template, request, redirect, \
    url_for, send_file
from sqlalchemy.orm.scoping import scoped_session

from app.database import db
from app.models import Students
from app.constants import class_letters

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


@app.route('/generating_docx')
@app.route('/generating_pdf')
@app.route('/generating_print')
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
def table():
    students = Students.query
    date = datetime.now().date()
    year = date.year - (1 if date.month < 9 else 0)
    return render_template("tables/select_students.html",
                           db=db,
                           students=students,
                           letters=class_letters,
                           year=year, let=1,
                           title=f'Выбор учеников для генерации таблицы')


@app.route('/generating_xlsx')
def generate_table():
    print(request.args.getlist("fills"))
    student_ids = list(
        map(
            int, request.args.getlist("students")
        )
    )
    titles = ["Фамилия", "Имя", "Отчество"]
    fillings = ["lastname", "name", "patronymic"]
    titles += request.args.getlist("headers")
    query = [
        eval(f"Students.{filling}")
        for filling in fillings
    ]
    if int(request.args.get("class_sheets")):
        students = query_for_table(student_ids, query + [Students.id])

        sheets = {}
        for student in students:
            grade = Students.query.filter_by(id=student.id).first().full_grade()
            sheet_name = f"{grade} класс"
            sheet = sheets.get(sheet_name)
            if not sheet:
                sheets[sheet_name] = []
            sheets[sheet_name].append(student[:-1])
    else:
        students = query_for_table(student_ids, query)
        sheets = {
            "sheet": students
        }
    return send_file(tables.generate(titles, **sheets,
                                     fullname=not int(request.args.get("split_fullname"))), as_attachment=True)


def query_for_table(ids, query):
    session: scoped_session = db.session
    res_query = query.copy()
    spec_fields = {
        "classroom": ["admission_year"],
        "classroom_and_letter": ["admission_year", "classroom_letter"],
    }
    if set(spec_fields.keys()) & set(res_query):
        for num, q in enumerate(res_query):
            if q in spec_fields:
                res_query[num:num+1] = spec_fields[q]
    print(query, res_query)
    for st_id in ids:
        yield session.query(*query).filter_by(id=st_id).first()

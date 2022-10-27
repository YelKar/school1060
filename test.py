from docx import Document
from docx.document import Document as D

from app.database import db
from app.models import Students

wordDoc: D = Document('Списки_классов\\8 Н.docx')
p = wordDoc.paragraphs
print(*[_.text for _ in p[2:-1]], sep="\n")
assert int(input("0/1: ")), ValueError("Отмена")
for par in p[2:-1]:
    st: Students = Students()
    if not par.text:
        continue
    lastname, name, patr, *status = par.text.split()
    if "-" not in status:
        print(lastname, name, patr)
        st.lastname = lastname
        st.name = name
        st.patronymic = patr
        st.admission_year = 2013
        st.classroom_letter = 0
        db.session.add(st)

db.session.commit()

db.session.commit()

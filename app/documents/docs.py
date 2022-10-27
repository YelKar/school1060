from docx2pdf import convert
from docxtpl import DocxTemplate, RichText
from datetime import datetime

from app.constants import year_to_classroom, class_letters


def generate(name: str, *contexts: dict[int or str]):
    doc = DocxTemplate(f"app/documents/templates/{name}.docx")
    for context in contexts:
        for key, val in context.items():
            context[key] = context_var(val)

    doc.render({'context': contexts})
    gen_id = datetime.now().strftime("%d-%m-%y___%H-%M-%S--%f")
    save_route = f"documents/generated/docx/{name}{gen_id}.docx"
    doc.save("app/" + save_route)
    return save_route


def context_var(value: int or str):
    value: str = str(value).replace(" ", "_")

    def formatting(length: int) -> RichText:
        to_add = ("_" * ((length - len(value)) // 2)) \
            if len(value) < length else ""
        result = to_add + value + to_add
        if len(result) < length:
            result += "_"
        return RichText(result, underline=True)

    return formatting


def query2context(query: list):
    now = datetime.now()
    for student in query:
        yield dict(
            fullname=f"{student.lastname} {student.name} {student.patronymic}",
            lastname=student.lastname,
            name=student.name,
            patronymic=student.patronymic,
            birthdate="",
            classroom=f"{year_to_classroom(student.admission_year)}",
            letter=class_letters[student.classroom_letter],
            date=now.strftime("%d.%m.%y"),
            Date=now.strftime("%d.%m.%Y")
        )


genitive_names = {
    "а": "ы",

}
genitive_lastnames = {
    "в": "ва",
    "н": "на",
    "ий": "ого",
    "ой": "ого",
    "ва": "вой",
    "на": "ной",
    "ая": "ой",
    "ок": "ка",
    "а": "ы",
    "ы": ""
}


def genitive(word, **word_type):
    if word_type.get("lastname"):
        ...


def to_pdf(route: str):
    route = "app/" + route
    route_pdf = route.replace(".docx", ".pdf").replace("/docx/", "/pdf/")
    convert(route, route_pdf)
    return route_pdf[4:]


if __name__ == '__main__':
    # generate("Справка об обучении",
    #          dict(fullname="Полное имя", birthdate="28.08.2005", classroom="10", letter="н"),
    #          dict(fullname="П2", birthdate="b2", classroom="10", letter="н"),
    #          dict(fullname="П3", birthdate="b3", classroom="10", letter="н"),
    #          dict(fullname="П4", birthdate="b4", classroom="10", letter="н"),
    #          dict(fullname="П5", birthdate="b5", classroom="10", letter="н"),
    #          dict(fullname="П6", birthdate="b6", classroom="10", letter="н"),
    #          dict(fullname="П7", birthdate="b7", classroom="10", letter="н"),
    #          )
    convert("generated/docx/Справка об обучении23-34-04--092641___06-10-22.docx")


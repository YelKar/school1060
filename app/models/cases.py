from pymorphy2.tagset import OpencorporaTag
from pymorphy2.tagset import _select_grammeme_from


class Case:
    from pymorphy2 import MorphAnalyzer as __Morph
    from pymorphy2.analyzer import Parse as __Parse

    __morph = __Morph()

    def __init__(self, lastname: str, firstname: str, patronymic: str):
        parse = self.__Parse
        self.lastname: parse = sorted(self.__morph.parse(lastname),
                                      key=lambda m: {"Surn"} in m.tag, reverse=True)[0]
        self.firstname: parse = sorted(self.__morph.parse(firstname),
                                       key=lambda m: {"Name"} in m.tag, reverse=True)[0]
        self.patronymic: parse = sorted(self.__morph.parse(patronymic),
                                        key=lambda m: {"Patr"} in m.tag, reverse=True)[0]
        if self.lastname.tag.case == "gent" and self.lastname.tag.gender is not None:
            self.lastname = self.lastname.inflect({"femn", "nomn"}) or self.lastname
        if self.lastname is None:
            print(lastname)

    def __call__(self, case):
        fullname_case = []
        if not self.can_vary():
            return tuple([self.lastname.word.title(),
                          self.firstname.word.title(),
                          self.patronymic.word.title(),
                          False])
        const_lastname = self.lastname.tag.gender == "masc" and self.firstname.tag.gender == "femn"
        if not const_lastname:
            fullname_case.append(self.lastname.inflect({case}).word.title())
        else:
            fullname_case.append(self.lastname.word.title())
        if {"Name"} in self.firstname.tag:
            fullname_case.append(self.firstname.inflect({case}).word.title())
        else:
            fullname_case.append(self.firstname.word.title())
        if {"Patr"} in self.patronymic.tag:
            fullname_case.append(self.patronymic.inflect({case}).word.title())
        else:
            fullname_case.append(self.patronymic.word.title())
        return tuple(fullname_case + [True])

    def can_vary(self):
        if self.patronymic and self.patronymic.tag.gender != self.firstname.tag.gender\
                or self.lastname.tag.case != "nomn":
            return False
        return True


if __name__ == '__main__':
    fullname = Case(*"Сердюкова Агнесса Ивановна".split())
    for case, r_case in [
        ('nomn', 'именительный'),
        ('gent', 'родительный'),
        ('datv', 'дательный'),
        ('accs', 'винительный'),
        ('ablt', 'творительный'),
        ('loct', 'предложный')
    ]:
        print(f"{r_case.title():<15}", *fullname(case))
    print(fullname.lastname.inflect({"gent"}))

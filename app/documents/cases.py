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

        if self.lastname.tag.case == "gent":
            self.lastname = self.lastname.inflect({"femn", "nomn"})

    def __call__(self, case):
        fullname_case = []
        if not self.__can_vary():
            return tuple([self.lastname.word.title(),
                          self.firstname.word.title(),
                          self.patronymic.word.title(),
                          False])
        const_lastname = self.lastname.tag.gender == "masc" and self.firstname.tag.gender == "femn"
        if {"Surn"} in self.lastname.tag and not const_lastname:
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

    def __can_vary(self):
        if self.patronymic.tag.gender != self.firstname.tag.gender:
            return False

if __name__ == '__main__':
    fullname = Case(*"Мкртчян Матвей Александрович".split())
    for case, r_case in [
        ('nomn', 'именительный'),
        ('gent', 'родительный'),
        ('datv', 'дательный'),
        ('accs', 'винительный'),
        ('ablt', 'творительный'),
        ('loct', 'предложный')
    ]:
        print(f"{r_case.title():<15}", *fullname(case))

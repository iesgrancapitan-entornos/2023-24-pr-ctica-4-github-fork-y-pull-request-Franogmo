"""
Goal: A machine that assigns classes alphabetically by surname. It also must be able to split a list
into 3 classes. All of this through lambda functions.

WARNING: THE NAMES MUST BE WRITTEN AS "Surname Name" and must not contain accents.
Non-English characters will probably end up in the last class.

By Fran Ogallas
Start: Last update:
"""
from typeguard import typechecked

# TODO THIS CLASS MUST BE REFINED IN ORDER TO BE ACTUALLY USEFUL.


class AssigningError(ValueError):

    def __init__(self, student):
        super().__init__(f"{student} is not assignable.")


@typechecked
class ClassAssigner:

    def __init__(self, students: list):
        self.__students = students

    @property
    def students(self):
        return self.__students

    def assign(self, student):
        if student < "Ja":
            return "A"
        elif student >= "Ja" and student < "Oa":
            return "B"
        elif student >= "Oa":
            return "C"
        else:
            raise AssigningError(student)

    def list_of_classes(self):
        change = lambda x: self.assign(x)
        return list(map(change, self.__students))

    def split_students(self):
        final_classes = []
        class_a = list(filter(lambda x: self.assign(x) == "A", self.__students))
        final_classes.append(class_a)
        class_b = list(filter(lambda x: self.assign(x) == "B", self.__students))
        final_classes.append(class_b)
        class_c = list(filter(lambda x: self.assign(x) == "C", self.__students))
        final_classes.append(class_c)
        return final_classes

    def format_students_lists(self):
        """
        I know this method should return str's instead of prints, but this is a lambda practice,
        so I don't want to lose time in this part right now.

        :return:
        """
        final_classes = self.split_students()
        print("Class A:")
        for student in final_classes[0]:
            print(student, end=", ")
        print("\nClass B:")
        for student in final_classes[1]:
            print(student, end=", ")
        print("\nClass C:")
        for student in final_classes[2]:
            print(student, end=", ")


def main():
    STUDENTS = ["Mbappe Killian", "Debruyne Kevin", "Dovbyk Artem", "Vandijk Virgil", "Gvardiol Josko",
                "Szoboszlai Dominic", "Hernandez Rodrigo", "Kane Harry", "Leao Rafael", "Sommer Jan",
                "Kimmich Joshua", "Vlahovic Dusan", "Calhanoglu Hakan", "Robertson Andrew", "Barella Niccolo",
                "Dragusin Radu", "Lewandowski Robert", "Kvaratskhelia Kvischa", "Oblak Jan", "Sabitzer Marcel",
                "Soucek Tomas", "Iznajar Pablo", "Oaxaca Luis"]

    generation = ClassAssigner(STUDENTS)
    print(generation.list_of_classes())
    generation.format_students_lists()


if __name__ == "__main__":
    main()


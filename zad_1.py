import statistics

class Student:
    def __init__(self, name: str, marks: list):
        self.name = name
        self.marks = marks

    def is_passed(self) -> bool:
        mean = statistics.mean(self.marks)
        return True if mean >50 else False

student1 = Student('Marek', [50, 40, 100, 20])
student2 = Student('Piotr', [50, 40, 20, 20])

print(student1.is_passed())
print(student2.is_passed())
from zad_2_utils.Book import Book
from zad_2_utils.Employee import Employee
from zad_2_utils.Student import Student


class Order:
    def __init__(
        self,
        employee: Employee,
        student: Student,
        books: list[Book],
        order_date: str,
    ):
        self.order_date = order_date
        self.books = books
        self.student = student
        self.employee = employee

    def __str__(self):
        books_str = "\n ".join(str(b) for b in self.books)

        return f"Order date: {self.order_date}\nEmployee -> {self.employee}\nStudent -> {self.student}\nBooks:\n {books_str}"

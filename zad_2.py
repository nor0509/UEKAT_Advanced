from zad_2_utils.Book import Book
from zad_2_utils.Employee import Employee
from zad_2_utils.Library import Library
from zad_2_utils.Order import Order
from zad_2_utils.Student import Student

l1 = Library("Warsaw", "Main St 10", "00-001", "8-16", "501234567")
l2 = Library("Krakow", "Green St 5", "30-002", "9-17", "692881440")

b1 = Book(l1, "2001", "Adam", "Mickiewicz", 300)
b2 = Book(l1, "1999", "Henryk", "Sienkiewicz", 450)
b3 = Book(l2, "2010", "J.K.", "Rowling", 520)
b4 = Book(l2, "2015", "George", "Martin", 900)
b5 = Book(l1, "2020", "Andrzej", "Sapkowski", 650)

e1 = Employee("Jan", "Kowalski", "2015", "1980", "Warsaw", "Main St 12", "00-001", "735220119")
e2 = Employee("Anna", "Nowak", "2018", "1990", "Krakow", "Hill St 3", "30-003", "884992003")
e3 = Employee("Piotr", "Zielinski", "2020", "1995", "Warsaw", "River St 7", "00-002", "797660540")

s1 = Student("Kamil Adamski", [100, 20, 50])
s2 = Student("Ola Kwiatkowska", [100, 20, 50])
s3 = Student("Marek Nowicki", [100, 20, 50])

o1 = Order(e1, s1, [b1, b2], "2024-01-15")
o2 = Order(e2, s3, [b3, b4, b5], "2024-01-20")

print(o1)
print()
print(o2)

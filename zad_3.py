from zad_3_utils.Flat import Flat
from zad_3_utils.House import House

flat = Flat(area=55, rooms=2, price=350000, address="Warszawa, ul. Przykładowa 10", floor=5)

house = House(area=150, rooms=5, price=950000, address="Kraków, ul. Zielona 5", plot=500)

print(flat)
print(house)

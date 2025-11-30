from zad_3_utils.Property import Property

class Flat(Property):
    def __init__(
            self,
            area: int,
            rooms: int,
            price: float,
            address: str,
            floor: int
    ):
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self):
        return (f"Flat | area: {self.area} m², {self.rooms} rooms, "
                f"{self.price} PLN, address: {self.address}, "
                f"floor: {self.floor}")
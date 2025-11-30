from zad_3_utils.Property import Property


class House(Property):
    def __init__(
            self,
            area: int,
            rooms: int,
            price: float,
            address: str,
            plot: int
    ):
        super().__init__(area, rooms, price, address)
        self.plot = plot
    def __str__(self):
        return (
            f"House | area: {self.area} m², rooms: {self.rooms}, "
            f"price: {self.price} PLN, address: {self.address}, "
            f"plot: {self.plot} m²"
        )
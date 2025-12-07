from typing import Optional

import requests


class Brewery:
    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: str,
        address_1: Optional[str],
        address_2: Optional[str],
        address_3: Optional[str],
        city: Optional[str],
        state_province: Optional[str],
        postal_code: Optional[str],
        country: Optional[str],
        longitude: Optional[float],
        latitude: Optional[float],
        phone: Optional[str],
        website_url: Optional[str],
    ):
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.address_1 = address_1
        self.address_2 = address_2
        self.address_3 = address_3
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.phone = phone
        self.website_url = website_url

    def __str__(self):
        return (
            f"Brewery Details:\n"
            f"ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Type: {self.brewery_type}\n"
            f"Address 1: {self.address_1 or 'N/A'}\n"
            f"Address 2: {self.address_2 or 'N/A'}\n"
            f"Address 3: {self.address_3 or 'N/A'}\n"
            f"City: {self.city or 'N/A'}\n"
            f"State/Province: {self.state_province or 'N/A'}\n"
            f"Postal Code: {self.postal_code or 'N/A'}\n"
            f"Country: {self.country or 'N/A'}\n"
            f"Longitude: {self.longitude if self.longitude is not None else 'N/A'}\n"
            f"Latitude: {self.latitude if self.latitude is not None else 'N/A'}\n"
            f"Phone: {self.phone or 'N/A'}\n"
            f"Website URL: {self.website_url or 'N/A'}\n"
        )


def fetch_breweries() -> list[Brewery]:
    url = "https://api.openbrewerydb.org/v1/breweries"
    params = {"page": 1, "per_page": 20}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        breweries = []
        for b in data:
            brewery = Brewery(
                id=b.get("id"),
                name=b.get("name"),
                brewery_type=b.get("brewery_type"),
                address_1=b.get("address_1"),
                address_2=b.get("address_2"),
                address_3=b.get("address_3"),
                city=b.get("city"),
                state_province=b.get("state_province"),
                postal_code=b.get("postal_code"),
                country=b.get("country"),
                longitude=float(b["longitude"]) if b.get("longitude") else None,
                latitude=float(b["latitude"]) if b.get("latitude") else None,
                phone=b.get("phone"),
                website_url=b.get("website_url"),
            )
            breweries.append(brewery)

        return breweries

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []

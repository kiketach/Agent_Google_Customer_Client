"""Customer entity module."""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

class Address(BaseModel):
    """
    Represents a customer's address.
    """

    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    """
    Represents a product in a customer's purchase history.
    """

    product_id: str
    name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    """
    Represents a customer's purchase.
    """

    date: str
    items: List[Product]
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class CommunicationPreferences(BaseModel):
    """
    Represents a customer's communication preferences.
    """

    email: bool = True
    sms: bool = True
    push_notifications: bool = True
    model_config = ConfigDict(from_attributes=True)


class GardenProfile(BaseModel):
    """
    Represents a customer's garden profile.
    """

    type: str
    size: str
    sun_exposure: str
    soil_type: str
    interests: List[str]
    model_config = ConfigDict(from_attributes=True)


class Customer(BaseModel):
    """
    Represents a customer.
    """

    account_number: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    email: str
    phone_number: str
    customer_start_date: str
    years_as_customer: int
    billing_address: Address
    purchase_history: List[Purchase]
    loyalty_points: int
    preferred_store: str
    communication_preferences: CommunicationPreferences
    garden_profile: GardenProfile
    scheduled_appointments: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Converts the Customer object to a JSON string.

        Returns:
            A JSON string representing the Customer object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_customer(current_customer_id: str) -> Optional["Customer"]:
        """
        Retrieves a customer based on their ID.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            The Customer object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy customer.
        return Customer(
            customer_id=current_customer_id,
            account_number="428765091",
            customer_first_name="Enrique",
            customer_last_name="Abril",
            email="kiketachira@gmail.com",
            phone_number="+57-300-105-7454",
            customer_start_date="2022-0-10",
            years_as_customer=2,
            billing_address=Address(
                street="Calle 35a sur #23a-52", city="Bogota", state="Colombia", zip="12345"
            ),
            purchase_history=[
                Purchase(
                    date="2023-10-05",
                    items=[
                        Product(
                            product_id="zht-ultra-01",
                            name="Zapatilla Ultra (cuero) - Suela negra",
                            quantity=1,
                        )
                    ],
                    total_amount=99_900,
                ),
                Purchase(
                    date="2023-12-22",
                    items=[
                        Product(
                            product_id="zht-copa-02",
                            name="Zapatilla Copa (sintética) - Suela torretin",
                            quantity=2,
                        )
                    ],
                    total_amount=179_800,
                ),
                Purchase(
                    date="2024-03-11",
                    items=[
                        Product(
                            product_id="personalization-001",
                            name="Personalización: Nombre y número bordado",
                            quantity=3,
                        )
                    ],
                    total_amount=15_000,
                )
            ],
            loyalty_points=62,
            preferred_store="Zapatillas Hat Trick - Bogotá (Principal)",
            communication_preferences=CommunicationPreferences(
                email=True, sms=True, push_notifications=True
            ),
            garden_profile=GardenProfile(
                type="jugador_microfutbol",
                size="adulto",
                sun_exposure="indoor",
                soil_type="cemento",
                interests=["futsal", "torneos", "entrenamiento"]
            ),
            scheduled_appointments={
                "factory_visit": {
                    "date": "2025-05-02",
                    "time": "10:30",
                    "location": "Bodega Hat Trick"
                }
            }
        )

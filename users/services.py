import requests
import stripe
from rest_framework import status

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует полученную сумму рублей в доллары"""
    response = requests.get(
        "https://api.currencyapi.com/v3/latest?apikey=cur_live_EXD1STSIhC6qbl9RS82Dg9jaYWu3mN1XfpdIG9VP&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = amount / usd_rate
        return int(usd_price)


def create_stripe_product(product, description):
    """Создает продукт в страйпе"""

    return stripe.Product.create(name=product, description=description)


def create_stripe_price(amount, stripe_product):
    """Создает цену на продукт в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,  # округляет копейки
        product=stripe_product.get("id"),
    )


def create_stripe_session(price):
    """Создает страйп-сессию на оплату"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def change_stripe_session_status(session_id):
    session_result = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session_result.get("payment_status")

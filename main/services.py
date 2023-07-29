import stripe
from config import settings
import requests
from main.models import Payment


def checkout_session(course, user):
    headers = {'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'}
    data = [
        ('amount', course.price),
        ('currency', 'usd'),
    ]
    response = requests.post('https://api.stripe.com/v1/payment_intents', headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f'ошибка : {response.json()["error"]["message"]}')
    return response.json()


def create_payment(course, user):
    Payment.objects.create(
        user=user,
        payed_course=course,
        sum_payed=course.price,
    )

# class StripeApi:
#     headers = {
#         'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}',
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#
#     def create_payment(self):
#
#         data = {
#             'type': 'card',
#             'card[token]': 'tok_visa',
#
#         }
#
#         req = requests.post('https://api.stripe.com/v1/payment_methods', headers=self.headers, data=data)
#
#         return req.json().get('id')
#
#     def create_payment_intent(self, user_data, user):
#
#         amount = user_data.get('sum_payed')
#         currency = user_data.get('currency'),
#         if user_data.get('payed_lesson') is not None:
#             course_or_lesson = user_data.get('payed_lesson')
#         else:
#             course_or_lesson = user_data.get('payed_course')
#
#         data = {
#             'amount': amount,
#             'currency': currency,
#             'metadata[user]': user,
#             'metadata[payed_object]': course_or_lesson,
#             'payment_method': self.create_payment()
#
#         }
#         rq = requests.post('https://api.stripe.com/v1/payment_intents',
#                            headers=self.headers,
#                            data=data)
#         return_data = [rq.json().get('id'), rq.json().get('status')]
#         return return_data
#
#     def confirm_intent(self, stripe_id):
#         # подтверждение платежа
#
#         return_url = 'https://example.com/return-url'
#
#         data = {
#             'payment_method': 'pm_card_visa',
#             'return_url': return_url
#         }
#         rq = requests.post(f'https://api.stripe.com/v1/payment_intents/{stripe_id}/confirm',
#                            headers=self.headers,
#                            data=data)
#         return rq.json().get('status')
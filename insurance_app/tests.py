import unittest
from decimal import Decimal
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Quote, StateConfig
from .serializers import QuoteSerializer
from .pricing import calculate_price

class QuotePricingTests(TestCase):

    def test_quote_1_pricing(self):
        data = {
            'buyer_name': 'John Doe',
            'coverage_type': 'Basic',
            'state': 'California',
            'has_pet': True,
            'coverage': {'flood': True}
        }

        serializer = QuoteSerializer(data=data)
        serializer.is_valid()
        
        quote_instance = Quote(**serializer.validated_data)
        pricing_details = calculate_price(quote_instance)

        self.assertEqual(pricing_details["Monthly Subtotal"], 40.80)
        self.assertEqual(pricing_details["Monthly Taxes"], 0.40)
        self.assertEqual(pricing_details["Monthly Total"], 41.20)

    def test_quote_2_pricing(self):
        data = {
            'buyer_name': 'John Doe',
            'coverage_type': 'Premium',
            'state': 'California',
            'has_pet': True,
            'coverage': {'flood': True}
        }

        serializer = QuoteSerializer(data=data)
        serializer.is_valid()
        
        quote_instance = Quote(**serializer.validated_data)
        pricing_details = calculate_price(quote_instance)

        self.assertEqual(pricing_details["Monthly Subtotal"], 61.20)
        self.assertEqual(pricing_details["Monthly Taxes"], 0.61)
        self.assertEqual(pricing_details["Monthly Total"], 61.81)

    def test_quote_3_pricing(self):
        data = {
            'buyer_name': 'John Doe',
            'coverage_type': 'Premium',
            'state': 'New York',
            'has_pet': True,
            'coverage': {'flood': False}
        }

        serializer = QuoteSerializer(data=data)
        serializer.is_valid()
        
        quote_instance = Quote(**serializer.validated_data)
        pricing_details = calculate_price(quote_instance)

        self.assertEqual(pricing_details["Monthly Subtotal"], 60.00)
        self.assertEqual(pricing_details["Monthly Taxes"], 1.20)
        self.assertEqual(pricing_details["Monthly Total"], 61.20)

    def test_quote_4_pricing(self):
        data = {
            'buyer_name': 'John Doe',
            'coverage_type': 'Basic',
            'state': 'Texas',
            'has_pet': False,
            'coverage': {'flood': True}
        }

        serializer = QuoteSerializer(data=data)
        serializer.is_valid()
        
        quote_instance = Quote(**serializer.validated_data)
        pricing_details = calculate_price(quote_instance)

        self.assertEqual(pricing_details["Monthly Subtotal"], 30.00)
        self.assertEqual(pricing_details["Monthly Taxes"], 0.15)
        self.assertEqual(pricing_details["Monthly Total"], 30.15)


class QuoteTests(APITestCase):
    def test_create_quote_valid_data(self):
        data = {
            'buyer_name': 'John Doe',
            'coverage_type': 'Basic',
            'state': 'California',
            'has_pet': True,
            'coverage': {'flood': True}
        }

        response = self.client.post('/insurance/quote/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        quote = Quote.objects.get(id=response.data['id'])
        self.assertEqual(quote.coverage_type, data['coverage_type'])
        self.assertEqual(quote.state, data['state'])


    def test_create_quote_invalid_data(self):
        data = {
            'coverage_type': 'InvalidType',
            'state': 'InvalidState',
            'has_pet': 'NotBoolean',
            'coverage': {'invalid_key': 'value'}
        }

        response = self.client.post('/insurance/quote/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_quote_valid_id(self):
        quote = Quote.objects.create(coverage_type='Basic', state='California', has_pet=True)
        response = self.client.get(f'/insurance/quote/{quote.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_quote_invalid_id(self):
        response = self.client.get('/insurance/quote/999/')  # Assuming 999 is an invalid ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_data_format(self):
        invalid_data = 'invalid_data'
        response = self.client.post('/insurance/quote/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quote_with_missing_fields(self):
        incomplete_data = {'coverage_type': 'Basic'}
        response = self.client.post('/insurance/quote/', incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()

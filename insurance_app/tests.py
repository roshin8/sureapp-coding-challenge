import unittest
from decimal import Decimal
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase
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

if __name__ == '__main__':
    unittest.main()

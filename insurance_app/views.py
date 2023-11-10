from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quote
from .serializers import QuoteSerializer
from .pricing import calculate_price
import json

@api_view(['GET'])
def get_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    serializer = QuoteSerializer(quote)
    return Response(serializer.data)

@api_view(['POST'])
def create_quote(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        serializer = QuoteSerializer(data=data)
        if serializer.is_valid():
            quote = serializer.save()

            # Calculate the price
            pricing_details = calculate_price(quote)

            # Save pricing details in the Quote model
            quote.pricing = pricing_details
            quote.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from typing import Union, Dict, Any
from django.http import HttpRequest
from .models import Quote
from .serializers import QuoteSerializer
from .pricing import calculate_price
import json

@api_view(['GET'])
def get_quote(request: HttpRequest, quote_id: int) -> Response:
    quote = get_object_or_404(Quote, id=quote_id)
    serializer = QuoteSerializer(quote)
    return Response(serializer.data)


@api_view(['POST'])
def create_quote(request: HttpRequest) -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = QuoteSerializer(data=data)
    if not serializer.is_valid():
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        quote = Quote(**serializer.validated_data)

        # Calculate the price
        pricing_details = calculate_price(quote)

        # Save pricing details in the Quote model
        quote.pricing = pricing_details
        quote.save()

        return Response(QuoteSerializer(quote).data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

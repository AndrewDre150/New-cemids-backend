from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import DonationSerializer
from .models import Donation

class DonationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing donations.
    """
    serializer_class = DonationSerializer
    queryset = Donation.objects.all()

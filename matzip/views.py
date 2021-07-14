from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MatzipSerializer
from .models import Matzip
from rest_framework import filters


class MatzipViewSet(viewsets.ModelViewSet):
    queryset = Matzip.objects.all()
    serializer_class = MatzipSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=keyword']

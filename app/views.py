from django.shortcuts import redirect
from rest_framework import filters, viewsets

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


def index_view(request):
    redirect("products")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["title", "description"]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by("id")
    serializer_class = StockSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["products__title", "products__description"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(
                products__title__icontains=search_query
            ) | queryset.filter(products__description__icontains=search_query)
        return queryset

from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        exclude = ["stock"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = ProductSerializer(instance.product).data
        representation["product"] = product_representation
        return representation


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        positions_data = validated_data.pop("positions")
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop("positions")
        stock = super().update(instance, validated_data)
        stock.positions.delete()
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

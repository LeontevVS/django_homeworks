from logistic.models import Stock, Product, StockProduct

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        self.create_positions(positions, stock)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        self.create_positions(positions, stock)
        return stock
    
    def create_positions(self, positions, stock):
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)

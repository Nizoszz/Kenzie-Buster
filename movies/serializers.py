from rest_framework import serializers
from .models import Movie, Rating, MovieOrder
from datetime import datetime


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(choices=Rating.choices, default=Rating.G)
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)
    

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    title = serializers.CharField(source="movie.title", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    buyed_by = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
        
    # def update(self, instance: MovieOrder, validated_data: dict) -> MovieOrder:
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()

    #     return instance

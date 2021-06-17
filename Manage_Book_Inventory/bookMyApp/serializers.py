from rest_framework import serializers

from .models import Books

# class UserSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
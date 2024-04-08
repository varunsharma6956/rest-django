from rest_framework import serializers
from myapp.models import *



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Ensure 'fields' is used, not 'field'
    
    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({"age": "Age cannot be less than 18"})
        
        # This will check if there are any digits in the name and raise a ValidationError
        if any(char.isdigit() for char in data.get('name', '')):
            raise serializers.ValidationError({"name": "Name cannot contain numbers"})
        
        # This will check if the entire name is numeric
        if data.get('name', '').replace('-', '').isdigit():
            raise serializers.ValidationError({"name": "Name cannot be fully numeric"})
        
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        #depth = 1

        
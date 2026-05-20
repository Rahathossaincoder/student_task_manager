from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'timezone', 'week_start_day', 'password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create user with hashed password"""
        user = User.objects.create_user(**validated_data)
        return user
    
    '''
    ** means "unpack dictionary as keyword arguments"
    validated_data = {
    'username': 'testuser',
    'email': 'test@test.com',
    'password': 'securepass123',
    'timezone': 'UTC',
    'week_start_day': 'monday'
}

    # WITHOUT **
    User.objects.create_user(validated_data)
    # ❌ WRONG - passes dictionary as single argument

    # WITH **
    User.objects.create_user(**validated_data)
    # ✅ CORRECT - unpacks to:
    # User.objects.create_user(
    #     username='testuser',
    #     email='test@test.com', 
    #     password='securepass123',
    #     timezone='UTC',
    #     week_start_day='monday'
    # )
    '''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserSignUpSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        max_length=17,
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({"phone": "Phone number is already in use."})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserSignInSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(
                request=self.context.get('request'),
                username=phone,  # Using phone as username
                password=password
            )
            if user is None:
                raise serializers.ValidationError("Invalid phone number or password.")
        else:
            raise serializers.ValidationError("Must include 'phone' and 'password'.", code='authorization')
        attrs['user'] = user 

        return attrs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .models import User
import random

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

OTP_EXPIRY = 300  # 5 minutes
OTP_RATE_LIMIT = 60  # 1 minute

def generate_otp():
    return str(random.randint(100000, 999999))

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        last_sent = cache.get(f"{phone}_last_sent")
        now = timezone.now().timestamp()
        if last_sent and now - last_sent < OTP_RATE_LIMIT:
            return Response({"error": "OTP already sent. Please wait."}, status=429)

        otp = generate_otp()
        cache.set(f"otp_{phone}", otp, timeout=OTP_EXPIRY)
        cache.set(f"{phone}_last_sent", now, timeout=OTP_RATE_LIMIT)

        # Replace with real SMS gateway
        print(f"Sending OTP {otp} to {phone}")

        return Response({"message": "OTP sent successfully."}, status=200)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        cached_otp = cache.get(f"otp_{phone}")
        if cached_otp != otp:
            return Response({"error": "Invalid or expired OTP."}, status=400)

        user, created = User.objects.get_or_create(phone=phone)
        refresh = RefreshToken.for_user(user)

        cache.delete(f"otp_{phone}")  # clean up

        response = Response({
            "message": "Login successful.",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=200)

        response.set_cookie(
            key='access',
            value=str(refresh.access_token),
            httponly=True,       # 👈 So JavaScript can't read it
            secure=True,         # 👈 Only over HTTPS in production
            samesite='Lax',      # 👈 Or 'Strict' or 'None' as needed
            max_age=3600,
        )
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    return Response({
        'phone': user.phone,  # Assuming user has a 'phone' field
        # Add other user fields as needed
    })

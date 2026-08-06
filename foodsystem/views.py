from wsgiref import headers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db.models import Sum, F
from django.core.mail import send_mail
from django.urls import reverse
from datetime import timedelta
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FoodItem
from .models import Recipe
from .serializers import FoodItemSerializer
from .serializers import RecipeSerializer
from .serializers import UserSerializer
import traceback
import requests
import requests
class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return FoodItem.objects.filter(
            user=self.request.user
        )
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        print("Current user:", self.request.user)
        print("Authenticated:", self.request.user.is_authenticated)

        return Recipe.objects.filter(
            user=self.request.user
        ).order_by("-id")
    def perform_create(self, serializer):
        recipe = serializer.save(
            user=self.request.user
        )
        print("Recipe created:")
        print("ID:", recipe.id)
        print("Name:", recipe.name)
        print("User:", recipe.user)
        
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username_or_email = request.data.get("username")
    password = request.data.get("password")

    if "@" in username_or_email:
        user_obj = User.objects.filter(email=username_or_email).first()
        if not user_obj:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        username = user_obj.username
    else:
        username = username_or_email

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),

        "username": user.username,
        "email": user.email
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    print("Authenticated:", request.user.is_authenticated)
    print("User:", request.user)
    total_items = FoodItem.objects.filter(
        user=request.user
    ).count()
    expiring_soon = FoodItem.objects.filter(
        user=request.user,
        expiry_date__lte=timezone.now().date() + timedelta(days=3),
        expiry_date__gte=timezone.now().date()
    ).count()
    expired = FoodItem.objects.filter(
        user=request.user,
        expiry_date__lt=timezone.now().date()
    ).count()
    return Response({
        "total_items": total_items,
        "expiring_soon": expiring_soon,
        "expired": expired
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expiry_alerts(request):
    foods = FoodItem.objects.filter(
        user=request.user
    )
    today = timezone.now().date()
    alerts = []
    for food in foods:
        if food.expiry_date < today:
            status = "Expired"
        elif food.expiry_date <= today + timedelta(days=3):
            status = "Expiring Soon"
        else:
            continue
        alerts.append({
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "quantity": food.quantity,
            "unit": food.unit,
            "expiry_date": food.expiry_date,
            "status": status
        })
    return Response(alerts)

@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    try:
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "No account found with that email."},
                status=404,
            )

        token = default_token_generator.make_token(user)
        reset_link = (
            f"https://smart-food-frontend-xi.vercel.app/reset-password/"
            f"{user.id}/{token}"
        )

        html_message = f"""
        <p>Hello {user.username},</p>
        <p>Click the link below to reset your password.</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you did not request this, ignore this email.</p>
        """

        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        }

        payload = {
            "sender": {
                "name": "Smart Food",
                "email": "glorianushka@gmail.com",
            },
            "to": [{"email": user.email}],
            "subject": "Reset your Smart Food password",
            "htmlContent": html_message,
        }

        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers=headers,
            timeout=15,
        )

        if response.status_code >= 400:
            print(response.status_code)
            print(response.text)
            return Response(
                {"error": "Failed to send email."},
                status=500,
            )

        return Response({"message": "Password reset link sent successfully."})

    except User.DoesNotExist:
        return Response(
            {"error": "No account found with that email."},
            status=404,
        )
    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):

    if request.method == "GET":
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_report(request):

    foods = FoodItem.objects.filter(user=request.user)

    return Response({
        "foods": FoodItemSerializer(
            foods,
            many=True
        ).data
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def waste_report(request):

    today = timezone.now().date()

    foods = FoodItem.objects.filter(user=request.user)

    expired = foods.filter(
        expiry_date__lt=today
    ).count()

    used = foods.filter(
        is_used=True
    ).count()

    money_saved = foods.filter(
        is_used=True,
        used_date__isnull=False,
        used_date__lte=F("expiry_date")
    ).aggregate(
        total=Sum("price")
    )["total"] or 0

    return Response({

        "total_items": foods.count(),

        "items_used": used,

        "items_wasted": expired,

        "money_saved": money_saved,

    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reports(request):

    today = timezone.now().date()

    foods = FoodItem.objects.filter(user=request.user)

    total_items = foods.count()

    expired_items = foods.filter(
        expiry_date__lt=today
    )

    expiring_soon = foods.filter(
        expiry_date__gte=today,
        expiry_date__lte=today + timedelta(days=3)
    )

    items_wasted = expired_items.count()

    items_used = foods.filter(
    is_used=True,
    used_date__isnull=False
).count()

    waste_reduction = 0

    if total_items > 0:
        waste_reduction = round(
            (items_used / total_items) * 100
        )

    money_saved = foods.filter(
    is_used=True,
    used_date__isnull=False,
    used_date__lte=F("expiry_date")
).aggregate(
    total=Sum("price")
)["total"] or 0
    
    weeks = []

    for i in range(3, -1, -1):

            start = today - timedelta(days=(i + 1) * 7 - 1)
            end = today - timedelta(days=i * 7)

            used = foods.filter(
                is_used=True,
                used_date__gte=start,
                used_date__lt=end
            ).count()

            wasted = foods.filter(
               expiry_date__range=[start, end],
               is_used=False
            ).count()

            weeks.append({
                "week": f"Week {4 - i}",
                "wasted": wasted,
                "used": used,
            })
           

    return Response({

        "total_items": total_items,

        "expired": items_wasted,

        "expiring_soon": expiring_soon.count(),

        "items_used": items_used,

        "items_wasted": items_wasted,

        "money_saved": money_saved,

        "waste_reduction": waste_reduction,

        "foods": FoodItemSerializer(
            foods,
            many=True
        ).data,

        "weekly_trend": weeks,
    })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_food_used(request, pk):

    try:
        food = FoodItem.objects.get(
            id=pk,
            user=request.user
        )

    except FoodItem.DoesNotExist:
        return Response(
            {"error": "Food item not found"},
            status=404
        )

    food.is_used = True
    food.used_date = timezone.now().date()
    food.save()

    return Response({
        "message": "Food marked as used."
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response({"error": "Invalid user."}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired link."}, status=400)

    user.set_password(password)
    user.save()

    return Response({"message": "Password updated successfully."})
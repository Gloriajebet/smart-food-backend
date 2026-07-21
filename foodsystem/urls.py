from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import FoodItemViewSet, RecipeViewSet, dashboard_summary, expiry_alerts
from .views import register_user
from .views import login_user 
from .views import dashboard_summary
from .views import forgot_password
from .views import profile
from .views import reports
from .views import mark_food_used
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import mark_food_used

router = DefaultRouter()
router.register(
    r'fooditems', 
    FoodItemViewSet,
    basename='fooditems'
    )

router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)

urlpatterns = [
    path('', include(router.urls)),
    path("dashboard/", dashboard_summary),
    path("register/", register_user),
    path("login/", login_user),
    path("alerts/", expiry_alerts),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("forgot-password/", forgot_password),
    path("profile/", profile),
    path(
    "reports/",
    reports,
    name="reports",
),
    path(
    "fooditems/<int:pk>/mark-used/",
    mark_food_used,
    name="mark-food-used"
),

]
from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FoodItem


class ReportsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        foods = FoodItem.objects.filter(
            user=request.user
        )

        period = request.GET.get("period", "month")

        today = timezone.now().date()

        if period == "today":
         foods = foods.filter(
        purchase_date=today
 )

        elif period == "week":
         foods = foods.filter(
        purchase_date__gte=today - timedelta(days=7)
    )

        else:
         foods = foods.filter(
        purchase_date__gte=today - timedelta(days=30)
    )

        used_before_expiry = foods.filter(
            is_used=True,
            used_date__lte=F("expiry_date")
        ).count()

        today = timezone.now().date()

        expired = foods.filter(
            expiry_date__lt=today,
            is_used=False
        ).count()

        total = used_before_expiry + expired

        if total == 0:
            waste_reduction = 0
        else:
            waste_reduction = round(
                (used_before_expiry / total) * 100
            )

        money_saved = foods.filter(
            is_used=True,
            used_date__lte=F("expiry_date")
        ).aggregate(
            total=Sum("price")
        )["total"] or 0

        weeks = []

        for i in range(4):

            end = today - timedelta(days=i * 7)

            start = end - timedelta(days=6)

            wasted = foods.filter(
                expiry_date__range=[start, end],
                is_used=False
            ).count()

            weeks.append({
                "week": f"Week {4 - i}",
                "wasted": wasted
            })

        weeks.reverse()

        return Response({
            "waste_reduction": waste_reduction,
            "money_saved": money_saved,
            "items_used": used_before_expiry,
            "items_wasted": expired,
            "weekly_trend": weeks
        })
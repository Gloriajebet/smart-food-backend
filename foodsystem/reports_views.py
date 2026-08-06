from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FoodItem
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, red, green, orange
from django.http import HttpResponse


class ReportsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        foods = FoodItem.objects.filter(
            user=request.user
        )

        period = request.GET.get("period", "month")

        today = timezone.now().date()

        if period == "today":
         report_foods = foods.filter(
        purchase_date=today
 )

        elif period == "week":
         report_foods = foods.filter(
        purchase_date__gte=today - timedelta(days=7)
    )

        else:
         report_foods = foods.filter(
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
            start = today - timedelta(days=6)

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
            "total_items": foods.count(),
            "expiring_soon": foods.filter(
        expiry_date__gte=today,
        expiry_date__lte=today + timedelta(days=3)
    ).count(),
            "expired": expired,
            "waste_reduction": waste_reduction,
            "money_saved": money_saved,
            "items_used": used_before_expiry,
            "items_wasted": expired,
            "weekly_trend": weeks,
            "foods": [
        {
            "name": food.name,
            "quantity": food.quantity,
            "unit": food.unit,
            "expiry_date": food.expiry_date,
        }
        for food in foods
    ]
})
class InventoryReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        foods = FoodItem.objects.filter(user=request.user)

        today = timezone.now().date()

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="Inventory_Report.pdf"'

        pdf = canvas.Canvas(response)

        greenColor = HexColor("#2c9635")

        # Header
        pdf.setFont("Helvetica-Bold", 22)
        pdf.setFillColor(greenColor)
        pdf.drawString(40, 810, "Smart Food System")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor("black")
        pdf.drawString(40, 785, "Inventory Report")

        pdf.setStrokeColor(greenColor)
        pdf.line(40, 775, 560, 775)

        pdf.setFont("Helvetica", 11)
        pdf.drawString(
            40,
            755,
            f"Generated: {timezone.now().strftime('%d %b %Y %I:%M %p')}"
        )

        pdf.drawString(40,730,f"Total Items: {foods.count()}")

        pdf.drawString(
            40,
            710,
            f"Expiring Soon: {foods.filter(expiry_date__lte=today+timedelta(days=3), expiry_date__gte=today).count()}"
        )

        pdf.drawString(
            40,
            690,
            f"Expired Items: {foods.filter(expiry_date__lt=today,is_used=False).count()}"
        )

        pdf.line(40,675,560,675)

        pdf.setFont("Helvetica-Bold",14)
        pdf.drawString(40,650,"Inventory Details")

        y = 625

        for food in foods:

            if y < 80:
                pdf.showPage()
                y = 800

            expiry = food.expiry_date

            if expiry < today:

                pdf.setFillColor(red)
                status = "Expired"

            elif expiry <= today + timedelta(days=3):

                pdf.setFillColor(orange)
                status = "Expiring Soon"

            else:

                pdf.setFillColor(green)
                status = "Fresh"

            pdf.setFont("Helvetica-Bold",12)
            pdf.drawString(50,y,food.name)

            pdf.setFillColor("black")

            pdf.setFont("Helvetica",11)
            pdf.drawString(70,y-18,f"Quantity: {food.quantity} {food.unit}")

            pdf.drawString(70,y-34,f"Expiry Date: {food.expiry_date}")

            pdf.drawString(70,y-50,f"Status: {status}")

            pdf.setStrokeColor(HexColor("#DDDDDD"))
            pdf.line(50,y-60,550,y-60)

            y -= 85

        pdf.save()

        return response
class WasteReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        foods = FoodItem.objects.filter(user=request.user)

        today = timezone.now().date()

        expired = foods.filter(
            expiry_date__lt=today,
            is_used=False
        ).count()

        used = foods.filter(
            is_used=True,
            used_date__lte=F("expiry_date")
        ).count()

        saved = foods.filter(
            is_used=True,
            used_date__lte=F("expiry_date")
        ).aggregate(total=Sum("price"))["total"] or 0

        total = used + expired

        if total == 0:
            reduction = 0
        else:
            reduction = round((used / total) * 100)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"]='attachment; filename="Waste_Report.pdf"'

        pdf = canvas.Canvas(response)

        greenColor = HexColor("#2c9635")

        pdf.setFont("Helvetica-Bold",22)
        pdf.setFillColor(greenColor)
        pdf.drawString(40,810,"Smart Food System")

        pdf.setFont("Helvetica-Bold",16)
        pdf.setFillColor("black")
        pdf.drawString(40,785,"Waste Analysis Report")

        pdf.setStrokeColor(greenColor)
        pdf.line(40,775,560,775)

        pdf.setFont("Helvetica",11)
        pdf.drawString(
            40,
            755,
            f"Generated: {timezone.now().strftime('%d %b %Y %I:%M %p')}"
        )

        pdf.setFont("Helvetica-Bold",15)
        pdf.drawString(40,720,"Performance Summary")

        pdf.setFont("Helvetica",12)

        pdf.drawString(60,690,f"Items Used On Time : {used}")

        pdf.drawString(60,665,f"Items Wasted : {expired}")

        pdf.drawString(60,640,f"Money Saved : KSh {saved:,.2f}")

        pdf.drawString(60,615,f"Waste Reduction Score : {reduction}%")

        pdf.line(40,595,560,595)

        pdf.setFont("Helvetica-Bold",14)
        pdf.drawString(40,565,"System Recommendation")

        pdf.setFont("Helvetica",11)

        if reduction >= 80:

            recommendation = (
                "Excellent! Continue following your current food management habits."
            )

        elif reduction >= 50:

            recommendation = (
                "Good progress. Consider using more foods before expiry."
            )

        else:

            recommendation = (
                "High food waste detected. Prioritize foods nearing expiry."
            )

        pdf.drawString(50,535,recommendation)

        pdf.line(40,500,560,500)

        pdf.setFont("Helvetica-Oblique",10)

        pdf.drawString(
            40,
            475,
            "Generated automatically by Smart Food System"
        )

        pdf.save()

        return response
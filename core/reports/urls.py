from django.urls import path

from app.core.reports.views import ReportVentaView

urlpatterns = [
    path('venta/', ReportVentaView.as_view(), name='report_venta')
]
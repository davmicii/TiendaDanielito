from django.urls import path

from core.reports.views import ReportVentaView, ReportPagoView, OptionsView

urlpatterns = [
    path('todos/', OptionsView.as_view(), name='all_reports'),
    path('venta/', ReportVentaView.as_view(), name='report_venta'),
    path('pago/', ReportPagoView.as_view(), name='report_pago')
]
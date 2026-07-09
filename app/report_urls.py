# from django.urls import path
# from app import report_views

# urlpatterns = [
#     path('', report_views.reports_list, name='reports'),
# ]

from django.urls import path
from app import report_views

urlpatterns = [
    path('', report_views.report_views, name='reports'),
    path('chart-data/', report_views.chart_data, name='chart_data'),
    path('export-excel/', report_views.export_excel, name='export_excel'),
    path('export-pdf/', report_views.export_pdf, name='export_pdf'),
]
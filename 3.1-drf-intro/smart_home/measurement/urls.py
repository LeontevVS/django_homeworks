from django.urls import path
from measurement.views import SensorView, SensorListView, MeasurementView

urlpatterns = [
    path('sensors/<pk>/', SensorView.as_view()),
    path('sensors/', SensorListView.as_view()),
    path('measurements/', MeasurementView.as_view())
]

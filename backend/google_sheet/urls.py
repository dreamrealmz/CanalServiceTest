from django.urls import path
from .views import SheetRowScheduleAPIView
from .viewsets import SheetRowViewSet

urlpatterns = [
    path(
        'api/v1/SheetRowViewSet/',
        SheetRowViewSet.as_view(
            {
                'get': 'list',
            }
        )
    ),
    path('api/v1/SheetRowScheduleAPIView/',
         SheetRowScheduleAPIView.as_view()
         ),
]

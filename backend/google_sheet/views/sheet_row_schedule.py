from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import SheetRow


class SheetRowScheduleAPIView(APIView):
    authentication_classes = []

    def get(self, request):
        response = {
            'sheets': SheetRow.objects.all().order_by('delivery_time').values('cost_in_rur', 'delivery_time')
        }
        return Response(response, status=status.HTTP_200_OK)

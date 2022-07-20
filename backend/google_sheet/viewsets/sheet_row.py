from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers import SheetRowSerializer
from ..models import SheetRow


class SheetRowPagination(PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.GET.get('page_size', 6)
        return page_size


class SheetRowViewSet(viewsets.ModelViewSet):
    queryset = SheetRow.objects.all()
    pagination_class = SheetRowPagination
    serializer_class = SheetRowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    order_by = ['delivery_time']

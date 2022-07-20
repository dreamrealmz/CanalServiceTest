from rest_framework import serializers
from ..models import SheetRow


class SheetRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetRow
        fields = '__all__'

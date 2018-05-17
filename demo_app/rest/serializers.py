from rest_framework import serializers

from ..models import Document


class DocumentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Document
        fields = ('text',)

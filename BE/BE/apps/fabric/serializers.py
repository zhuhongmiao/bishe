from rest_framework import serializers
from .models import Fabric


class FabricSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    pattern = serializers.SerializerMethodField()

    class Meta:
        model = Fabric
        fields = '__all__'

    def get_title(self, obj):
        return obj.translate_text(obj.title)

    def get_category_name(self, obj):
        return obj.translate_text(obj.category_name)

    def get_country(self, obj):
        return obj.translate_text(obj.country)

    def get_pattern(self, obj):
        return obj.translate_text(obj.pattern)

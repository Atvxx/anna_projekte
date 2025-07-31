from rest_framework import serializers
from .models import Bewerbung, Kontaktanfrage

class BewerbungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bewerbung
        fields = '__all__'



class KontaktanfrageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontaktanfrage
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth  import get_user_model

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['username','date_joined','telegram_id']
    
class TelegramConnectSerializer(serializers.Serializer):
  token = serializers.CharField()
  telegram_id = serializers.IntegerField()
  
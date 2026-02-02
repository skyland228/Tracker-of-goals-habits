from rest_framework import serializers
from users.models import get_user_model

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['username','date_joined']
    
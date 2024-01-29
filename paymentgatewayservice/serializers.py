from rest_framework import serializers
from .models import USSDRequest, USSDJobRequest, Jobs, Wallet, Transactions, Users  # Adjust the import according to your project structure

# User Serializer
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

# USSDRequest Serializer
class USSDRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSDRequest
        fields = '__all__'

# USSDJobRequest Serializer
class USSDJobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSDJobRequest
        fields = '__all__'

# Jobs Serializer
class JobsSerializer(serializers.ModelSerializer):
    client = UsersSerializer(read_only=True)
    worker = UsersSerializer(read_only=True)
    
    class Meta:
        model = Jobs
        fields = '__all__'

# Wallet Serializer
class WalletSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'

# Transactions Serializer
class TransactionsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Transactions
        fields = '__all__'

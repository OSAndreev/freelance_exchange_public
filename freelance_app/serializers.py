from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserDataSerializer(serializers.ModelSerializer):
    #role = serializers.IntegerField(source=UserData.role)

    class Meta:
        model = UserData
        fields = ['id', 'first_name', 'last_name', 'mail']


class FreelancerSerializer(serializers.ModelSerializer):
    user_id = UserDataSerializer()
    #role = serializers.IntegerField(source=UserData.role)

    class Meta:
        model = Freelancer
        fields = '__all__'


class CreateFreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user_id = UserDataSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    performer = FreelancerSerializer()

    #degree_to_company = serializers.IntegerField(source=Order.degree_to_company)
    #degree_to_performer = serializers.IntegerField(source=Order.degree_to_performer)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    #degree_to_company = serializers.IntegerField(source=Order.degree_to_company)
    #degree_to_performer = serializers.IntegerField(source=Order.degree_to_performer)

    class Meta:
        model = Order
        fields = '__all__'


class OffersSerializer(serializers.ModelSerializer):
    details = OrderSerializer()
    freelance_variety = FreelancerSerializer()

    class Meta:
        model = Offers
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DealHistorySerializer(serializers.ModelSerializer):
    from_who = UserDataSerializer()
    to_who = UserDataSerializer()

    class Meta:
        model = DealHistory
        fields = '__all__'


class CreateDealHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DealHistory
        fields = '__all__'


class BalanceOperationsSerializer(serializers.ModelSerializer):
    user_id = UserDataSerializer()

    class Meta:
        model = BalanceOperations
        fields = '__all__'


class CreateBalanceOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceOperations
        fields = '__all__'

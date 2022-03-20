
from rest_framework import serializers
from database.models import *
from .utils import *

class ProductSerializer(serializers.ModelSerializer):

    

    class Meta:
        model  = Product
        fields =  ('__all__')

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)  

       



class OrderSerializer(serializers.ModelSerializer):
    
    get_total     = serializers.ReadOnlyField()
    get_total_usd = serializers.ReadOnlyField()

    class Meta:
        model  = Order
        fields =  ('id','date_time','get_total','get_total_usd')

    






class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model  = OrderDetail
        fields =  ('__all__')

      

    
     

    

          

        

from wsgiref import validate
from rest_framework import serializers
from rest_framework import status
from database.models import *
from .utils import *

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class ProductSerializer(serializers.ModelSerializer):

    name  = serializers.CharField(validators=[required])
    price = serializers.FloatField(validators=[required])
    stock = serializers.IntegerField(validators=[required])

    class Meta:
        model  = Product
        fields =  ('__all__')


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


    def validate(self, attrs):

        order    = attrs['order']
        product  = attrs['product']
        cuantity = attrs['cuantity']


        # Verifica que la cantidad sea un numero valido.
        if int(cuantity) == 0 or int(cuantity) < 0 or cuantity == '':
            raise serializers.ValidationError({'cuantity':'Informacion Invalida.'})

        
        # Verifica que no se repitan productos en el mismo pedido.
        if OrderDetail.objects.filter(order=order,product=product).exists():
            data   = {'Message':'Ya se solicito este producto en la orden.'}            
            raise serializers.ValidationError(data)    

        return super().validate(attrs) 

        

    


      

    
     

    

          

        
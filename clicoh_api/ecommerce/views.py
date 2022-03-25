from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from database.models import *

from .serializers import *
from .utils import *

class BaseModelViewSet(ModelViewSet):    
    
    permission_classes     = [IsAuthenticated]

class ProductView(BaseModelViewSet):
    
    serializer_class   = ProductSerializer
    queryset           = Product.objects.all()

    def list(self, request):

        queryset   = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    

class OrderView(BaseModelViewSet):   

    serializer_class   = OrderSerializer
    queryset           = Order.objects.all()

    def list(self, request):

        queryset   = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):  

        instance = self.get_object()   

        # Se retornara la cantidad solicitada al stock disponible de lo productos
        OrderTools.return_stock(instance) 

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    

    
   


class OrderDetailView(BaseModelViewSet):

    serializer_class   = OrderDetailSerializer
    queryset           = OrderDetail.objects.all()

    def list(self, request):

        queryset   = OrderDetail.objects.all()
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data) 


    def create(self, validated_data): 

        data    = validated_data.data
        
        # Verifica si hay stock disponible.
        stock_control = OrderDetailsTools.stock_control(data) 

        if stock_control.status_code == 404: return stock_control 
        if stock_control.status_code == 400: return stock_control
        if stock_control.status_code == 200:                     

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED, ) 
        
   
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        data     = request.data 

        # Verifica que la cantidad sea un numero valido.
        # OrderDetailsTools.validate_cuantity(data)
        
        update_product = OrderDetailsTools.update_orderdetails(instance,data)

        # Verifica si hay stock disponible.
        if update_product.status_code == 404: return update_product 
        if update_product.status_code == 400: return update_product        
        
        instance.cuantity =  data['cuantity']
        instance.order    =  Order.objects.get(id=data['order'])
        instance.product  =  Product.objects.get(id=data['product'])
        instance.save()

        serializer = OrderDetailSerializer(instance)

        return Response(serializer.data,status=status.HTTP_200_OK)
        

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()  

        # Se retornara la cantidad solicitada al stock disponible del producto
        OrderDetailsTools.return_stock(instance)    

        self.perform_destroy(instance)

        return Response(status=status.HTTP_200_OK)


    

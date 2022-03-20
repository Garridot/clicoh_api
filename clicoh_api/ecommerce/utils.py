from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from database.models import Product,OrderDetail



class OrderTools:

    def return_stock(instance):

        # Se retornara la cantidad solicitada al stock disponible de lo productos

        products = OrderDetail.objects.filter(order=instance)        

        for i in products:
            product = Product.objects.get(name=i.product)                      
            product.stock=product.stock + int(i.cuantity)
            product.save()



class OrderDetailsTools:

    def validate_cuantity(data):

        # Verifica que la cantidad sea un numero valido.

        if int(data['cuantity']) == 0 or int(data['cuantity']) < 0 or data['cuantity'] == '':

            raise serializers.ValidationError({'cuantity':'Informacion Invalida.'})


    def product_in_order(data):

        # Verifica que no se repitan productos en el mismo pedido.

        order   = data['order']
        product = data['product']

        if OrderDetail.objects.filter(order=order,product=product).exists():

            data   = 'Ya se solicito este producto en la orden.'            
            return Response(data, status = status.HTTP_400_BAD_REQUEST)

        else: return Response(status.HTTP_200_OK)


    def stock_control(data):

        # Verifica si hay stock disponible.

        product  = Product.objects.get(id=data['product'])        
        stock    = product.stock 
        cuantity = int(data['cuantity'])    
        
        if stock == 0: 
            data  = 'Producto agotado.' 
            return Response(data,status = status.HTTP_404_NOT_FOUND)

        if stock < cuantity: 
            data = f'{product.name},stock disponible: {stock}'
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

        else:        
            product.stock = stock - cuantity 
            product.save()
            return Response(status.HTTP_200_OK)


    def update_orderdetails(instance,data): 
       
        # Se retornara la cantidad solicitada al stock disponible del producto. 
        # Una vez hecho esto, se enviara la nueva cantidad solicitada.
          

        OrderDetailsTools.return_stock(instance) 

        # Verifica si se solicito el mismo producto.
        if int(instance.product.id) != int(data['product']):  
            
            product_in_order = OrderDetailsTools.product_in_order(data)

            if product_in_order.status_code == 400 :
                 return product_in_order

            else : 
                return OrderDetailsTools.stock_control({'product':data['product'],'cuantity':data['cuantity']})  
        
        else:        
            return OrderDetailsTools.stock_control({'product':instance.product.id,'cuantity':data['cuantity']})         


    def return_stock(instance):

        # Se retornara la cantidad solicitada al stock disponible del producto. 
        product = Product.objects.get(name=instance.product)
        product.stock = product.stock + int(instance.cuantity)
        product.save()           





                

            
                








  

              
                

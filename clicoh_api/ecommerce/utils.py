from rest_framework.response import Response
from rest_framework import status
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

        n_product  = data['product']
        n_cuantity = data['cuantity']
       
        # Se retornara la cantidad solicitada al stock disponible del producto
        
        OrderDetailsTools.return_stock(instance) 

        # Una vez hecho esto, se enviara la nueva cantidad solicitada.

        # Verifica si se solicito el mismo producto.
        if int(instance.product.id) != int(n_product):              
            
            return OrderDetailsTools.stock_control({'product':n_product,'cuantity':n_cuantity})  
        
        else:        
            return OrderDetailsTools.stock_control({'product':instance.product.id,'cuantity':n_cuantity})         


    def return_stock(instance):

        # Se retornara la cantidad solicitada al stock disponible del producto. 
        product = Product.objects.get(name=instance.product)
        product.stock = product.stock + int(instance.cuantity)
        product.save()           





                

            
                








  

              
                

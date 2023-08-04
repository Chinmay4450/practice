from .models import Brand,Category,Product,Productsize,Cart,Order,Banner,Notification,ContactUs
from .serializers import brandSerializer,categorySerializer, orderhistorySerializer,productSerializer,orderSerializer,productsizeSerializer,CartSerializer,outofstockkSerializer,allorderSerializer,orderrrSerializer,BannerSerializer,salesSerializer,NotificationSerializer,ContactUsSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db.models import Sum
import datetime
import json
from jamali.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import format_html
import datetime
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from registration.models import UserRegistration
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
now = datetime.datetime.now()


class brandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = brandSerializer
    permission_classes = [AllowAny]
    
class categoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('category_order')
    serializer_class = categorySerializer
    permission_classes = [AllowAny]
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
   # max_page_size = 10



class productView(viewsets.ModelViewSet):
    filterset_fields = {
        'category': ['exact'],
        'brand': ['exact'],
        'status': ['exact'],
        'productName':['icontains']
        
    }
    parser_classes = [MultiPartParser]
    queryset = Product.objects.order_by('-created_at')
    serializer_class = productSerializer
    permission_classes = [AllowAny]    
    pagination_class = StandardResultsSetPagination
    #parser_classes = (MultiPartParser, FormParser,)



class productsizeView(viewsets.ModelViewSet):
    filterset_fields = {
        'product': ['exact'],
        'status':['exact']

        }
    queryset = Productsize.objects.all()
    serializer_class = productsizeSerializer
    permission_classes = [AllowAny] 
         
class cartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer   
    permission_classes = [AllowAny]     
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user.id,is_ordered=False,query=False)   
    
    
    def create(self, request, *args, **kwargs):
        data = request.data
        if "products" in data:
            data_class = data["products"]
            # print(data_class)
            for i in data_class:
                if Cart.objects.filter(product_id = i['product'],productsize=i['productsize'],user_id=i["user"]).exists():
                    pass
                else:
                    quantity=i['quantity']
                    productid=Product.objects.get(id=i['product'])
                    productsize=Productsize.objects.get(id=i['productsize'])
                    productmaximumQty=productsize.maximumQty
                    productunitprice=productsize.unitprice
                    productdis=Category.objects.get(id=productid.category.id)
                    discount=productdis.discount
                    bill=quantity*productunitprice
                    data["quantity"]=i['quantity']
                    data["product"]=i['product']
                    data["productsize"]=i['productsize']
                    data["user"]=i['user']
                    data["unit"]=productsize.unitname
                    data["price"]=productunitprice
                    data["netsum"]=bill
                    data["discount"]=discount
                    data["productname"]=productid.productName
                    totaldiscount=bill-(bill*discount/100)
                    data["afterdiscount"]=totaldiscount
                    serializer = self.get_serializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                # headers = self.get_success_headers(serializer.data)
                # user = UserInfo.objects.get(email=i['admin']['email'])
                # user.set_password("123")
                # user.save()
        else:
            quantity=data['quantity']
            productid=Product.objects.get(id=data['product'])
            productsize=Productsize.objects.get(id=data['productsize'])
            productmaximumQty=productsize.maximumQty
            if quantity>productmaximumQty:
                productunitprice=productsize.unitprice
                productdis=Category.objects.get(id=productid.category.id)
                discount=productdis.discount
                bill=float(quantity)*float(productunitprice)
                data["user"]=request.user.id
                data["unit"]=productsize.unitname
                data["price"]=productunitprice
                data["netsum"]=bill
                data["discount"]=discount
                data["productname"]=productid.productName
                totaldiscount=bill-(bill*discount/100)
                data["afterdiscount"]=totaldiscount
                data["query"]=True
                serializer = CartSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    self.perform_create(serializer)
                    subject = 'Query generated for Product - #{productidd}'.format(productidd=productid.id)
                    message = "Dear Admin,\r\nYou have received a query for #{productidd}.\r\nPlease review it.\r\n http://139.59.39.231/jamaladmin/query_list".format(productidd=productid.id)
                    msg = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL])
                    msg.send() 
                    return Response({'message': 'we will get back to you'})
                
            else:   
                productunitprice=productsize.unitprice
                productdis=Category.objects.get(id=productid.category.id)
                discount=productdis.discount
                bill=float(quantity)*float(productunitprice)
                data["user"]=request.user.id
                data["unit"]=productsize.unitname
                data["price"]=productunitprice
                data["netsum"]=bill
                data["discount"]=discount
                data["productname"]=productid.productName
                totaldiscount=bill-(bill*discount/100)
                data["afterdiscount"]=totaldiscount
                serializer = CartSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    self.perform_create(serializer)
                    return Response({'message': 'order created'}, status=status.HTTP_201_CREATED)
        return Response({'success ': 'products added successfully'}, status=200)

        
        # data = request.data
        # quantity=data['quantity']
        # productid=Product.objects.get(id=data['product'])
        # productsize=Productsize.objects.get(id=data['productsize'])
        # productmaximumQty=productsize.maximumQty
        # if quantity>productmaximumQty:
        #     productunitprice=productsize.unitprice
        #     productdis=Category.objects.get(id=productid.category.id)
        #     discount=productdis.discount
        #     bill=float(quantity)*float(productunitprice)
        #     data["user"]=request.user.id
        #     data["unit"]=productsize.unitname
        #     data["price"]=productunitprice
        #     data["netsum"]=bill
        #     data["discount"]=discount
        #     data["productname"]=productid.productName
        #     totaldiscount=bill-(bill*discount/100)
        #     data["afterdiscount"]=totaldiscount
        #     data["query"]=True
        #     serializer = CartSerializer(data=data)
        #     if serializer.is_valid(raise_exception=True):
        #         self.perform_create(serializer)
        #         return Response({'message': 'we will get back to you'})
            
        # else:   
            # productunitprice=productsize.unitprice
            # productdis=Category.objects.get(id=productid.category.id)
            # discount=productdis.discount
            # bill=float(quantity)*float(productunitprice)
            # data["user"]=request.user.id
            # data["unit"]=productsize.unitname
            # data["price"]=productunitprice
            # data["netsum"]=bill
            # data["discount"]=discount
            # data["productname"]=productid.productName
            # totaldiscount=bill-(bill*discount/100)
            # data["afterdiscount"]=totaldiscount
            # serializer = CartSerializer(data=data)
            # if serializer.is_valid(raise_exception=True):
            #     self.perform_create(serializer)
            #     return Response({'message': 'order created'}, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        quantity=data['quantity']
        productid=Product.objects.get(id=data['product'])
        productsize=Productsize.objects.get(id=data['productsize'])
        productmaximumQty=productsize.maximumQty
        if quantity>productmaximumQty:
            productunitprice=productsize.unitprice
            productdis=Category.objects.get(id=productid.category.id)
            discount=productdis.discount
            bill=quantity*productunitprice
            data["user"]=request.user.id
            data["unit"]=productsize.unitname
            data["price"]=productunitprice
            data["netsum"]=round(bill,2)
            data["discount"]=discount
            data["productname"]=productid.productName
            totaldiscount=bill-(bill*discount/100)
            data["afterdiscount"]=round(totaldiscount, 2)
            data["query"]=True
            serializer = CartSerializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response({'message': 'we will get back to you'})       
        else:   
            productunitprice=productsize.unitprice
            productdis=Category.objects.get(id=productid.category.id)
            discount=productdis.discount
            bill=quantity*productunitprice
            data["user"]=request.user.id
            data["unit"]=productsize.unitname
            data["price"]=productunitprice
            data["netsum"]=round(bill,2)
            data["discount"]=discount
            data["productname"]=productid.productName
            totaldiscount=bill-(bill*discount/100)
            data["afterdiscount"]=round(totaldiscount, 2)
            serializer = CartSerializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response({'message': 'order is updated'}, status=status.HTTP_200_OK)
        
        
class totalView(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        queryset = Cart.objects.filter(user=user.id,is_ordered=False,query=False)
        ab=queryset.aggregate(Sum('afterdiscount')).values()
        #serializer = CartSerializer(queryset, many=True)
        total=0
        for i in ab:
            total=i
        
        string_num=f"{total:.3f}"
        totalprice={"total":string_num}
        return Response(totalprice) 


class orderView(viewsets.ModelViewSet):
    filterset_fields = {'date_ordered': ['gte', 'lte'],'id':['exact']}
    serializer_class = orderSerializer   
    permission_classes = [AllowAny]      
    
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Order.objects.filter(sales=False,re=False).order_by('-date_ordered')
    
   
    
    def create(self, request, *args, **kwargs):
        
        
        user = self.request.user
        data = request.data
        user1 = data['user']
      #  print(user1)
        cartlst=data["cart"]

        # for i in cartlst:
        #     cart=Cart.objects.get(id=i)
        #     psize=Productsize.objects.get(id=cart.productsize.id)
        #     if psize.inventory <= 0:
        #         subject = 'Out of stock - #{order_id}'.format(order_id=psize.product.id)
        #         message = "Dear Admin,Product ID #{order_id} of Size {sizename} is out of stock.\r\n Please re-stock.\r\n http://139.59.39.231/jamaladmin/products".format(order_id=psize.product.id,sizename=psize.productSizename)
        #         msg = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL])
        #         msg.send()

        filtercart=Cart.objects.filter(id__in=cartlst)
        for i in filtercart:
            i.is_ordered=True
            i.date_ordered=now
            i.save()
        
        filterprice=Cart.objects.filter(id__in=cartlst)
        ab=filterprice.aggregate(Sum('afterdiscount')).values()
        total=0
        for i in ab:
            total=i

        userinfo=UserRegistration.objects.get(id=user1)
        
        notification_name="order created by "+ userinfo.name

        # print(notification_name)
        # print(userinfo.name)
        Notification.objects.create(Name=notification_name)
        total=f"{total:.3f}"
        totalprice={"totalprice":total,"username":userinfo.name }
        lst=filterprice.values("productsize_id__productSizename","product_id","productsize_id__partNumber","productname","price","quantity","unit","netsum","discount","afterdiscount")
        mylst=[]
        mylst.append(totalprice)
        
        for i in lst:
            d={}
            d['product_id']=i['productsize_id__partNumber']
            d['productSizename']=i['productsize_id__productSizename']
            d['productname']=i['productname']
            price=f"{i['price']:.3f}"
            d['price']=price
            d['quantity']=i['quantity']
            d['unit']=i['unit']
            netsum=f"{i['netsum']:.3f}"
            d['netsum']=netsum
            d['discount']=i['discount']
            afterdiscount=f"{i['afterdiscount']:.3f}"
            d['afterdiscount']=afterdiscount
            mylst.append(d)

         


        # subject, from_email, to = 'Order Accepted', DEFAULT_FROM_EMAIL,user.email
        # message = "Your order has been accepted we will back to you"
        # msg = EmailMessage(subject, message, from_email, [to])
        # msg.send()

        serializer = orderSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            order_no=serializer.save()
            order_serial_no={"order_no":order_no.id}
            mylst.append(order_serial_no)
            sub='Order Received #{order_id}'.format(order_id=order_no.id)
            subject, from_email= sub, DEFAULT_FROM_EMAIL
            message = get_template('orderacc.html').render({"mylst":mylst}, request=request)
            msg = EmailMessage(subject, message, from_email,[userinfo.email,'online@jamaliunited.com'])
            msg.content_subtype = 'html'
            msg.send()   
            return Response({'message': "Order Accepted"}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        data = request.data
        user = data['user']
        userinfo=UserRegistration.objects.get(id=user)
        status=data['accept'] 
        if status==True:
            cartlst=data["cart"]
            data["sales"]=True
            data["accept"]=True
            total_discount=data['discount']
            
            for i in cartlst:
                cart=Cart.objects.get(id=i)
                quantity=cart.quantity
                psize=Productsize.objects.get(id=cart.productsize.id)
                quanti=psize.unitquantity
                totalquantity=quantity*quanti
                total=psize.inventory
                result=total-totalquantity
                psize.inventory=result
                psize.save()

            for i in cartlst:
                cart=Cart.objects.get(id=i)
                psize=Productsize.objects.get(id=cart.productsize.id)
                if psize.inventory <= 0:
                    subject = 'Out of stock - #{order_id}'.format(order_id=psize.product.id)
                    message = "Dear Admin,Product ID #{order_id} of Size {sizename} is out of stock.\r\n Please re-stock.\r\n http://139.59.39.231/jamaladmin/products".format(order_id=psize.product.id,sizename=psize.productSizename)
                    msg = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL])
                    msg.send()    
            
            filterprice=Cart.objects.filter(id__in=cartlst)
            ab=filterprice.aggregate(Sum('afterdiscount')).values()
            total=0
            for i in ab:
                total=i
            
            if total_discount==0:
                totalsales=total
            totalsales=total-(total*total_discount/100)
            
            
            salesdate=data["sales_date"] 

            newsalesdate=salesdate[0:10]
            
            # print(salesdate)
            totalsales=f"{totalsales:.3f}"

            totalprice={"totalprice":totalsales,"username":userinfo.name,
                       "extradiscount":total_discount,"sales_date":newsalesdate}

            lst=filterprice.values("productsize_id__productSizename","productsize_id__partNumber","product_id","productname","price","quantity","unit","netsum","discount","afterdiscount")
            data["totalsales"]=totalsales
            mylst=[]
            mylst.append(totalprice)
            for i in lst:
                d={}
                d['product_id']=i['productsize_id__partNumber']
                d['productSizename']=i['productsize_id__productSizename']
                d['productname']=i['productname']
                price=f"{i['price']:.3f}"
                d['price']=price
                d['quantity']=i['quantity']
                d['unit']=i['unit']
                netsum=f"{i['netsum']:.3f}"
                d['netsum']=netsum
                d['discount']=i['discount']
                afterdiscount=f"{i['afterdiscount']:.3f}"
                d['afterdiscount']=afterdiscount
                mylst.append(d)
            
            
            
            #cartobj= Cart.objects.filter(user=request.user.id,is_ordered=True,query=False)
            for i in filterprice:
                i.sales=True
                i.save()

            serializer = orderSerializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                order_no=serializer.save()
                order_serial_no={"order_no":order_no.id}
                mylst.append(order_serial_no)
                sub='Order Confirmed #{order_id}'.format(order_id=order_no.id)
                subject, from_email, to = sub, DEFAULT_FROM_EMAIL,userinfo.email
                message = get_template('order.html').render({"mylst":mylst}, request=request)
                msg = EmailMessage(subject, message, from_email, [to])
                msg.content_subtype = 'html'
                msg.send()
                return Response({'message': 'Order Placed'})
        
        reason = data['note']
        cartlst=data["cart"]
        data['re']=True
        data['sales']=True
        filterprice=Cart.objects.filter(id__in=cartlst)
        ab=filterprice.aggregate(Sum('afterdiscount')).values()
        total=0
        for i in ab:
            total=i
        totalprice={"totalprice":total,"username":userinfo.name,"reason":reason}
        lst=filterprice.values("productsize_id__productSizename","productsize_id__partNumber","product_id","productname","price","quantity","unit","netsum","discount","afterdiscount")
        mylst=[]
        mylst.append(totalprice)
        for i in lst:
            d={}
            d['product_id']=i['productsize_id__partNumber']
            d['productSizename']=i['productsize_id__productSizename']
            d['productname']=i['productname']
            price=f"{i['price']:.3f}"
            d['price']=price
            d['quantity']=i['quantity']
            d['unit']=i['unit']
            netsum=f"{i['netsum']:.3f}"
            d['netsum']=netsum
            d['discount']=i['discount']
            afterdiscount=f"{i['afterdiscount']:.3f}"
            d['afterdiscount']=afterdiscount
            mylst.append(d)
        
        subject, from_email, to = 'Your order has been Rejected', DEFAULT_FROM_EMAIL,userinfo.email
        message = get_template('reject_order.html').render({"mylst":mylst}, request=request)
        msg = EmailMessage(subject, message, from_email, [to])
        msg.content_subtype = 'html'
        msg.send()
        # msg = EmailMessage(subject, message, from_email, [to])
        # msg.send()        
        serializer = orderSerializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({'message': 'Order Rejected'})
                
    
class outofstockView(viewsets.ModelViewSet):
    queryset = Productsize.objects.all()
    serializer_class = outofstockkSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Productsize.objects.filter(inventory__lte=0)


class allordersView(viewsets.ModelViewSet):
    filterset_fields = {'date_ordered': ['gte', 'lte']}

    queryset = Cart.objects.all()
    serializer_class = allorderSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Cart.objects.filter(is_ordered=True)


class cartordersView(viewsets.ModelViewSet):
    filterset_fields = {'date_ordered': ['gte', 'lte']}
    queryset = Cart.objects.all()
    serializer_class = allorderSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Cart.objects.filter(is_ordered=False,query=False)



class bestproductView(viewsets.ModelViewSet):
    filterset_fields = {
        'category': ['exact'],
        'brand': ['exact']
        
    }
    queryset = Product.objects.filter(bestSeller=True)
    serializer_class = productSerializer
    permission_classes = [AllowAny] 


class queryView(viewsets.ModelViewSet):
    filterset_fields = {'date_ordered': ['gte', 'lte']}
    queryset = Cart.objects.filter(query=True)
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


class orderrView(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = orderrrSerializer   
    permission_classes = [AllowAny]      
        
    
    def list(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        
        for i in queryset:
            res=i.cart.all()
        
        querysett = Order.objects.all().values()
       
        response={
            "view":querysett,
            "cart":res.values()
        }
        return Response(response)
   

class allcartview(viewsets.ModelViewSet):
    queryset = Cart.objects.filter()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]   



class BannerView(viewsets.ModelViewSet):
    
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]     



class SalesReportView(viewsets.ModelViewSet):
  
    filterset_fields = {'sales_date': ['gte', 'lte']}
    queryset = Order.objects.filter(completed=True)
    serializer_class = salesSerializer
    permission_classes = [AllowAny]   


class OrderHistoryView(viewsets.ModelViewSet):
  
    filterset_fields = {'sales_date': ['gte', 'lte'],'accept': ['exact'],'user':['exact'],'completed':['exact']}
    queryset = Order.objects.filter(sales=True).order_by('-date_ordered')
    serializer_class = orderhistorySerializer
    permission_classes = [AllowAny]   
    
    def partial_update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        data = request.data
        serializer = orderhistorySerializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({'message': 'Order Completed'})



# class SalesReportView(viewsets.ModelViewSet):
  
#     filterset_fields = {'sales_date': ['gte', 'lte']}
#   #  queryset = Order.objects.filter(sales=True)
#     serializer_class = salesSerializer
#     permission_classes = [AllowAny]  
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             queryset = Order.objects.filter(sales=False,re=False)
#             return queryset
#         else:
#             return None



class Dashboardview(viewsets.ReadOnlyModelViewSet):
    
    
    def list(self, request):
        from itertools import groupby
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        q = Q()
        s= Q()
        u= Q()
        p= Q()
        if start_date is not None:
            q &= Q(date_ordered__gte=start_date,date_ordered__lte=end_date)
            s &= Q(sales_date__gte=start_date,sales_date__lte=end_date)
            u &= Q(created_at__gte=start_date,created_at__lte=end_date)
            p &= Q(created_at__gte=start_date,created_at__lte=end_date)
        
        orderobj=Order.objects.filter(q).count()

        salesobj=Order.objects.filter(s,completed=True).aggregate(Sum('totalsales'))
        
        print(salesobj)
        if salesobj["totalsales__sum"]:
            totalsales=f"{salesobj['totalsales__sum']:.3f}"
        else:
            totalsales=0
        totalusers=UserRegistration.objects.filter(u).count()
        
        totalproduct=Product.objects.filter(p).count()
        disabled_product=Product.objects.filter(status=False).count()
        out_of_stock_product=Productsize.objects.filter(inventory__lte=0).count()
      
        invoices = Order.objects.only('sales_date', 'totalsales').filter(completed=True).order_by('sales_date')
        indata=[]

        for i in invoices:
            if i.sales_date is not None:
               indata.append(i)
        
        month_totals = {
                    k: sum(x.totalsales for x in g) 
                    for k, g in groupby(indata, key=lambda i: i.sales_date.month)
                    }
        
        for i in range(1,13):
            if i not in month_totals.keys():
                month_totals[i]=0
        orderpending=Order.objects.filter(sales=False,re=False).count()
        orderdone=Order.objects.filter(completed=True).count()
        data={"totalorders":orderobj,
               "totalsales":totalsales,
               "totalusers":totalusers,
               "totalitems":totalproduct,
               "monthwise":month_totals,
               "orderpending":orderpending,
               "orderdone":orderdone,
               "disabled_product":disabled_product,
               "out_of_stock_product":out_of_stock_product
                }
       
        return Response(data)    



class NotificationView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Notification.objects.filter(status=False)
        return queryset


class images_not_added(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.filter(image="")
        res={"images":queryset.values()}
        return Response(res) 


class contactUsView(viewsets.ModelViewSet):
    
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ContactUsSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            contact_us_ser=serializer.save()
            contactusdict={
                 "name" : contact_us_ser.name,
                 "number":contact_us_ser.contactNo,
                 "message":contact_us_ser.message
            }
            
            subject, from_email, to = 'Contact US Message', DEFAULT_FROM_EMAIL,DEFAULT_FROM_EMAIL
            message = get_template('contact_us.html').render({'contactusdict': contactusdict}, request=request)
            msg = EmailMessage(subject, message, from_email, [to])
            msg.content_subtype = 'html'
            msg.send()
            return Response({'message': "message send"}, status=status.HTTP_201_CREATED)
    
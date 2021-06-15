from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from django.db.models import Q

from .models import Product, Tag
from .serializers import ProductSerializer
from category.models import Category



class ProductAPIView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    # data_product = self.request.POST
    # image = request.FILES['image']
    # title = data_product.get('title', '')
    # description = data_product.get('description')
    # active = data_product.get('active')
    # featured = data_product.get('featured')
    # original_price = data_product.get('original_price', 0.0)
    # price = data_product.get('price')
    # tax = data_product.get('tax')
    try:
      serializer = ProductSerializer(data=request.data, many=False)
      if serializer.is_valid(raise_exception=True):
        product = serializer.save()
        return Response('create product success!')
    except:
      str_error = ''
      errors = serializer.errors
      for key, values in errors.items():
        str_error += key
        for text in values:
          str_error += ' ' + text
      return Response(str_error.lower())

    # try:
    #   product = Product.objects.create(title=title, image=image, description=description,
    #                                       active=active, featured=featured, original_price=original_price,
    #                                       price=price, tax=tax)
    #   if product:
    #     return Response('create product success!')
    # except:
    #   return Response('create product faild')

@api_view(['GET'])
def getProductsWithCategory(request, id_category, *args, **kwargs):
  products = Product.objects.filter(category=id_category)
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def getManyProductsDifferWithCategory(request, id_category, *args, **kwargs):
  subs_categories = Category.objects.filter(parent=id_category)
  products = []
  for cate in subs_categories:
    data_products = Product.objects.filter(category=cate.id)
    products += data_products
  serializer = ProductSerializer(products, many=True)
  # products = Product.objects.filter(id=id_category)
  # serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)



class ProductViewSet(ModelViewSet):
  serializer_class = ProductSerializer
  permission_classes = [permissions.AllowAny]
  lookup_field = 'id'

  # def get_queryset(self):
  #   data = self.request.GET
  #   max_price = data.get('max_price')
  #   min_price = data.get('min_price')
  #   sort = data.get('sort')
  #   keyword = data.get('keyword')
  #   products = Product.objects.filter_products(keyword, sort, min_price, max_price)
  #   return products


  def get_queryset(self):
    products_men = Product.objects.filter(Q(gender=0))[:4]
    products_women = Product.objects.filter(Q(gender=1))[:4]
    products = list(products_men) + list(products_women)
    return products

  # def get_permissions(self):
  #   """
  #   Instantiates and returns the list of permissions that this view requires.
  #   """
  #   if self.action == 'list' or self.action == 'retrieve':
  #     permission_classes = [AllowAny]
  #   else:
  #     permission_classes = [IsAdminUser]
  #   return [permission() for permission in permission_classes]

  def retrieve(self, request, id, *args, **kwargs):
    instance = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(instance, many=False)
    return Response(serializer.data)

  def create(self, request, *args, **kwargs):
    try:
      serializer = ProductSerializer(data=request.data, many=False)
      if serializer.is_valid(raise_exception=True):
        product = serializer.save()
        return Response('create product success!')
    except:
      str_error = ''
      errors = serializer.errors
      for key, values in errors.items():
        str_error += key
        for text in values:
          str_error += ' ' + text
      return Response(str_error.lower())


  def destroy(self, request, id, *args, **kwargs):
    product = Product.objects.get(id=id)
    if product:
      try:
        product.delete()
        return Response('delete product success!')
      except:
        return Response('can not delete product')
    return Response('product not found')

  def update(self, request, id, *args, **kwargs):
    product = Product.objects.get(id=id)
    try:
      if product:
        data_product = request.data
        product.title = data_product.get('title', product.title)
        if request.FILES['image']:
          product.image = request.FILES['image']
        product.description = data_product.get('description', product.description)
        product.active = data_product.get('active', product.active)
        product.featured = data_product.get('featured',product.featured)
        product.original_price = data_product.get('original_price', product.original_price)
        product.price = data_product.get('price', product.price)
        product.tax = data_product.get('tax', product.tax)
        product.save()
        return Response('update product success!')
    except:
      return Response('can not update product!')



class RelatedProductView(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, id, *args, **kwargs):
    product_id = id  # request.data.get("product_id")
    if not product_id:
      return Response({"error": "Product Id Not Found"}, status=400)
    product = get_object_or_404(Product, id=product_id)
    products_serialized = ProductSerializer(
      product.get_related_products(), many=True, context={'request': request})
    return Response(products_serialized.data)

  @classmethod
  def get_extra_actions(cls):
    return []



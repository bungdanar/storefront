from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.pagination import PageNumberPagination

from store.filters import ProductFilter
from store.pagination import DefaultPagination
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)

    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({
                'error': 'Product cannot be deleted because it is associated with an order item.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()

    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it includes one or more products.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()

#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}

#     # Use these if inherit from APIView
#     # def get(self, request):
#     #     queryset = Product.objects.select_related('collection').all()
#     #     serializer = ProductSerializer(
#     #         queryset, many=True, context={'request': request})
#     #     return Response(serializer.data)

#     # def post(self, request):
#     #     serializer = ProductSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # Use these if inherit from APIView
#     # def get(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)

#     # def put(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({
#                 'error': 'Product cannot be deleted because it is associated with an order item.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()

#     serializer_class = CollectionSerializer

#     # def get_queryset(self):
#     #     return Collection.objects.annotate(
#     #         products_count=Count('products')).all()

#     # def get_serializer_class(self):
#     #     return CollectionSerializer

#     # Use these if inherit from APIView
#     # def get(self, request):
#     #     queryset = Collection.objects.annotate(
#     #         products_count=Count('products')).all()

#     #     serializer = CollectionSerializer(queryset, many=True)
#     #     return Response(serializer.data)

#     # def post(self, request):
#     #     serializer = CollectionSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products'))
#     serializer_class = CollectionSerializer

#     # Use these if inherit from APIView
#     # def get(self, request, pk):
#     #     collection: Collection = get_object_or_404(Collection.objects.annotate(
#     #         products_count=Count('products')), pk=pk)

#     #     serializer = CollectionSerializer(collection)
#     #     return Response(serializer.data)

#     # def put(self, request, pk):
#     #     collection: Collection = get_object_or_404(Collection.objects.annotate(
#     #         products_count=Count('products')), pk=pk)

#     #     serializer = CollectionSerializer(collection, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)

#     def delete(self, request, pk):
#         collection: Collection = get_object_or_404(Collection, pk=pk)

#         if collection.products.count() > 0:
#             return Response({
#                 'error': 'Collection cannot be deleted because it includes one or more products.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

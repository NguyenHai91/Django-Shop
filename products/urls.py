
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ProductViewSet, RelatedProductView, ProductAPIView,
                    getProductsWithCategory, getManyProductsDifferWithCategory)

urlpatterns = [
  path('create/', ProductAPIView.as_view()),
  path('delete/<id>/', ProductViewSet.as_view({'delete': 'destroy'})),
  path('update/<id>/', ProductViewSet.as_view({'put': 'update'})),
  path('list/', ProductViewSet.as_view({'get': 'list'})),
  path('<id>/', ProductViewSet.as_view({'get': 'retrieve'})),
  path('related/<id>/', RelatedProductView.as_view()),
  path('category/<id_category>/details/', getProductsWithCategory),
  path('category/<id_category>/', getManyProductsDifferWithCategory),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
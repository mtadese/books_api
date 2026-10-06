from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

#DefaultRouter automatically creates standard RESTful endpoints
router=DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
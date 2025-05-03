from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'listQuiz', quiz_list)
# router.register(r'quiz_detail', quiz_detail)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
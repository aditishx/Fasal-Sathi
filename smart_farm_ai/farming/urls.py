from django.urls import include, path
from . import views
from .views import disease_detection, market_prediction, signup, login_user, logout_user, dashboard, blog_and_news
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('crop/', views.crop_recommend, name='crop'),
    path("disease/", disease_detection, name="disease"),
    path("market/", market_prediction, name="market"),
    path('blog/', blog_and_news, name='blog'),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('history/', views.combined_history, name='combined_history'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


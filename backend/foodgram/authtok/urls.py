from django.urls import include, path

app_name = 'authtok'


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]

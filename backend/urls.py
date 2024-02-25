from django.urls import path, include, re_path

app_name = 'backend'
urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),


]

from django.urls import path, include, re_path

from backend.views import UserView, ContactView

app_name = 'backend'
urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('user/details', UserView.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),

]

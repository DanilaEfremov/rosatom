from django.urls import path, include


urlpatterns = [
    path('chat/', include('chat.api.urls')),
    path('accounts/', include('accounts.api.urls')),
]

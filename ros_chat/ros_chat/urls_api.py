from django.urls import path, include


urlpatterns = [
    path('chat/', include('chat.chat_api_urls')),
    path('accounts/', include('accounts.accounts_api_urls')),
]

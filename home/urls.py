from django.urls import path, include

from home.views import WebLoginView, ChatPanelView

urlpatterns = [
    path('login/', WebLoginView.as_view(), name='web-login'),
    path('chat-panel/', ChatPanelView.as_view(), name='chat-panel'),
]
from django.urls import path, include, re_path

from home.views import WebLoginView, ChatPanelView

urlpatterns = [
    path('login/', WebLoginView.as_view(), name='web-login'),
    re_path(
        r"^messages/(?P<user_id>[\w-]+)/$", ChatPanelView.as_view(),
        name='chat-panel'
    ),
]
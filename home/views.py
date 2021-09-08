from django.shortcuts import render

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class WebLoginView(TemplateView):
    template_name = "login.html"


class ChatPanelView(TemplateView):
    template_name = "chat_panel.html"

# -*- coding:utf-8 -*-
from django.urls import re_path
from constrainedfilefield.tests import views

urlpatterns = [
    re_path(r"^nomodel/$", views.nomodel_form, name="nomodel"),
]

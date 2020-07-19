from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.forms.models import modelform_factory, HiddenInput
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count, Avg
from django.db.models import Q
from django.db.models.functions import Round
from django.utils.translation import get_language
from django.contrib import messages
import json
import logging

# Create your views here.

class InstructorCreateAccount(View):
    def get(self, request, *args, **kwargs):
        return render(request,'Hello World')



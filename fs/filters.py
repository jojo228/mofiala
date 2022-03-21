from django.db.models import fields
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class AgenceFilter(django_filters.FilterSet):
    Nom = CharFilter(field_name ="nom_agence", lookup_expr="icontains", label="Nom de l'agence")


class ContribuableFilter(django_filters.FilterSet):
    Nom = CharFilter(field_name ="first_name", lookup_expr="icontains", label="Nom de l'agence")



        
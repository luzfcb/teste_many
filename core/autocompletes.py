# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip

from dal import autocomplete
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class UserAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete view to Django User Based
    """

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super(UserAutocomplete, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return USER_MODEL.objects.none()

        assinado_por = self.forwarded.get('assinado_por', None)

        qs = User.objects.all().order_by('first_name', 'last_name')

        if self.q:
            qs = qs.filter(Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q))

        if assinado_por:
            qs = qs.exclude(id=assinado_por)
            # qs = qs.annotate(full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField()))
            # qs = qs.filter(full_name__icontains=self.q)
        return qs

    def get_result_label(self, result):
        name, user_name = result.get_full_name().title(), getattr(result, result.USERNAME_FIELD)
        return '{} ({})'.format(name, user_name)

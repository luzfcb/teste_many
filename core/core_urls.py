from django.conf.urls import url

from core import views, autocompletes

urlpatterns = [
    url(r'^$', views.DocumentoListar.as_view(), name='list'),
    url(r'^editar/(?P<slug>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',
        views.DocumentoEditar.as_view(), name='editar'),
    url(r'^assinar/(?P<slug>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',
        views.AssinarDocumentoView.as_view(), name='assinar'),
    url(r'^user-autocomplete/$',
        autocompletes.UserAutocomplete.as_view(),
        name='user-autocomplete'
        ),
]

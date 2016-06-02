from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import redirect

from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache

from core.forms import AssinarDocumentoForm
from core.models import Documento, Assinatura


class AssinarDocumentoView(generic.FormView, generic.DetailView):
    template_name = 'core/documento_assinar.html'
    form_class = AssinarDocumentoForm
    model = Documento
    slug_field = 'uuid_hash'
    success_url = reverse_lazy('documentos:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AssinarDocumentoView, self).post(request, *args, **kwargs)

    @method_decorator(never_cache)
    @method_decorator(login_required)
    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(AssinarDocumentoView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(AssinarDocumentoView, self).get_initial()
        # copia o dicionario, para evitar mudar acidentalmente um dicionario mutavel
        initial = initial.copy()
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated():
            initial.update({
                'assinado_por': user,
            }
            )
        return initial

    def get_form_kwargs(self):
        kwargs = super(AssinarDocumentoView, self).get_form_kwargs()
        current_logged_user = self.request.user
        kwargs['current_logged_user'] = current_logged_user
        return kwargs

    def form_valid(self, form):
        ret = super(AssinarDocumentoView, self).form_valid(form)
        ###################################
        # documento = form.save(False)
        documento = self.object

        assinado_por = form.cleaned_data.get('assinado_por')
        form.save()
        # # cria ou obten instancia de Assinatura para o usuario selecionado em  assinado_por
        # obj, created = Assinatura.objects.get_or_create(documento=documento,
        #                                                 assinado_por=assinado_por,
        #                                                 versao_numero=documento.versao_numero,
        #                                                 esta_ativo=True,
        #                                                 defaults={
        #                                                     'documento': documento,
        #                                                     'assinado_por': assinado_por,
        #                                                     'versao_numero': documento.versao_numero + 1,
        #                                                     'esta_ativo': True
        #                                                 }
        #                                                 )
        # if created:
        #     print("criado : {}".format(obj.assinado_por.username))
        # else:
        #     print("obtido")
        #
        # if not obj.esta_assinado:
        #     obj.assinar_documento()
        #
        # # cria assinatura
        # usuarios_assinantes = form.cleaned_data.get('incluir_assinantes')
        # for usuario_assinante in usuarios_assinantes:
        #     # Assinatura.objects.get
        #     obj, created = Assinatura.objects.get_or_create(documento=documento,
        #                                                     assinado_por=usuario_assinante,
        #                                                     versao_numero=documento.versao_numero,
        #                                                     defaults={
        #                                                         'documento': documento,
        #                                                         'assinado_por': usuario_assinante,
        #                                                         'versao_numero': documento.versao_numero + 1,
        #                                                         'esta_assinado': False
        #                                                     }
        #                                                     )
        #     if created:
        #         print("criado : {}".format(obj.assinado_por.username))
        #         # notificar usuario
        #     else:
        #         print("obtido")
        #
        # # documento.assinar_documento(
        # #     assinado_por=form.cleaned_data.get('assinado_por'),
        # #     current_logged_user=form.current_logged_user
        # # )
        #
        # print(form.cleaned_data.get('incluir_assinantes'))
        # # return documento
        # ###################################
        # assinado_por = form.cleaned_data.get('assinado_por', None)
        #
        # msg = 'Documento n°{} assinado com sucesso por {}'.format(
        #     self.object.identificador_versao,
        #     assinado_por.get_full_name().title()
        # )
        # messages.add_message(self.request, messages.INFO, msg)
        return ret

    def get_success_url(self):
        # detail_url = reverse('documentos:validar-detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('documentos:list')
        # return detail_url


class DocumentoEditar(generic.UpdateView):
    model = Documento
    template_name = 'core/documento_editar.html'
    fields = '__all__'
    slug_field = 'uuid_hash'
    success_url = reverse_lazy('documentos:list')

    def get(self, request, *args, **kwargs):
        response = super(DocumentoEditar, self).get(request, *args, **kwargs)
        if self.object.status_assinatura == Documento.ASSINADO:
            response = redirect('documentos:list')
        return response


class DocumentoListar(generic.ListView):
    model = Documento

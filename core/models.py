from __future__ import absolute_import, unicode_literals

import uuid
from django.db import models, transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
import autorepr

__all__ = (
    'Assinatura',
    'AssinaturaBloco',
    'Documento'
)


class ActiveInactiveQuerySet(models.QuerySet):
    def inativos(self):
        return self.filter(esta_ativo=False)

    def ativos(self):
        return self.filter(esta_ativo=True)

    def nao_assinados(self, assinante=None):
        if assinante:
            return self.ativos().filter(esta_assinado=False, assinado_por=assinante)
        return self.ativos().filter(esta_assinado=False)

    def assinados(self, assinante=None):
        if assinante:
            return self.ativos().filter(esta_assinado=True, assinado_por=assinante)
        return self.ativos().filter(esta_assinado=True)


class AssinaturaManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return ActiveInactiveQuerySet(model=self.model, using=self._db).ativos()

    def inativos(self):
        return ActiveInactiveQuerySet(model=self.model, using=self._db).inativos()

    def ativos(self):
        return self.get_queryset()

    def nao_assinados(self, assinante=None):
        return self.get_queryset().nao_assinados(assinante=assinante)

    def assinados(self, assinante=None):
        return self.get_queryset().assinados(assinante=assinante)


class AssinaturaAdminManager(models.Manager):
    def get_queryset(self):
        return ActiveInactiveQuerySet(model=self.model, using=self._db)

    def inativos(self):
        return self.get_queryset().inativos()

    def ativos(self):
        return self.get_queryset().ativos()

    def nao_assinados(self, assinante=None):
        return self.get_queryset().nao_assinados(assinante=assinante)

    def assinados(self, assinante=None):
        return self.get_queryset().assinados(assinante=assinante)


class AssinaturaBlocoManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return ActiveInactiveQuerySet(model=self.model, using=self._db)

    def inativos(self):
        return self.get_queryset().inativos()

    def ativos(self):
        return self.get_queryset().ativos()

    def nao_assinados(self, assinante=None):
        return self.get_queryset().nao_assinados(assinante=assinante)

    def assinados(self, assinante=None):
        return self.get_queryset().assinados(assinante=assinante)


class Assinatura(models.Model):
    assinatura_bloco = models.ForeignKey(to='AssinaturaBloco',
                                         related_name="assinaturas",
                                         null=True,
                                         blank=True,
                                         on_delete=models.SET_NULL,
                                         # editable=False,
                                         )

    assinado_por = models.ForeignKey(to='auth.User',
                                     related_name="%(app_label)s_%(class)s_assinado_por",
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     # editable=False
                                     )

    esta_ativo = models.NullBooleanField(default=True, editable=False)

    objects = AssinaturaManager()

    def __repr__(self):
        return 'Assinatura(id={}, assinatura_bloco={}, assinado_por={})'.format(self.pk, self.assinatura_bloco_id,
                                                                                self.assinado_por_id)

    def __str__(self):
        return self.__repr__()


class AssinaturaBloco(models.Model):
    documento = models.ForeignKey(to='Documento',
                                  related_name="bloco_assinatura",
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  # editable=False,
                                  )

    assinantes = models.ManyToManyField(to='auth.User',
                                        related_name="assinaturas",
                                        blank=True,
                                        through='Assinatura',
                                        # editable=False,
                                        )

    datahora = models.DateTimeField(default=timezone.now, editable=False)

    esta_ativo = models.NullBooleanField(default=True, editable=True)

    objects = AssinaturaBlocoManager()

    def __str__(self):
        return 'pk: {}, documento: {}, assinantes: {}, datahora: {}'.format(getattr(self, 'pk', None),
                                                                            self.documento.pk, self.assinantes,
                                                                            self.datahora)

    class Meta:
        ordering = ('documento',)


class Documento(models.Model):
    uuid_hash = models.UUIDField(editable=False, unique=True, null=True)

    NAO_ASSINADO = 10
    POSSUI_ASSINATURAS_PENDENTES = 20
    ASSINADO = 30

    STATUS_ASSINATURA = (
        (NAO_ASSINADO, 'Não Assinado'),
        (POSSUI_ASSINATURAS_PENDENTES, 'Possui Assinaturas Pendentes'),
        (ASSINADO, 'Esta assinado e não possui nenhuma assinatura pendente'),
    )

    status_assinatura = models.PositiveSmallIntegerField(choices=STATUS_ASSINATURA, default=NAO_ASSINADO)

    def __str__(self):
        return 'pk: {}'.format(getattr(self, 'pk', None))

    @method_decorator(transaction.atomic)
    def save(self, *args, **kwargs):
        if not self.uuid_hash:
            self.uuid_hash = uuid.uuid4()

        super(Documento, self).save(*args, **kwargs)
        if not self.bloco_assinatura.count():
            assinatura_block = AssinaturaBloco(documento=self)
            assinatura_block.save()
            # super(Documento, self).save(*args, **kwargs)

    def remover_assinatura(self):
        if not self.bloco_assinatura.count():
            assinatura_block = AssinaturaBloco(documento=self)
            assinatura_block.save()

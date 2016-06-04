from __future__ import absolute_import, unicode_literals

import uuid
from django.db import models, transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from . import managers

__all__ = (
    'Assinatura',
    'AssinaturaBloco',
    'Documento'
)


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

    esta_assinado = models.BooleanField(default=False, editable=False)
    esta_ativo = models.NullBooleanField(default=True, editable=False)

    objects = managers.AssinaturaManager()

    def __repr__(self):
        return 'Assinatura(id={}, assinatura_bloco={}, assinado_por={})'.format(self.pk,
                                                                                self.assinatura_bloco_id,
                                                                                self.assinado_por_id)

    def __str__(self):
        return self.__repr__()


class AssinaturaBloco(models.Model):
    documento = models.ForeignKey(to='Documento',
                                  related_name="_bloco_assinatura",
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

    criado_em = models.DateTimeField(default=timezone.now, editable=False)

    esta_ativo = models.NullBooleanField(default=True, editable=True)

    objects = managers.AssinaturaBlocoManager()

    def __str__(self):
        return 'pk: {}, documento: {}, assinantes: {}, datahora: {}'.format(getattr(self, 'pk', None),
                                                                            self.documento_id,
                                                                            self.assinantes.all(),
                                                                            self.datahora)

    def adicionar_assinantes_ao_bloco(self, assinantes):
        for assinante in assinantes:
            yield self._nova_assinatura(assinante)

    def _nova_assinatura(self, assinante):
        if self.pk:
            obj, created = self.assinantes.through.objects.get_or_create(assinatura_bloco=self,
                                                                         assinado_por=assinante,
                                                                         defaults={
                                                                             'assinatura_bloco': self,
                                                                             'assinado_por': assinante,
                                                                         }
                                                                         )
            return obj, created
        return None, False

    class Meta:
        ordering = ('documento',)


class Documento(models.Model):
    NAO_ASSINADO = 10
    POSSUI_ASSINATURAS_PENDENTES = 20
    ASSINADO = 30

    uuid_hash = models.UUIDField(editable=False, unique=True, null=True, db_index=True)
    assinatura_hash = models.TextField(blank=True)
    conteudo_documento = models.TextField(blank=True)

    STATUS_ASSINATURA = (
        (NAO_ASSINADO, 'Não Assinado'),
        (POSSUI_ASSINATURAS_PENDENTES, 'Possui Assinaturas Pendentes'),
        (ASSINADO, 'Esta assinado e não possui nenhuma assinatura pendente'),
    )

    status_assinatura = models.PositiveSmallIntegerField(choices=STATUS_ASSINATURA, default=NAO_ASSINADO)

    @property
    def status_assinatura_verbose(self):
        return dict(Documento.STATUS_ASSINATURA)[self.status_assinatura]

    def __str__(self):
        return 'pk: {}'.format(getattr(self, 'pk', None))

    @method_decorator(transaction.atomic)
    def save(self, *args, **kwargs):
        if not self.uuid_hash:
            self.uuid_hash = uuid.uuid4()

        super(Documento, self).save(*args, **kwargs)
        if not self._bloco_assinatura.exists():
            self._novo_bloco_assinatura(desativar_antigos=True)
            # assinatura_block = AssinaturaBloco(documento=self)
            # assinatura_block.save()
            # super(Documento, self).save(*args, **kwargs)

    def remover_assinatura(self):
        return self._novo_bloco_assinatura(desativar_antigos=True)

    def _novo_bloco_assinatura(self, desativar_antigos=False) -> AssinaturaBloco:
        if desativar_antigos:
            self._bloco_assinatura.update(esta_ativo=False)

        assinatura_block = AssinaturaBloco.objects.create(documento=self)
        return assinatura_block

    def adicionar_assinantes(self, assinantes):
        return self.bloco_assinatura.adicionar_assinantes_ao_bloco(assinantes)

    @cached_property
    def bloco_assinatura(self):
        bloco = self._bloco_assinatura.filter(esta_ativo=True)
        if bloco:
            bloco = bloco.first()
        return bloco or None

    def assinaturas(self):
        return self.bloco_assinatura.assinaturas.all()

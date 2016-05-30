from django.db import models


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

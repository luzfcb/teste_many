from django.contrib import admin

from . import models


@admin.register(models.Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    pass


class AssinaturaInline(admin.TabularInline):
    model = models.AssinaturaBloco.assinantes.through


@admin.register(models.AssinaturaBloco)
class AssinaturaBlocoAdmin(admin.ModelAdmin):
    inlines = [AssinaturaInline]


class AssinaturaIBloconline(admin.TabularInline):
    model = models.AssinaturaBloco
    extra = 0


@admin.register(models.Documento)
class DocumentoAdmin(admin.ModelAdmin):
    inlines = [AssinaturaIBloconline]
    list_display = ['pk', 'uuid_hash']

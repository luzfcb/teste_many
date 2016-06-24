# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assinatura',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('esta_assinado', models.BooleanField(default=False, editable=False)),
                ('esta_ativo', models.NullBooleanField(default=True, editable=False)),
                ('assinado_por', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='core_assinatura_assinado_por')),
            ],
        ),
        migrations.CreateModel(
            name='AssinaturaBloco',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('esta_ativo', models.NullBooleanField(default=True)),
                ('assinantes', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='core.Assinatura', blank=True, related_name='assinaturas')),
            ],
            options={
                'ordering': ('documento',),
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('uuid_hash', models.UUIDField(null=True, db_index=True, unique=True, editable=False)),
                ('assinatura_hash', models.TextField(blank=True)),
                ('conteudo_documento', models.TextField(blank=True)),
                ('status_assinatura', models.PositiveSmallIntegerField(choices=[(10, 'Não Assinado'), (20, 'Possui Assinaturas Pendentes'), (30, 'Esta assinado e não possui nenhuma assinatura pendente')], default=10)),
            ],
        ),
        migrations.AddField(
            model_name='assinaturabloco',
            name='documento',
            field=models.ForeignKey(null=True, to='core.Documento', blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='_bloco_assinatura'),
        ),
        migrations.AddField(
            model_name='assinatura',
            name='assinatura_bloco',
            field=models.ForeignKey(null=True, to='core.AssinaturaBloco', blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assinaturas'),
        ),
    ]

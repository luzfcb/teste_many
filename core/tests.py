from django.test import TestCase
from django.contrib.auth.models import User
# https://pypi.python.org/pypi/factory_boy/
import factory
# https://pypi.python.org/pypi/Unidecode
from unidecode import unidecode

from . import models

DEFAULT_PASSWORD = 123


class UserAdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('first_name', 'last_name')

    username = factory.LazyAttributeSequence(
        lambda o, n: unidecode('%s_%s' % (o.first_name.lower(), o.last_name.lower())).replace(' ', '_'))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda o: '%s@gmail.com' % o.username)
    password = factory.PostGenerationMethodCall('set_password',
                                                DEFAULT_PASSWORD)
    is_superuser = True
    is_staff = True
    is_active = True


# class UserTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # create and save 96 instances of User
#         cls.users_list = UserAdminFactory.create_batch(96)
#

# Create your tests here.
class DocumentoTestCase(TestCase):
    fixtures = ['auth.json']
    documento = None
    bloco_assinatura1 = None
    bloco_assinatura2 = None
    usuarios = []

    def setUp(self):
        self.documento = models.Documento.objects.create()
        self.bloco_assinatura1 = self.documento.bloco_assinatura
        self.contador = User.objects.count()
        # self.assinantes = UserAdminFactory.create_batch(3)

    # def test_bloco_assinatura_em_documento(self):
    #     self.assertEqual(self.documento.bloco_assinatura.all().count(), 1)

    def test_novo_bloco_em_documento(self):

        novo_bloco = self.documento._novo_bloco_assinatura(True)
        self.assertIsNot(self.bloco_assinatura1, novo_bloco)
        self.assertIsNot(self.bloco_assinatura1, self.documento.bloco_assinatura)

    def test_adicionar_assinantes(self):
        assinantes = User.objects.all()[:5]
        self.documento.adicionar_assinantes(assinantes)

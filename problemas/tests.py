from django.test import TestCase
from django.utils import timezone
from .models import Problema, Resolucao
from obras.models import Obra

class ProblemaModelTest(TestCase):
    def setUp(self):
        self.obra = Obra.objects.create(nome="Nome da Obra")
        self.problema = Problema.objects.create(
            obra=self.obra,
            descricao="Descrição do problema",
            categoria='MAT',
            severidade='BAIX',
            status='ABERTO'
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.problema),
            "Problema: Descrição do problema... Status: Aberto"
        )

class ResolucaoModelTest(TestCase):
    def setUp(self):
        self.obra = Obra.objects.create(nome="Nome da Obra")
        self.problema = Problema.objects.create(
            obra=self.obra,
            descricao="Descrição do problema",
            categoria='MAT',
            severidade='BAIX',
            status='ABERTO'
        )
        self.resolucao = Resolucao.objects.create(
            problema=self.problema,
            responsavel_resolucao="Responsável",
            observacoes="Observações"
        )

    def test_str_representation(self):
        self.assertEqual(
        str(self.resolucao),
        f"Resolução para o problema {self.problema.id}"
    )

    def test_update_problema_status(self):
        self.problema.refresh_from_db()
        self.assertEqual(self.problema.status, "RESOLVIDO")

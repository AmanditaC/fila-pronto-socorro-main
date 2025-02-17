# tests/test_fila_pronto_socorro_unittest.py
import unittest
from datetime import datetime
from main.domain import Paciente, FilaAtendimento, Atendimento, Risco, ValidacaoError, FilaVaziaError

class TestPaciente(unittest.TestCase):
    def test_criar_paciente(self):
        # Testa a criação de um paciente com dados válidos
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        self.assertEqual(paciente.nome, "João Silva")
        self.assertEqual(paciente.cpf, "12345678901")
        self.assertEqual(paciente.email, "joao@example.com")
        self.assertEqual(paciente.nascimento, "01/01/1990")

    def test_validar_nome_invalido(self):
        # Testa a validação de um nome inválido (vazio)
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        self.assertIn("O nome do paciente é obrigatório.", str(context.exception))

    def test_validar_cpf_invalido(self):
        # Testa a validação de um CPF inválido (com menos de 11 dígitos)
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="João Silva", cpf="123", email="joao@example.com", nascimento="01/01/1990")
        self.assertIn("CPF inválido, deve conter 11 dígitos numéricos.", str(context.exception))

    def test_validar_email_invalido(self):
        # Testa a validação de um e-mail inválido
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="João Silva", cpf="12345678901", email="joao@", nascimento="01/01/1990")
        self.assertIn("E-mail inválido.", str(context.exception))

class TestFilaAtendimento(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes da fila de atendimento
        self.fila = FilaAtendimento()
        self.paciente1 = Paciente(nome="Maria Oliveira", cpf="98765432109", email="maria@example.com", nascimento="15/05/1985")
        self.paciente2 = Paciente(nome="Carlos Souza", cpf="45678912309", email="carlos@example.com", nascimento="20/10/1975")
        self.atendimento1 = Atendimento(paciente=self.paciente1, risco=Risco.VERDE)
        self.atendimento2 = Atendimento(paciente=self.paciente2, risco=Risco.VERMELHO)

    def test_inserir_atendimento(self):
        # Testa a inserção de um atendimento na fila
        self.fila.inserir(self.atendimento1)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_proximo_atendimento(self):
        # Testa a remoção do próximo atendimento da fila (prioridade por risco)
        self.fila.inserir(self.atendimento1)  # Risco VERDE
        self.fila.inserir(self.atendimento2)  # Risco VERMELHO (maior prioridade)
        proximo = self.fila.proximo()
        self.assertEqual(proximo.paciente.nome, "Carlos Souza")  # Risco VERMELHO deve ser atendido primeiro
        self.assertEqual(self.fila.tamanho(), 1)

    def test_fila_vazia(self):
        # Testa o comportamento da fila quando está vazia
        with self.assertRaises(FilaVaziaError) as context:
            self.fila.proximo()
        self.assertIn("Não tem nenhum paciente na fila de atendimento", str(context.exception))

    def test_ordem_chegada(self):
        # Testa a ordem de chegada quando os riscos são iguais
        paciente3 = Paciente(nome="Ana Costa", cpf="12345678901", email="ana@example.com", nascimento="05/12/2000")
        atendimento3 = Atendimento(paciente=paciente3, risco=Risco.VERDE)
        self.fila.inserir(self.atendimento1)  # Risco VERDE
        self.fila.inserir(atendimento3)  # Risco VERDE (deve ser atendido depois)
        self.assertEqual(self.fila.proximo().paciente.nome, "Maria Oliveira")
        self.assertEqual(self.fila.proximo().paciente.nome, "Ana Costa")

if __name__ == '__main__':
    unittest.main()
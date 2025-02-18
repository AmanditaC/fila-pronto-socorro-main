import pytest
from datetime import datetime
from main.domain import Paciente, Risco, Atendimento, FilaAtendimento, ValidacaoError, FilaVaziaError

# Fixtures para reutilização de código
@pytest.fixture
def paciente_valido():
    return Paciente("João Silva", "12345678901", "joao@example.com", "01/01/2000")

@pytest.fixture
def paciente_invalido_cpf():
    return Paciente("Maria Oliveira", "1234567890", "maria@example.com", "02/02/1990")

@pytest.fixture
def paciente_invalido_email():
    return Paciente("Carlos Souza", "98765432109", "carlosexample.com", "03/03/1980")

@pytest.fixture
def paciente_invalido_nascimento():
    return Paciente("Ana Costa", "45678912301", "ana@example.com", "01/01/3000")

@pytest.fixture
def fila_atendimento():
    return FilaAtendimento()

# Testes para a classe Paciente
class TestPaciente:
    def test_paciente_valido(self, paciente_valido):
        assert paciente_valido.nome == "João Silva"
        assert paciente_valido.cpf == "12345678901"
        assert paciente_valido.email == "joao@example.com"
        assert paciente_valido.nascimento == "01/01/2000"

    def test_paciente_cpf_invalido(self, paciente_invalido_cpf):
        with pytest.raises(ValidacaoError, match="CPF inválido, deve conter 11 dígitos numéricos."):
            paciente_invalido_cpf.validar_cpf(paciente_invalido_cpf.cpf)

    def test_paciente_email_invalido(self, paciente_invalido_email):
        with pytest.raises(ValidacaoError, match="E-mail inválido."):
            paciente_invalido_email.validar_email(paciente_invalido_email.email)

    def test_paciente_nascimento_invalido(self, paciente_invalido_nascimento):
        with pytest.raises(ValidacaoError, match="Data de nascimento inválida, use o formato DD/MM/YYYY."):
            paciente_invalido_nascimento.validar_nascimento(paciente_invalido_nascimento.nascimento)

# Testes para a classe Atendimento
class TestAtendimento:
    def test_atendimento_criacao(self, paciente_valido):
        atendimento = Atendimento(paciente_valido, Risco.VERMELHO)
        assert atendimento.paciente == paciente_valido
        assert atendimento.risco == Risco.VERMELHO
        assert isinstance(atendimento.entrada, datetime)

    def test_atendimento_sem_paciente(self):
        with pytest.raises(ValidacaoError, match="Paciente não registrado"):
            Atendimento(None, Risco.VERDE)

# Testes para a classe FilaAtendimento
class TestFilaAtendimento:
    def test_inserir_e_proximo(self, fila_atendimento, paciente_valido):
        atendimento1 = Atendimento(paciente_valido, Risco.AMARELO)
        atendimento2 = Atendimento(paciente_valido, Risco.VERMELHO)

        fila_atendimento.inserir(atendimento1)
        fila_atendimento.inserir(atendimento2)

        assert fila_atendimento.tamanho() == 2
        assert fila_atendimento.proximo().risco == Risco.VERMELHO  # Prioridade maior
        assert fila_atendimento.proximo().risco == Risco.AMARELO   # Prioridade menor
        assert fila_atendimento.tamanho() == 0

    def test_fila_vazia(self, fila_atendimento):
        with pytest.raises(FilaVaziaError, match="Não tem nenhum paciente na fila de atendimento"):
            fila_atendimento.proximo()

    def test_possui_proximo(self, fila_atendimento, paciente_valido):
        assert not fila_atendimento.possui_proximo()

        atendimento = Atendimento(paciente_valido, Risco.VERDE)
        fila_atendimento.inserir(atendimento)

        assert fila_atendimento.possui_proximo()
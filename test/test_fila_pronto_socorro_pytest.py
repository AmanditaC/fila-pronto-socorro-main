# tests/test_main.py
import pytest  # type: ignore
from main.domain import Paciente, Atendimento, FilaAtendimento, Risco, ValidacaoError

# Testes para RF1 - Registrar Paciente
class TestRegistrarPaciente:
    def test_registro_bem_sucedido(self):
        # Sucesso: O paciente é criado com dados válidos.
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        assert paciente.nome == "João Silva"
        assert paciente.cpf == "12345678901"
        assert paciente.email == "joao@example.com"
        assert paciente.nascimento == "01/01/1990"

    def test_registro_cpf_duplicado(self):
        # Sucesso: A implementação agora verifica CPF duplicado.
        paciente1 = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        with pytest.raises(ValidacaoError) as error:
            paciente2 = Paciente(nome="Maria Oliveira", cpf="12345678901", email="maria@example.com", nascimento="15/05/1985")
        assert "CPF já cadastrado" in str(error.value)

    def test_registro_cpf_invalido(self):
        # Sucesso: O CPF "123" é inválido.
        with pytest.raises(ValidacaoError) as error:
            Paciente(nome="João Silva", cpf="123", email="joao@example.com", nascimento="01/01/1990")
        assert "CPF inválido" in str(error.value)

    def test_registro_email_invalido(self):
        # Sucesso: O e-mail "joao@" é inválido.
        with pytest.raises(ValidacaoError) as error:
            Paciente(nome="João Silva", cpf="12345678901", email="joao@", nascimento="01/01/1990")
        assert "E-mail inválido" in str(error.value)

    def test_registro_data_nascimento_invalida(self):
        # Sucesso: A data "01/01/2100" é inválida.
        with pytest.raises(ValidacaoError) as error:
            Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/2100")
        assert "Data de nascimento inválida" in str(error.value)

# Testes para RF2 - Realizar Triagem
class TestRealizarTriagem:
    def test_triagem_com_sucesso(self):
        # Sucesso: O atendimento é criado com um paciente válido.
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        atendimento = Atendimento(paciente=paciente, risco=Risco.VERMELHO)
        assert atendimento.risco == Risco.VERMELHO

    def test_triagem_sem_paciente_cadastrado(self):
        # Sucesso: A exceção é lançada quando o paciente é None.
        with pytest.raises(ValidacaoError) as error:
            Atendimento(paciente=None, risco=Risco.VERMELHO)
        assert "Paciente não registrado" in str(error.value)

# Testes para RF3 - Gerenciar Fila de Atendimento
class TestGerenciarFilaAtendimento:
    def test_registro_paciente_na_fila(self):
        # Sucesso: O atendimento é inserido na fila.
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        atendimento = Atendimento(paciente=paciente, risco=Risco.VERDE)
        fila = FilaAtendimento()
        fila.inserir(atendimento)
        assert fila.tamanho() == 1

    def test_validacao_dados_antes_registro(self):
        # Sucesso: A exceção é lançada quando o nome está vazio.
        with pytest.raises(ValidacaoError) as error:
            Paciente(nome="", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        assert "Nome inválido" in str(error.value)

    def test_atendimento_ordem_chegada(self):
        # Sucesso: A ordem de atendimento é respeitada.
        paciente1 = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        paciente2 = Paciente(nome="Maria Oliveira", cpf="98765432109", email="maria@example.com", nascimento="15/05/1985")
        atendimento1 = Atendimento(paciente=paciente1, risco=Risco.VERDE)
        atendimento2 = Atendimento(paciente=paciente2, risco=Risco.VERDE)
        fila = FilaAtendimento()
        fila.inserir(atendimento1)
        fila.inserir(atendimento2)
        assert fila.proximo().paciente.nome == "João Silva"
        assert fila.proximo().paciente.nome == "Maria Oliveira"

# Testes para RF4 - Chamar Próximo da Fila
class TestChamarProximoFila:
    def test_chamar_proximo_da_fila(self):
        # Sucesso: O próximo paciente é chamado.
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        atendimento = Atendimento(paciente=paciente, risco=Risco.VERDE)
        fila = FilaAtendimento()
        fila.inserir(atendimento)
        assert fila.proximo().paciente.nome == "João Silva"

    def test_retirar_paciente_da_fila(self):
        # Sucesso: O paciente é retirado da fila.
        paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
        atendimento = Atendimento(paciente=paciente, risco=Risco.VERDE)
        fila = FilaAtendimento()
        fila.inserir(atendimento)
        fila.proximo()
        assert fila.tamanho() == 0
from datetime import datetime
from abc import ABC, abstractmethod, abstractclassmethod

class Cliente():
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
class Conta():

    def __init__(self, numero, cliente):
        self._agencia = '0001'
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
        self._saldo = 0

    @property
    def agencia(self):
        return self._agencia
        
    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @property
    def saldo(self):
        return self._saldo
    
    @abstractclassmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo
        
        if valor <= 0:
            print('Operação falhou! O valor informado é inválido.')

        elif valor - int(valor) != 0:
            print('Operação falhou! Este terminal não opera com moedas.')

        elif saldo < valor:
            print('Operação falhou! Saldo insuficiente.')

        else:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

        return False

    def depositar(self, valor):
        if valor <= 0:
            print('Operação falhou! O valor informado é inválido.')
            
        else:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        
        return False

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def __str__(self):
        return f'''\
            Agência: {self.agencia}
            Conta: {str(self.numero)}
            Titular: {self.cliente.nome}
        '''

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'SAQUE'])

        if numero_saques >= self._limite_saques:
            print(f'Operação falhou! Limite de saques diário excedido ({self._limite}).')

        elif self._limite < valor:
            print(f'Operação falhou! Limite de saques por operação excedido (R$ {self._limite:.2f}).')

        else:
            return super().sacar(valor)
        
        return False
    
    def depositar(self, valor):
        return super().depositar(valor)

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__.upper(),
            'valor': transacao.valor,
            'data': datetime.today().strftime('%d/%m/%Y %H:%M:%S')
        })

class Transacao(ABC):
    @property
    @abstractmethod  
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def criar_menu():
    menu = '\n' + ' MENU '.center(46, '=')
    menu += '''
  Selecione uma opção:

    [1] Deposito
    [2] Saque
    [3] Extrato
    [4] Novo cliente
    [5] Nova conta
    [6] Listar contas

    [0] Encerrar

=> '''
    return menu

def depositar(clientes):
    cpf = input('Informe o CPF (somente números): ')
    
    while not cpf_valido(cpf):
        cpf = input('Informe o CPF (somente números): ')

    cliente = buscar_cliente_por_cpf(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Informe o valor que deseja depósitar: '))
    transacao = Deposito(valor)

    conta = buscar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
        
    cpf = input('Informe o CPF (somente números): ')
    
    while not cpf_valido(cpf):
        cpf = input('Informe o CPF (somente números): ')

    cliente = buscar_cliente_por_cpf(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Informe o valor que deseja sacar: '))
    transacao = Saque(valor)

    conta = buscar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    mensagem = '\n\n' + ' EXTRATO '.center(46, '#')

    cpf = input('Informe o CPF (somente números): ')
    
    while not cpf_valido(cpf):
        cpf = input('Informe o CPF (somente números): ')

    cliente = buscar_cliente_por_cpf(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = buscar_conta_cliente(cliente)

    if not conta:
        return

    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
        extrato += '\n\n' + 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f'\n[{transacao['tipo']}]: R$ {transacao['valor']:.2f} em {transacao['data']}'

    mensagem += extrato
    mensagem += f'\n\nSaldo: R$ {conta.saldo:.2f}'
    mensagem += f'\n\n{''.center(46, '#')}'

    print(mensagem)

def criar_cliente(clientes):
    boas_vindas = '='.center(42, '=')
    boas_vindas += '\n' + 'Bem vindo à criação de clientes!' + '\n'
    boas_vindas += '\n' + 'Por favor nos informe os seguintes dados:' + '\n'

    print(boas_vindas)

    cpf = input('CPF (somente números): ')
    while len(cpf.strip()) == 0:
        cpf = input('CPF (somente números): ')

    if buscar_cliente_por_cpf(cpf, clientes):
        print('O CPF informado já possui cadastro!')
        return
    
    nome = input('Nome completo: ')
    nome = nome.strip().upper()

    data_nascimento = input('Data de nascimento (dd/mm/yyyy): ')
    data_nascimento = data_nascimento.strip()

    logradouro = input('Logradouro (rua): ')
    logradouro = logradouro.strip().upper()

    numero = input('Número: ')
    numero = f', {numero}' if len(numero.strip()) > 0 else ''

    bairro = input('Bairro: ')
    bairro = f' - {bairro.upper()}' if len(bairro.strip()) > 0 else ''
    
    cidade = input('Cidade: ')
    cidade = f' - {cidade.upper()}' if len(cidade.strip()) > 0 else ''

    uf = input('UF: ')
    uf = f'/{uf.upper()}' if len(uf.strip()) > 0 else ''
    
    endereco = f'{logradouro}{numero}{bairro}{cidade}{uf}'

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print(clientes)
    print('Cliente cadastrado com sucesso!')
    
def criar_conta(numero_conta, clientes, contas):
    boas_vindas = '='.center(46, '=')
    boas_vindas += '\n' + '\tBem vindo à criação de contas!' + '\n'
    boas_vindas += '\n' + 'Por favor nos informe os seguintes dados:' + '\n'

    print(boas_vindas)
    
    cpf = input('CPF (somente números): ')
    while len(cpf.strip()) == 0:
        cpf = input('CPF (somente números): ')

    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print('Conta criada com sucesso!', numero_conta)
        return
                
    print('O usuário informado não foi encontrado!')
    
def listar_contas(contas):
    print(contas)
    for conta in contas:
        print(''.center(46, '#'))
        print(str(conta))

def cpf_valido(cpf):
    if len(cpf.strip()) == 0:
        return False

    return True

def buscar_cliente_por_cpf(cpf, clientes):
    cliente_encontrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_encontrado[0] if cliente_encontrado else None

def buscar_conta_cliente(cliente):
    if not cliente.contas:
       print('O cliente informado não possui uma conta ativa!') 
       return

    return cliente.contas[0]   
     
def main():
    contas = []
    clientes = []
    
    while True:
        menu = criar_menu()

        opcao = input(menu)
    
        if opcao == '0':
            print('Obrigado por utilizar nossos serviços. Volte sempre!')
            break
        
        if opcao == '1':
            depositar(clientes)
            
        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            criar_cliente(clientes)

        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == '6':   
            listar_contas(contas)
        
        else:
            print('Opção inválida, por favor selecione novamente a operação desejada.')

main()
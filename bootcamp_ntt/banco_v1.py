from datetime import datetime

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

def criar_menu():
    menu = '\n' + ' MENU '.center(42, '=')
    menu += '''
    Selecione uma opção:

        [1] Deposito
        [2] Saque
        [3] Extrato

        [0] Encerrar

    => '''

    return menu

def selecionar_opcao(operacao):
    global saldo, numero_saques, LIMITE_SAQUES
    valor = float(input(criar_submenu(operacao))) if operacao == '1' or operacao == '2' else print(criar_submenu(operacao))

    if operacao == '1':
        if valor <= 0:
            print('Operação falhou! O valor informado é inválido.')
        else:
            depositar(valor) 
    elif operacao == '2':
        if valor <= 0:
            print('Operação falhou! O valor informado é inválido.')
        elif valor - int(valor) != 0:
            print('Operação falhou! Este terminal não opera com moedas.')
        elif numero_saques >= LIMITE_SAQUES:
            print('Operação falhou! Limite de saques diário excedido (3).')
        elif limite < valor:
            print(f'Operação falhou! Limite de saques por operação excedido (R$ {limite:.2f}).')
        elif saldo < valor:
            print('Operação falhou! Saldo insuficiente.')
        else:
            sacar(valor)

def criar_submenu(opcao):
    mensagem = 'Informe o valor do '

    if opcao == '1':
        mensagem += 'deposito: '
    elif opcao == '2':
        mensagem += 'saque: '
    elif opcao == '3':
        mensagem = '\n\n' + ' EXTRATO '.center(50, '#')
        mensagem += '\n\n' + 'Não foram realizadas movimentações.' if not extrato else extrato
        mensagem += f"\n\nSaldo: R$ {saldo:.2f}"
    elif opcao == '0':
        mensagem = 'Obrigado por utilizar nossos serviços. Volte sempre!'
    else:
        mensagem = 'Operação inválida, por favor selecione novamente a operação desejada.'
    
    return mensagem

def depositar(valor):
    global saldo, extrato
    
    saldo += valor

    extrato += f'\n[DEPÓSITO]: R$ {valor:.2f} em {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}'
    print('Depósito realizado com sucesso!')

def sacar(valor):
    global saldo, extrato, numero_saques
    
    saldo -= valor
    numero_saques += 1

    extrato += f'\n[SAQUE]: R$ {valor:.2f} em {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}'
    print('Saque realizado com sucesso!')

while True:
    opcao = input(criar_menu())
   
    if opcao == '0':
        break
    
    selecionar_opcao(opcao)
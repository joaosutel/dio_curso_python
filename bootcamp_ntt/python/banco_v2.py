from datetime import datetime

def criar_menu():
    menu = '\n' + ' MENU '.center(46, '=')
    menu += '''
  Selecione uma opção:

    [1] Deposito
    [2] Saque
    [3] Extrato
    [4] Novo usuário
    [5] Nova conta
    [6] Listar contas

    [0] Encerrar

=> '''
    return menu

def depositar(saldo, valor, extrato, /):
        
    if valor > 0:
        saldo += valor
        extrato += f'\n[DEPÓSITO]: R$ {valor:.2f} em {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}'

        print('Depósito realizado com sucesso!')
    else:
        print('Operação falhou! O valor informado é inválido.')
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
        
    if valor <= 0:
        print('Operação falhou! O valor informado é inválido.')

    elif valor - int(valor) != 0:
        print('Operação falhou! Este terminal não opera com moedas.')

    elif numero_saques >= limite_saques:
        print('Operação falhou! Limite de saques diário excedido (3).')

    elif limite < valor:
        print(f'Operação falhou! Limite de saques por operação excedido (R$ {limite:.2f}).')

    elif saldo < valor:
        print('Operação falhou! Saldo insuficiente.')
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f'\n[SAQUE]: R$ {valor:.2f} em {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}'
        print('Saque realizado com sucesso!')

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    mensagem = '\n\n' + ' EXTRATO '.center(46, '#')
    mensagem += '\n\n' + 'Não foram realizadas movimentações.' if not extrato else extrato
    mensagem += f'\n\nSaldo: R$ {saldo:.2f}'
    mensagem += f'\n\n{''.center(46, '#')}'

    print(mensagem)

def criar_usuario(usuarios):
    boas_vindas = '='.center(42, '=')
    boas_vindas += '\n' + 'Bem vindo à criação de usuários!' + '\n'
    boas_vindas += '\n' + 'Por favor nos informe os seguintes dados:' + '\n'

    print(boas_vindas)

    cpf = input('CPF (somente números): ')
    while len(cpf.strip()) == 0:
        cpf = input('CPF (somente números): ')

    if buscar_usuario_por_cpf(cpf, usuarios):
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

    usuario = {'cpf': cpf, 'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco}
    usuarios.append(usuario)
    
    print('Usuário cadastrado com sucesso!')
    
def criar_conta(agencia, numero_conta, usuarios, contas):
    boas_vindas = '='.center(46, '=')
    boas_vindas += '\n' + '\tBem vindo à criação de contas!' + '\n'
    boas_vindas += '\n' + 'Por favor nos informe os seguintes dados:' + '\n'

    print(boas_vindas)
    
    cpf = input('CPF (somente números): ')
    while len(cpf.strip()) == 0:
        cpf = input('CPF (somente números): ')

    usuario = buscar_usuario_por_cpf(cpf, usuarios)
    
    if usuario:
        contas.append({'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario})
        print('Conta criada com sucesso!', numero_conta)
        return 1
            
    print('O usuário informado não foi encontrado!')
    return 0

def buscar_usuario_por_cpf(cpf, usuarios):
    usuario_encontrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_encontrado[0] if usuario_encontrado else None
        
def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    usuarios = []
    contas = []
    numero_conta = 1

    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ''

    while True:
        menu = criar_menu()

        opcao = input(menu)
    
        if opcao == '0':
            print('Obrigado por utilizar nossos serviços. Volte sempre!')
            break
        
        if opcao == '1':
            valor = float(input('Informe o valor que deseja depósitar: '))
            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == '2':
            valor = float(input('Informe o valor que deseja sacar: '))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            criar_usuario(usuarios)

        elif opcao == '5':   
            numero_conta += criar_conta(AGENCIA, numero_conta, usuarios, contas) 

        else:
            print('Opção inválida, por favor selecione novamente a operação desejada.')

main()
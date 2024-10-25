from datetime import datetime

def falar_hello_world():
    return "Hello, World!"

def cumprimentar_usuario(nome):
    hora_atual = datetime.now().hour

    if 5 <= hora_atual < 12:
        saudacao = "Bom dia"
    elif 12 <= hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"
    
    return f"{saudacao}, {nome}!"
# Hello!

Este é um pacote Python simples que contém funções para exibir uma saudação "Hello, World!" e cumprimentar o usuário de acordo com o horário atual do sistema.

## Funcionalidades

O pacote possui dois métodos principais:

1. **falar_hello_world**: Retorna a mensagem "Hello, World!".
2. **cumprimentar_usuario**: Retorna uma saudação baseada no horário do sistema, que pode ser:
   - Bom dia (entre 05:00 e 11:59)
   - Boa tarde (entre 12:00 e 17:59)
   - Boa noite (entre 18:00 e 04:59)
   
   A função também exibe o nome do usuário como parte da saudação.

## Instalação

1. Clone este repositório ou faça o download dos arquivos.
2. Navegue até o diretório do pacote e instale-o com o `pip`:

```bash
pip install .
```

## Exemplo de uso
```python
from meu_pacote import falar_hello_world, cumprimentar_usuario

# Exibir 'Hello, World!'
print(falar_hello_world())

# Cumprimentar o usuário com base no horário
print(cumprimentar_usuario("João"))
```

## Exemplo de Saída
Cenário 1: Se for 10h da manhã
```bash
Hello, World!
Bom dia, João!
```

Cenário 2: Se for 20h (8h da noite)
```bash
Hello, World!
Boa noite, João!
```

# Calculadora

#SOMA

def operacao_soma (x,y):
    resultado = x + y
    return resultado



#SUBTRAÇÃO

def operacao_subtracao (x,y):
    return


#MULTIPLICAÇÃO

def operacao_multiplicacao (x,y):
    return


#DIVISÃO

def operacao_divisao (x,y):
    resultado = x / y
    return resultado


#EXPONENCIAÇÃO

def operacao_exponenciacao (x,y):
    resultado = x ** y
    return resultado


#RADICIAÇÃO

def operacao_radicacao (x,y):
    resultado = x ** (1/y)
    return resultado 


#DIVISÃO INTEIRA

def operacao_divisao_inteira (x,y):
    resultado = x // y
    return resultado


#RESTO

def operacao_resto (x,y):
    resultado = x % y
    return resultado


#PERCENTUAL

def operacao_percentual (x,y):
    resultado = (x/100) * y
    return resultado


#BP

while True:
    escolha = input("""\nEscolha uma das opções abaixo: 
\n1 - Soma
\n2 - Subtração
\n3 - Multiplicação
\n4 - Divisão
\n5 - Exponenciação
\n6 - Radiciação
\n7 - Divisão Inteira
\n8 - Resto
\n9 - Percentual
\n0 - Sair do Programa
\n""")
    x = float(input("Digite o primeiro número: "))
    y = float(input("Digite o segundo número: "))

    if escolha == "1":    
        resultado = operacao_soma(x,y)
        print(f"\nO resultado da soma é: {resultado}")

    elif escolha == "2":
        resultado = operacao_subtracao(x,y)
        print(f"O resultado da subtração é: {resultado}")

    elif escolha == "3":
        resultado = operacao_multiplicacao(x,y)
        print(f"O resultado da multiplicação é: {resultado}")

    elif escolha == "4":
        resultado = operacao_divisao(x,y)
        print(f"O resultado da divisão é: {resultado}")

    elif escolha == "5":
        resultado = operacao_exponenciacao(x,y)
        print(f"O resultado da exponenciação é: {resultado}")

    elif escolha == "6":
        resultado = operacao_radicacao(x,y)
        print(f"O resultado da radiciação é: {resultado}")

    elif escolha == "7":
        resultado = operacao_divisao_inteira(x,y)
        print(f"O resultado da divisão inteira é: {resultado}")

    elif escolha == "8":    
        resultado = operacao_resto(x,y)
        print(f"O resultado do resto da divisão é: {resultado}")

    elif escolha == "9":
        resultado = operacao_percentual(x,y)
        print(f"O resultado do percentual é: {resultado}")

    elif escolha == "0":
        print("Saindo do programa...")
        break

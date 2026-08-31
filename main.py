# Calculadora

#SOMA

def operacao_soma (x,y):
    return


#SUBTRAÇÃO

def operacao_subtracao (x,y):
    return


#MULTIPLICAÇÃO

def operacao_multiplicacao (x,y):
    return


#DIVISÃO

def operacao_divisao (x,y):
    return


#EXPONENCIAÇÃO

def operacao_exponenciacao (x,y):
    return


#RADICIAÇÃO

def operacao_radicacao (x,y):
    return  


#DIVISÃO INTEIRA

def operacao_divisao_inteira (x,y):
    return  


#RESTO

def operacao_resto (x,y):
    return


#PERCENTUAL

def operacao_percentual (x,y):
    return  


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
    if escolha == "1":
        x = float(input("Digite o primeiro número: "))
        y = float(input("Digite o segundo número: "))
        resultado = operacao_soma(x,y)
        print(f"\nO resultado da soma é: {resultado}")
    elif escolha == "2":
        x = float(input("Digite o primeiro número: "))
        y = float(input("Digite o segundo número: "))
        resultado = operacao_subtracao(x,y)
        print(f"O resultado da subtração é: {resultado}")
    elif escolha == "3":
        x = float(input("Digite o primeiro número: "))
        y = float(input("Digite o segundo número: "))
        resultado = operacao_multiplicacao(x,y)
        print(f"O resultado da multiplicação é: {resultado}")
    elif escolha == "4":
        x = float(input("Digite o primeiro número: "))
        y = float(input("Digite o segundo número: "))
        resultado = operacao_divisao(x,y)
        print(f"O resultado da divisão é: {resultado}")
    elif escolha == "5":
        x = float(input("Digite a base: "))
        y = float(input("Digite o expoente: "))
        resultado = operacao_exponenciacao(x,y)
        print(f"O resultado da exponenciação é: {resultado}")
    elif escolha == "6":
        x = float(input("Digite o número: "))
        y = float(input("Digite o índice da raiz: "))
        resultado = operacao_radicacao(x,y)
        print(f"O resultado da radiciação é: {resultado}")
    elif escolha == "7":
        x = float(input("Digite o dividendo: "))
        y = float(input("Digite o divisor: "))
        resultado = operacao_divisao_inteira(x,y)
        print(f"O resultado da divisão inteira é: {resultado}")
    elif escolha == "8":    
        x = float(input("Digite o dividendo: "))
        y = float(input("Digite o divisor: "))
        resultado = operacao_resto(x,y)
        print(f"O resultado do resto da divisão é: {resultado}")
    elif escolha == "9":
        x = float(input("Digite o valor total: "))
        y = float(input("Digite a porcentagem: "))
        resultado = operacao_percentual(x,y)
        print(f"O resultado do percentual é: {resultado}")
    elif escolha == "0":
        print("Saindo do programa...")
        break

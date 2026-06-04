# Faça um programa que simule um banco, use listas com os seguintes formatos:
#conta=[nib,codigoacesso,nome,saldo,ativo]= [1,1234,"Paulo",100,1]
#movimento[codigo,movimento] [1,-10] [1,20]
# crie menu com 1)levantamenos 2)depositos 3)ver saldo etc  

def create_user():
    lista_credenciais = []

    nome = input("Escreva o seu nome: ")
    password = input("Escreva a sua passowrd: ")
    nib = int(input("Insira o seu NIB: "))
    saldo = int(input("Insira o seu saldo, mas nao penses que és rico: "))
    lista_mov = []
    
    lista_credenciais = [nome, password,nib,saldo,lista_mov]
    print(lista_credenciais)
    login(lista_credenciais)

    return lista_credenciais

def login(lista):
    
    tentativas_username = 3
    tentativas_password = 3
    
    while tentativas_username != 0:
        nome = input("Escreva o seu nome: ")
        if nome != lista[0]:
            input(f"Escreveu nome errado. Tem mais {tentativas_username-1} tentativas.")
            tentativas_username -=1
        else:
            print("Username correto!")
            break
    
    if tentativas_username == 0:
            print("Xau Laura. Aqui nao entras mais. ")
            exit()
    
    while tentativas_password != 0:
        password = input("Escreva a sua password: ")
        if password != lista[1]:
            input(f"Escreveu password. Tem mais {tentativas_password-1} tentativas.")
            tentativas_password -=1
        else:
            print("Login correto!")
            break
    
    if tentativas_password == 0:
            print("Não te lembras da pass. Come menos queijo.")
            exit()
    
    menu(lista)

def menu(lista):
    # crie menu com 1)levantamenos 2)depositos 3)ver saldo etc  
    print("\nBem vindo à sua app do Banco")
    print("=========MENU===============")
    print("1 - Ver Conta")
    print("2 - Levantamentos")
    print("3 - Depositos")
    print("4 - Ver Saldo")
    print("5 - Ver movimentos")
    print("Prima 0 para sair")
    escolha = int(input("Escolha uma das opções: "))

    
    if escolha == 1:
        ver_conta(lista)
    elif escolha == 2:
        levantamento(lista)
    elif escolha == 3:
        deposito(lista)
    elif escolha == 4:
        consultar_saldo(lista)
    elif escolha == 5:
        ver_movimentos(lista)
    elif escolha == 0:
        exit()


def ver_conta(lista):
    
    while True:

        print("\nDados da sua conta:")
        print("Nib:", lista[0])
        print("Codigo Acesso:", lista[1])
        print("Nome:", lista[2])
        print("Saldo:", lista[3],"\n")
        
        voltar = input("Prima m para retornar o menu: ").lower() 
        if voltar == "m":
            menu(lista)
            break

    return lista

def levantamento(lista):
    
    while True:
        movimentos = lista[4]
        saldo = lista[3]

        if saldo <= 0:
            print("Oh morcao, nao tens dinheiro moçooo")
        else:
            valor = int(input("Digite o valor que quer levantar: "))
            saldo = saldo - valor
            update_saldo(lista,saldo)
            valor_neg = valor * (-1)
            movimentos.append(valor_neg)
            

        print("O seu saldo atual é:", saldo)
        update_saldo(lista,saldo)

        voltar = input("Prima m para retornar o menu: ").lower() 
        if voltar == "m":
            menu(lista)
            break

    return saldo

def deposito(lista):
    while True:
        movimentos = lista[4]

        saldo = lista[3]
        valor = int(input("Digite o valor que quer depositar: "))
        saldo = saldo + valor
        print("O seu saldo atual é:", saldo)
        update_saldo(lista,saldo)
        
        movimentos.append(valor)
    
        voltar = input("Prima m para retornar o menu: ").lower()
        if voltar == "m":
            menu(lista)
            break

    print("O seu saldo atual é:", saldo)
    return saldo

def consultar_saldo(lista):
    while True:
        print("Saldo: ", lista[3])
        voltar = input("Prima m para retornar o menu: ").lower() 
        
        if voltar == "m":
            menu(lista)
            break

def update_saldo(lista,novo_saldo):
    lista[3] = novo_saldo
    return novo_saldo

def ver_movimentos(lista):
    while True:
        movimentos = lista[4]

        if movimentos == []:
            print("Ainda nao foram efetuados movimentos.")
        else:
            for mov in movimentos:
                if mov > 0:
                    print(f"Depósito: +{mov}")
                else:
                    print(f"Levantamento: {mov}")
            
            print(movimentos)

        voltar = input("Prima m para retornar o menu: ").lower() 
        
        if voltar == "m":
            menu(lista)
            break

create_user()
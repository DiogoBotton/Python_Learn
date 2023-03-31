from random import randint

print("Grupo 2: \nDiogo Botton\nFelipe Katayama\nKalli Yuka\nLeonardo Cardenas\nWilian Barbosa\n")
print("Questão 2\n")

minValido = False
maxValido = False

while not minValido:
    min = input("Digite o número mínimo: ")

    try:
        min = int(min)
        minValido = True
    except:
        print("ERRO: Valor digitado não é um valor válido.\n")

while not maxValido:
    max = input("Digite o número máximo: ")

    try:
        max = int(max)
        if max <= min:
            print("Número máximo não pode ser menor ou igual ao número mínimo.\n")
            continue
        
        maxValido = True
    except:
        print("ERRO: Valor digitado não é um valor válido.\n")

intervalo = (min,max)
finalizarJogo = False
isPlayer = False
modoJogo = -1

while not finalizarJogo:
    print("|","-" * 40,"|")
    print("| Seja bem vindo ao jogo de apostas!")
    print("| Escolha o modo de jogo:")
    print("| 1 - Para jogar com o computador")
    print("| 2 - Para jogar com dois jogadores")
    print("| 0 - Para sair")
    print("|","-" * 40,"|\n")

    modoJogo = input("Digite o número correspondente ao modo de jogo ou sair: ")
    
    match modoJogo:
        case "0":
            finalizarJogo = True
        case "1":
            print("Você escolheu jogar com o computador\n")
            numSorteado = randint(intervalo[0], intervalo[1])
            #TODO
        case "2":
            print("Você escolheu jogar com dois jogadores.\n")
            print("Jogador 1 Será quem escolherá o número")
            print("Jogador 2 Será quem adivinhará o número\n")
            
            numValido = False
            while not numValido:
                numSorteado = input("Jogador 1: Escolha um número de {} à {}: ".format(intervalo[0], intervalo[1]))
                try:
                    numSorteado = int(numSorteado)
                    if numSorteado < intervalo[0] or numSorteado > intervalo[1]:
                        print("ERRO: Número não pode ser menor que {} ou maior que {}\n".format(intervalo[0], intervalo[1]))
                        continue

                    numValido = True
                    print("\n"*1000)
                except:
                    print("ERRO: Valor digitado não é um valor válido.\n")
            #TODO
        case _:
            print("ERRO: Valor digitado não é um valor válido.\n")
            input("Enter para continuar")
            continue
    
    finalizarJogo = True
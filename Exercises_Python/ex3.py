arrayString = []
N = 1
finalizar = False

while not finalizar:
    N = input("Digite o tamanho do losângulo (de [6-32]): ")
    print("\"0\" para sair.\n")

    try:
        N = int(N)
    except:
        print("ERRO: Valor digitado não é um valor válido.\n")
        continue

    if N == 0:
        finalizar = True
        continue

    if (N < 6 or N > 32) or N % 2 != 0:
        print("ERRO: Número Inválido.\nDigite um número par, maior ou igual à 6 e menor ou igual à 32.\n")
        continue
    
    cont = 0
    index = -1
    linhas = N-1
    while cont < (N / 2):
        newStr = ""
        indexList = []
        if cont == 0 or cont == N - 1:
            index = (N / 2) -1
        else:
            index -= 1
            
        indexList.append(index)
        indexList.append(index+1)
        indexList.append(linhas - index)
        indexList.append((linhas - index) -1)

        for i in range(0, N):
            if i in indexList:
                newStr += "*"
            else:
                newStr += " "
        
        arrayString.append(newStr)
        cont += 1
    
    finalizar = True
    
for s in arrayString:
    print(s)

linhas = int(N/2)
cont = linhas
while cont > 0:
    if cont != linhas:
        print(arrayString[cont-1])
    cont -= 1
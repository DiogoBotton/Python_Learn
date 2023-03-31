print("Grupo 2: \nDiogo Botton\nFelipe Katayama\nKalli Yuka\nLeonardo Cardenas\nWilian Barbosa\n")
print("Questão 1\n")
minValido = False
maxValido = False
numPrimos = []

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

for num in range(min, max+1):
    if num == 2:
        numPrimos.append(num)
    elif num % 2 != 0:
        resto = 1
        i = 3
        raiz = num ** 0.5
        while i <= raiz and resto != 0:
            resto = num % i
            i = i + 2
        if resto != 0:
            numPrimos.append(num)

print("Quantidade de primos no intervalo: ", numPrimos, " = ", len(numPrimos))

somaPrimos = 0
for primo in numPrimos:
    somaPrimos += primo

print("Soma dos primos no intervalo: ", somaPrimos)
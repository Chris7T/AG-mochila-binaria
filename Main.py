import numpy as np

itemGeral = []

f = open("itens.txt", "r")
for x in f:
    result = x.split(";")
    itemGeral.append([int(result[1]), int(result[2])])
itemGeral = np.array(itemGeral)


def criarPrimeiraPop(tamanhoPopulacao, genesTamanho):
    pop = np.zeros((tamanhoPopulacao, genesTamanho), int)
    for i in range(len(pop)):
        peso = 0
        for j in range(genesTamanho):
            chance = np.random.randint(0, 2)
            if chance:
                if peso+itemGeral[j][0] <= 400:
                    pop[i][j] = 1
                    peso = peso+itemGeral[j][0]
    return pop


def fitness(pop):
    fitness = []
    for i in range(len(pop)):
        fitness.append(np.sum(pop[i]*itemGeral[:, 1]))
    return np.asarray(fitness)


def pesoTotal(pop):
    peso = []
    for i in range(len(pop)):
        peso.append(np.sum(pop[i]*itemGeral[:, 0]))
    return peso


def selecao(pop, fitness, k):
    selecionados = []
    while(len(selecionados) < len(pop)-20):
        i = np.random.randint(len(pop)-1)
        random = np.random.randint(100)
        if fitness[i] < fitness[i+1]:
            if random < k:
                selecionados.append(pop[i+1])
            else:
                selecionados.append(pop[i])
        else:
            if random < k:
                selecionados.append(pop[i])
            else:
                selecionados.append(pop[i+1])
    return np.asarray(selecionados)


def pegarElite(fitness):
    elite = np.copy(fitness)
    elite = elite[0:20]
    return elite


def pesoTotalIndividuo(individuo):
    peso = 0
    for j in range(len(individuo)):
        if individuo[j]:
            peso = peso+itemGeral[j][0]
    return peso


def retirarAleatorio(individuo):
    while(1):
        valor = np.random.randint(100)
        if individuo[valor]:
            individuo[valor] = 0
            break


def remocaoPeso(filhos, genesTamanho):
    for i in range(len(filhos)):
        while(pesoTotalIndividuo(filhos[i]) > 400):
            retirarAleatorio(filhos[i])
    return filhos


def cruzamento(selecionados, chance):
    qtSelecionados = len(selecionados)
    filhos = np.zeros((qtSelecionados, 100), int)
    par = 0
    while par < qtSelecionados:
        if np.random.randint(100) < chance and par+1 < qtSelecionados:
            corte = np.random.randint(100)
            filhos[par, 0:corte] = selecionados[par, 0:corte]
            filhos[par, corte:100] = selecionados[par+1, corte:100]
            filhos[par+1, 0:corte] = selecionados[par+1, 0:corte]
            filhos[par+1, corte:100] = selecionados[par, corte:100]
            par = par + 2
        else:
            par = par + 1
    return remocaoPeso(filhos, 100)


def mutacao(selecionados, chance):
    for i in range(len(selecionados)):
        if np.random.randint(100) < 10:
            j = np.random.randint(100)
            if selecionados[i, j]:
                selecionados[i, j] = 0
            else:
                selecionados[i, j] = 1
    return remocaoPeso(selecionados, 100)


def ordenar(pop, fit):
    ordenado = np.asarray(fit)
    ordenado = ordenado.argsort()
    return pop[ordenado[::-1]], fit[ordenado[::-1]]


def rodando(geracaoMax, tamanhoPopulacao):
    geracao = 0
    popu = criarPrimeiraPop(tamanhoPopulacao, 100)
    while(geracao < geracaoMax):
        geracao = geracao+1
        fit = fitness(popu)
        popu, fit = ordenar(popu, fit)
        elite = pegarElite(popu)
        peso = pesoTotal(popu)
        selecionados = selecao(popu, fit, 75)
        selecionados = cruzamento(selecionados, 90)
        selecionados = mutacao(selecionados, 90)
        popu = np.concatenate(
            (np.asarray(elite), np.asarray(selecionados)), axis=0)
        print(fit[0], peso[0])


rodando(800, 400)

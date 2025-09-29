import random
import math
import copy

# ======================================================
# Funções auxiliares para o Problema do Caixeiro Viajante
# ======================================================

def distancia_euclidiana(cidade1, cidade2):
    """
    Calcula a distância euclidiana entre duas cidades.
    Cada cidade é representada como uma tupla (x, y).
    """
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)


def calcular_custo(rotas, distancias):
    """
    Calcula o custo total de uma solução (rota completa).
    :param rotas: lista representando a ordem das cidades visitadas
    :param distancias: matriz de distâncias pré-calculada
    :return: custo total da rota
    """
    custo = 0
    for i in range(len(rotas) - 1):
        custo += distancias[rotas[i]][rotas[i+1]]
    # adiciona a volta à cidade inicial
    custo += distancias[rotas[-1]][rotas[0]]
    return custo


def gerar_matriz_distancias(cidades):
    """
    Gera a matriz de distâncias entre todas as cidades.
    """
    n = len(cidades)
    matriz = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matriz[i][j] = distancia_euclidiana(cidades[i], cidades[j])
    return matriz

# ======================================================
# Construção da solução inicial - Fase Gulosa Randomizada
# ======================================================

def construir_solucao(distancias, alpha=0.3):
    """
    Constrói uma solução inicial utilizando um método guloso randomizado.
    :param distancias: matriz de distâncias
    :param alpha: parâmetro de controle de aleatoriedade (0=guloso puro, 1=aleatório puro)
    :return: solução inicial (rota)
    """
    n = len(distancias)
    solucao = []
    nao_visitados = list(range(n))
    
    # começa por uma cidade aleatória
    cidade_atual = random.choice(nao_visitados)
    solucao.append(cidade_atual)
    nao_visitados.remove(cidade_atual)
    
    while nao_visitados:
        # ordena próximos candidatos pelo custo
        custos = [(cidade, distancias[cidade_atual][cidade]) for cidade in nao_visitados]
        custos.sort(key=lambda x: x[1])
        
        # cria a lista restrita de candidatos (RCL)
        limite = int(len(custos) * alpha) + 1
        rcl = custos[:limite]
        
        # escolhe aleatoriamente dentro da RCL
        cidade_escolhida = random.choice(rcl)[0]
        solucao.append(cidade_escolhida)
        nao_visitados.remove(cidade_escolhida)
        cidade_atual = cidade_escolhida
    
    return solucao

# ======================================================
# Busca Local (2-opt)
# ======================================================

def busca_local(solucao, distancias):
    """
    Aplica a heurística 2-opt para melhorar uma solução.
    """
    melhor = solucao
    melhor_custo = calcular_custo(melhor, distancias)
    melhorou = True
    
    while melhorou:
        melhorou = False
        for i in range(1, len(solucao) - 2):
            for j in range(i+1, len(solucao)):
                if j - i == 1: 
                    continue
                nova_solucao = melhor[:]
                # inverte a subsequência entre i e j
                nova_solucao[i:j] = melhor[j-1:i-1:-1]
                novo_custo = calcular_custo(nova_solucao, distancias)
                if novo_custo < melhor_custo:
                    melhor = nova_solucao
                    melhor_custo = novo_custo
                    melhorou = True
        solucao = melhor
    return melhor

# ======================================================
# Perturbação (Busca Local Iterada)
# ======================================================

def perturbar(solucao):
    """
    Aplica uma perturbação simples trocando duas cidades de posição.
    """
    nova = solucao[:]
    i, j = random.sample(range(len(solucao)), 2)
    nova[i], nova[j] = nova[j], nova[i]
    return nova

# ======================================================
# GRASP com Busca Local Iterada
# ======================================================

def grasp(distancias, iteracoes=50, alpha=0.3):
    """
    Implementação do algoritmo GRASP com Busca Local Iterada.
    :param distancias: matriz de distâncias
    :param iteracoes: número de iterações
    :param alpha: parâmetro de controle da fase gulosa randomizada
    :return: melhor solução encontrada e seu custo
    """
    melhor_solucao = None
    melhor_custo = float("inf")
    
    for it in range(iteracoes):
        # fase de construção
        solucao = construir_solucao(distancias, alpha)
        
        # busca local
        solucao = busca_local(solucao, distancias)
        custo = calcular_custo(solucao, distancias)
        
        # busca local iterada: aplica perturbação e refina
        solucao_perturbada = perturbar(solucao)
        solucao_perturbada = busca_local(solucao_perturbada, distancias)
        custo_perturbado = calcular_custo(solucao_perturbada, distancias)
        
        # escolhe a melhor entre as duas
        if custo_perturbado < custo:
            solucao, custo = solucao_perturbada, custo_perturbado
        
        # atualiza melhor global
        if custo < melhor_custo:
            melhor_solucao = solucao
            melhor_custo = custo
    
    return melhor_solucao, melhor_custo

# ======================================================
# Exemplo de uso
# ======================================================

if __name__ == "__main__":
    # Define 10 cidades com coordenadas aleatórias
    cidades = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    
    # Gera a matriz de distâncias
    distancias = gerar_matriz_distancias(cidades)
    
    # Executa o GRASP
    melhor_rota, melhor_custo = grasp(distancias, iteracoes=100, alpha=0.3)
    
    print("Melhor rota encontrada:", melhor_rota)
    print("Custo da melhor rota:", melhor_custo)

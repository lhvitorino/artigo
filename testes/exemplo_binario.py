from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary

# Definir os dados (exemplo simples)
valores = [10, 40, 30, 50]  # valores dos itens
pesos = [5, 8, 7, 6]        # pesos dos itens
peso_maximo = 15            # restrição de peso máximo

# Definir o problema de otimização (maximização)
problema = LpProblem("Problema_da_Mochila", LpMaximize)

# Definir variáveis de decisão binárias (0 ou 1) para cada item
x = [LpVariable(f'x{i}', cat=LpBinary) for i in range(len(valores))]

# Definir a função objetivo (maximizar o valor dos itens selecionados)
problema += lpSum(valores[i] * x[i] for i in range(len(valores))), "Função Objetivo"

# Adicionar a restrição de peso (soma dos pesos dos itens selecionados <= peso máximo)
problema += lpSum(pesos[i] * x[i] for i in range(len(pesos))) <= peso_maximo, "Restrição de Peso"

# Resolver o problema
problema.solve()

# Exibir os resultados
print("Status:", problema.status)
for i in range(len(valores)):
    print(f'Item {i}: Selecionado = {x[i].varValue}')

# Exibir o valor da função objetivo (valor total dos itens selecionados)
print(f'Valor total dos itens selecionados: {problema.objective.value()}')

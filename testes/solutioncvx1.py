import cvxpy as cp
import numpy as np

# Parâmetros
Dmi = np.array([300, 320, 310, 305, 315, 300, 330, 340, 320, 310, 300, 315])  # Exemplo de demanda para 12 meses

# Variáveis de decisão
DC = cp.Variable(integer=True)  # DC deve ser inteiro
a = cp.Variable(12, boolean=True)  # Variáveis binárias a_i para cada mês
b = cp.Variable(12, boolean=True)  # Variáveis binárias b_i para cada mês

# Função objetivo
objective = cp.Minimize(cp.sum((Dmi - DC) * b + (DC - Dmi) * a))

# Restrições
constraints = []

# Valor grande M (suficientemente grande)
M = 10000  # Um valor grande para a técnica de grande-M

# Adicionar restrições para a_i e b_i
for i in range(12):
    # Restrições para b_i: b_i = 1 se Dmi[i] > 1.05 * DC
    constraints.append(Dmi[i] - 1.05 * DC <= M * (1 - b[i]))  # Garante que b_i = 1 se Dmi[i] > 1.05 * DC
    constraints.append(Dmi[i] - 1.05 * DC >= -M * b[i])  # Garante que b_i = 0 se Dmi[i] <= 1.05 * DC

    # Restrições para a_i: a_i = 1 se Dmi[i] < DC
    constraints.append(DC - Dmi[i] <= M * (1 - a[i]))  # Garante que a_i = 1 se Dmi[i] < DC
    constraints.append(DC - Dmi[i] >= -M * a[i])  # Garante que a_i = 0 se Dmi[i] >= DC

# Resolver o problema
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.CBC)  # Usar o solver GLPK_MI para programação inteira mista

# Exibir resultados
print("Status:", problem.status)
print(f"Valor de DC: {DC.value}")
for i in range(12):
    print(f"a_{i}: {a[i].value}, b_{i}: {b[i].value}")

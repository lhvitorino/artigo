import pulp
import numpy as np

# Dados
gFV = np.array([152.68, 141.88, 122.65, 98.17, 79.38, 66.95, 70.22, 88.64, 92.60, 113.54, 144.06, 156.40])
dL = np.array([2471.04, 2799.36, 4155.84, 1900.80, 1010.88, 959.04, 915.84, 794.88, 820.80, 1019.52, 1028.16, 1200.96])
dMi = dL - gFV
n = len(dMi)
Tc = 22.16
Ts = 18.40

# Variáveis de decisão
dC1 = pulp.LpVariable('dC1', lowBound=0, upBound=4800, cat='Integer')
dC2 = pulp.LpVariable('dC2', lowBound=0, upBound=4800, cat='Integer')
dC3 = pulp.LpVariable('dC3', lowBound=0, upBound=4800, cat='Integer')
dC4 = pulp.LpVariable('dC4', lowBound=0, upBound=4800, cat='Integer')

# Criação do problema de minimização
prob = pulp.LpProblem("Minimizar Custo", pulp.LpMinimize)

# Variáveis binárias
bsub = [pulp.LpVariable(f'bsub_{i}', cat='Binary') for i in range(n)]
bsob = [pulp.LpVariable(f'bsob_{i}', cat='Binary') for i in range(n)]
bsut = [pulp.LpVariable(f'bsut_{i}', cat='Binary') for i in range(n)]
bsot = [pulp.LpVariable(f'bsot_{i}', cat='Binary') for i in range(n)]


# Variáveis auxiliares
z_sub = [pulp.LpVariable(f'z_sub_{i}', lowBound=0) for i in range(n)]
z_sob = [pulp.LpVariable(f'z_sob_{i}', lowBound=0) for i in range(n)]
z_sut = [pulp.LpVariable(f'z_sut_{i}', lowBound=0) for i in range(n)]
z_sot = [pulp.LpVariable(f'z_sot_{i}', lowBound=0) for i in range(n)]

# Função objetivo
prob += pulp.lpSum([(z_sub[i] * 2 * Tc) + (z_sob[i] * Ts) + (z_sut[i] * 2 * Tc) + (z_sot[i] * Ts) for i in range(n)])

# Restrições de acréscimo e decréscimos de demanda

prob += dC2 >= 1.05 * dC1 # Segundo período deve subir 5% em relação ao primeiro para configurar período de teste
prob += dC3 >= 30 # demanda minima contratada na redução deve ser maior que 30kW
prob += dC4 >= 1.05 * dC3 # Quarto período deve subir 5% em relação ao terceiro para configurar período de teste

# Restrições para variáveis binárias e auxiliares
M = 1000000  # Constante Big-M

for i in range(n):
    if i >= 0 and i <= 2:
        # Linearização das condições para bsub:
        # Se dMi >= 1.05 * dC1, então bsub = 1, senão bsub = 0
        prob += dMi[i] - 1.05 * dC1 >= -M * (1 - bsub[i])
        prob += dMi[i] - 1.05 * dC1 <= M * bsub[i]
    
        # Linearização das condições para bsob:
        # Se dmi < dC3, então bsob = 1, senão bsob = 0
        prob += dC1 - dMi[i] >= -M * (1 - bsob[i])
        prob += dC1 - dMi[i] <= M * bsob[i]

        # Definir as variáveis auxiliares
        prob += z_sub[i] <= (dMi[i] - dC1) + M * (1 - bsub[i])  # z_sub = (dMi - dC1) * 2 * Tc * bsub
        prob += z_sub[i] >= (dMi[i] - dC1) - M * (1 - bsub[i])
        prob += z_sub[i] <= M * bsub[i]
    
        prob += z_sob[i] <= (dC1 - dMi[i]) + M * (1 - bsob[i])  # z_sob = (dC1 - dMi) * Ts * bsob
        prob += z_sob[i] >= (dC1 - dMi[i]) - M * (1 - bsob[i])
        prob += z_sob[i] <= M * bsob[i]

    if i >= 3 and i <= 5:
        # Linearização das condições para bsut:
        # Se dMi >= dC2 + 0.3 * (dC2 - dC1) + 0.05 * dC1, então bsut = 1, senão bsut = 0
        prob += dMi[i] - dC2 + 0.3 * (dC2 - dC1) + 0.05 * dC1 >= -M * (1 - bsut[i])
        prob += dMi[i] - dC2 + 0.3 * (dC2 - dC1) + 0.05 * dC1 <= M * bsut[i]
    
        # Linearização das condições para bsot:
        # Se dmi < dC1, então bsot = 1, senão bsot = 0
        prob += dC1 - dMi[i] >= -M * (1 - bsot[i])
        prob += dC1 - dMi[i] <= M * bsot[i]

        # Definir as variáveis auxiliares
        prob += z_sut[i] <= (dMi[i] - dC2) + M * (1 - bsut[i])  # z_sut = (dMi - dC2) * 2 * Tc * bsut
        prob += z_sut[i] >= (dMi[i] - dC2) - M * (1 - bsut[i])
        prob += z_sut[i] <= M * bsut[i]
    
        prob += z_sot[i] <= (dC1 - dMi[i]) + M * (1 - bsot[i])  # z_sot = (dC1 - dMi) * Ts * bsot
        prob += z_sot[i] >= (dC1 - dMi[i]) - M * (1 - bsot[i])
        prob += z_sot[i] <= M * bsot[i]

    if i >= 6 and i <= 8:
         # Linearização das condições para bsub:
        # Se dMi >= 1.05 * dC3, então bsub = 1, senão bsub = 0
        prob += dMi[i] - 1.05 * dC3 >= -M * (1 - bsub[i])
        prob += dMi[i] - 1.05 * dC3 <= M * bsub[i]
    
        # Linearização das condições para bsob:
        # Se dMi < dC3, então bsob = 1, senão bsob = 0
        prob += dC3 - dMi[i] >= -M * (1 - bsob[i])
        prob += dC3 - dMi[i] <= M * bsob[i]

        # Definir as variáveis auxiliares
        prob += z_sub[i] <= (dMi[i] - dC3) + M * (1 - bsub[i])  # z_sub = (dMi - dC3) * 2 * Tc * bsub
        prob += z_sub[i] >= (dMi[i] - dC3) - M * (1 - bsub[i])
        prob += z_sub[i] <= M * bsub[i]
    
        prob += z_sob[i] <= (dC3 - dMi[i]) + M * (1 - bsob[i])  # z_sob = (dC3 - dMi) * Ts * bsob
        prob += z_sob[i] >= (dC3 - dMi[i]) - M * (1 - bsob[i])
        prob += z_sob[i] <= M * bsob[i]
    
    if i >= 9 and i <= 11:
        # Linearização das condições para bsut:
        # Se dMi >= dC4 + 0.3 * (dC4 - dC3) + 0.05 * dC3, então bsut = 1, senão bsut = 0
        prob += dMi[i] - dC4 + 0.3 * (dC4 - dC3) + 0.05 * dC3 >= -M * (1 - bsut[i])
        prob += dMi[i] - dC4 + 0.3 * (dC4 - dC3) + 0.05 * dC3 <= M * bsut[i]
    
        # Linearização das condições para bsot:
        # Se dmi < dC3, então bsot = 1, senão bsot = 0
        prob += dC3 - dMi[i] >= -M * (1 - bsot[i])
        prob += dC3 - dMi[i] <= M * bsot[i]

        # Definir as variáveis auxiliares
        prob += z_sut[i] <= (dMi[i] - dC4) + M * (1 - bsut[i])  # z_sut = (dMi - dC4) * 2 * Tc * bsut
        prob += z_sut[i] >= (dMi[i] - dC4) - M * (1 - bsut[i])
        prob += z_sut[i] <= M * bsut[i]
    
        prob += z_sot[i] <= (dC3 - dMi[i]) + M * (1 - bsot[i])  # z_sot = (dC3 - dMi) * Ts * bsot
        prob += z_sot[i] >= (dC3 - dMi[i]) - M * (1 - bsot[i])
        prob += z_sot[i] <= M * bsot[i]

# Resolver o problema
prob.solve()

# Ver resultados
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Valor de dC1: {pulp.value(dC1)}")
print(f"Valor de dC2: {pulp.value(dC2)}")
print(f"Valor de dC3: {pulp.value(dC3)}")
print(f"Valor de dC4: {pulp.value(dC4)}")

for i in range(n):
    print(f"Mês {i+1}: bsub = {pulp.value(bsub[i])}, bsob = {pulp.value(bsob[i])}, bsut = {pulp.value(bsut[i])}, bsot = {pulp.value(bsot[i])}")
    print(f"Mês {i+1}: z_sub = {pulp.value(z_sub[i])}, z_sob = {pulp.value(z_sob[i])}, z_sut = {pulp.value(z_sut[i])}, z_sot = {pulp.value(z_sot[i])}")

import pulp

# Define the problem
model = pulp.LpProblem("Minimize_DC_Problem", pulp.LpMinimize)

# Define the variables
b = pulp.LpVariable.dicts("b", range(12), 0, 1, pulp.LpBinary)
a = pulp.LpVariable.dicts("a", range(12), 0, 1, pulp.LpBinary)
DC = pulp.LpVariable("DC", lowBound=0, cat='Integer')

# Auxiliary variables for linearization
y_b = pulp.LpVariable.dicts("y_b", range(12), lowBound=0, cat='Continuous')
y_a = pulp.LpVariable.dicts("y_a", range(12), lowBound=0, cat='Continuous')

# Define Dm as a parameter (list of 12 values as an example)
Dm = [100, 200, 250]  # You should replace these with actual values
n = len(Dm)

# Objective function
model += pulp.lpSum([y_b[i] * 2 + y_a[i] for i in range(n)])

# Add constraints to linearize y_b[i] = (Dm[i] - DC) * b[i]
for i in range(n):
    model += y_b[i] >= (Dm[i] - DC) - (1 - b[i]) * 1000  # Big M constraint
    model += y_b[i] <= (Dm[i] - DC) + (1 - b[i]) * 1000  # Big M constraint
    model += y_b[i] <= b[i] * 1000
    model += y_b[i] >= 0

# Add constraints to linearize y_a[i] = (DC - Dm[i]) * a[i]
for i in range(n):
    model += y_a[i] >= (DC - Dm[i]) - (1 - a[i]) * 1000  # Big M constraint
    model += y_a[i] <= (DC - Dm[i]) + (1 - a[i]) * 1000  # Big M constraint
    model += y_a[i] <= a[i] * 1000
    model += y_a[i] >= 0

# Add constraints for b and a based on Dm and DC
for i in range(n):
    model += b[i] == 1 if Dm[i] >= 1.05 * DC else 0
    model += a[i] == 1 if Dm[i] <= DC else 0

# Solve the model
model.solve()

# Print the results
print(f"Status: {pulp.LpStatus[model.status]}")
print(f"Optimal value of DC: {pulp.value(DC)}")
for i in range(n):
    print(f"b[{i}] = {pulp.value(b[i])}, a[{i}] = {pulp.value(a[i])}")


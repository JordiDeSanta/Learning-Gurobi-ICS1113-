from gurobipy import GRB, Model

model = Model()
model.setParam("TimeLimit", 60)

x = model.addVar(vtype=GRB.CONTINUOUS, name="x")
y = model.addVar(vtype=GRB.CONTINUOUS, name="y")
z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

model.update()

model.addConstr(3 * x + y + 2 * z <= 8, name="R1")
model.addConstr(x + 2 * y + z <= 10, name="R2")
model.addConstr(-x - y - 3 * z >= -14, name="R3")
model.addConstr(x >= 0, name="R4")
model.addConstr(y >= 0, name="R5")
model.addConstr(z >= 0, name="R6")

model.setObjective(2 * x + 4 * y + 5 * z, GRB.MAXIMIZE)
model.optimize()

valor_objetivo = model.Objval

print(f"La variable x toma el valor de {x.x}")
print(f"La variable x toma el valor de {y.x}")
print(f"La variable x toma el valor de {z.x}")

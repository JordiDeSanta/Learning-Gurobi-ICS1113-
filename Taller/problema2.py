from gurobipy import GRB, Model, quicksum

# Definicion de data: Definir de Distritos
Distritos = ["D1", "D2", "D3", "D4", "D5"]

# Definir valores para el parámetro t_ij y n_j (Tiempos de respuesta y promedios de incendio)
tiempo_respuesta = {
    "D1": {"D1": 5, "D2": 20, "D3": 15, "D4": 25, "D5": 10},
    "D2": {"D1": 12, "D2": 4, "D3": 20, "D4": 15, "D5": 25},
    "D3": {"D1": 30, "D2": 15, "D3": 6, "D4": 25, "D5": 15},
    "D4": {"D1": 20, "D2": 10, "D3": 15, "D4": 4, "D5": 12},
    "D5": {"D1": 15, "D2": 25, "D3": 12, "D4": 10, "D5": 5},
}

promedio_incendios = {
    "D1": 2,
    "D2": 1,
    "D3": 3,
    "D4": 1,
    "D5": 3
}


def t(i, j):
    return tiempo_respuesta[j][i]


def n(j):
    return promedio_incendios[j]


# Crea un modelo vacío
model = Model()

# Crea las variables de decisión x_i y z_ij
b = model.addVars(Distritos, vtype=GRB.BINARY, name="b_d")
a = model.addVars(Distritos, Distritos, vtype=GRB.BINARY, name="a_de")

# Llama a update para agregar las variables al modelo
model.update()

# Restricciones
# Crea la restriccion: Solo se se pueden instalar dos bombas
model.addConstr(quicksum(b[d] for d in Distritos) == 2, name="Solo dos bombas")

# Crea la restriccion: Cada distrito debe ser atendido por una bomba
model.addConstrs((quicksum(a[d, e] for d in Distritos if e != d) == 1 for e in Distritos), name="Atendido por una")

# Crea la restriccion: Si no se ha instalado ninguna bomba no es posible atender a ningun otro distrito desde ahí
model.addConstrs((b[d] >= a[d, e] for d in Distritos for e in Distritos if e != d), name="No atender")

# Escribe la funcion objetivo
objetivo = quicksum(a[d, e] * t(d, e) * n(d) for e in Distritos for d in Distritos)
model.setObjective(objetivo, GRB.MINIMIZE)

# Optimiza tu problema
model.optimize()

# Muestra los valores de las soluciones
print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
print(f"El valor objetivo es de: {model.ObjVal}")
for distrito1 in Distritos:
    if b[distrito1].x != 0:
        print(f"Se instala una bomba en el distrito {distrito1}")
    for distrito2 in Distritos:
        if a[distrito1, distrito2].x != 0:
            print(f"El distrito {distrito2} es atendido por la bomba del {distrito1}")

# ¿Cuál de las restricciones son activas?
print("\n"+"-"*9+" Restricciones Activas "+"-"*9)
for constr in model.getConstrs():
    if constr.getAttr("slack") == 0:
        print(f"La restricción {constr} está activa")

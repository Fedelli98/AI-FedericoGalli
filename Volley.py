import random
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
import matplotlib.pyplot as plt

#region

# # Funzione per generare dati randomizzati
# def generate_random_data(n, m, c):
#     squad_pp = np.zeros(n, dtype=int)
#     pal_pc = np.zeros((m, c), dtype=int)
    
#     random_squad_positions = random.sample(range(m * n), n)
#     for i, pos in enumerate(random_squad_positions):
#         squad_pp[i] = pos % m + 1
    
#     random_pal_positions = random.sample(range(m * c), m)
#     for i, pos in enumerate(random_pal_positions):
#         pal_pc[pos // c, pos % c] = i + 1
    
#     return squad_pp, pal_pc

# # Inserisci il numero di squadre, palazzetti e città
# n = int(input("Inserisci il numero di squadre (10-14): "))
# m = int(input("Inserisci il numero di palazzetti (7-9): "))
# c = int(input("Inserisci il numero di città (2-4): "))

# # Genera i dati randomizzati
# squad_pp, pal_pc = generate_random_data(n, m, c)

# # Calcola il numero di giornate
# giornate = (n-1)*2 if (n // 2) == (n / 2) else n*2

# # Crea il modello CPMpy
# model = Model()

# # Variabili
# calendario = boolvar(shape=(n, n, c, giornate))
# par_pc = intvar(0, m, shape=(c, giornate))

# # Vincoli
# # Una squadra non può giocare contro se stessa
# for i in range(n):
#     for k in range(c):
#         for g in range(giornate):
#             model += (calendario[i,i,k,g] == 0)

# # Massimo una partita per palazzetto a giornata
# for g in range(giornate):
#     for k in range(c):
#         for j in range(n):
#             model += (sum(calendario[:, j, k, g]) <= 1)
#         for i in range(n):
#             model += (sum(calendario[i, :, k, g]) <= 1)

# # Una giornata deve avere un numero di partite uguale alla parte intera inferiore di n/2
# for g in range(giornate):
#     model += (sum(calendario[:, :, :, g]) == n // 2)

# # # Una squadra può giocare al massimo una partita per giornata
# # for i in range(n):
# #     for g in range(giornate):
# #         model += (sum(calendario[i, :, :, g]) <= 1)
# #         model += (sum(calendario[:, i, :, g]) <= 1)

# # Massimo partite in campionato n*(n-1)
# model += (sum(calendario) == n * (n - 1))

# # Squadre giocano nelle città corrette
# for p in range(n):
#     for q in range(c):
#         if pal_pc[p % m, q] != 0:
#             for g in range(giornate):
#                 for k in range(c):
#                     if k != q:
#                         model += (sum(calendario[pal_pc[p % m, q]-1, :, k, g]) == 0)

# # Conta partite per città
# for g in range(giornate):
#     for t in range(c):
#         model += (par_pc[t,g] == sum(calendario[:,:,t,g]))

# # Ogni squadra gioca una partita per giornata
# for i in range(n):
#     for j in range(n):
#         for k in range(c):
#             for g in range(giornate):
#                 model += (calendario[i, j, k, g].implies(
#                     (sum(calendario[j, :, cit, g] for cit in range(c) if cit != k) == 0) &
#                     (sum(calendario[:, j, cit, g] for cit in range(c) if cit != k) == 0) &
#                     (sum(calendario[i, :, cit, g] for cit in range(c) if cit != k) == 0) &
#                     (sum(calendario[:, i, cit, g] for cit in range(c) if cit != k) == 0) &
#                     (sum(calendario[j, row, k, g] for row in range(n)) == 0) &
#                     (sum(calendario[col, i, k, g] for col in range(n)) == 0) &
#                     (sum(calendario[i, j, k, gio] for gio in range(giornate)) == 1)
#                 ))

# # Variabile obiettivo: minimizzare il numero di partite in una specifica città in una giornata
# func = par_pc[1,2]

# # Aggiungi l'obiettivo al modello
# model.minimize(func)

# # Risolvi il modello
# solver = CPM_ortools(model)
# if solver.solve():
#     print(pal_pc)
#     print("Calendario delle partite:")
#     calendario_value = calendario.value()
#     for g in range(giornate):
#         print(f"Giornata {g+1}:")
#         for i in range(n):
#             for k in range(c):
#                 for j in range(n):
#                     print(f"{1 if calendario_value[i, j, k, g] else 0}", end=" ")
#                 print("   ", end="")  # Separate matrices by spaces
#             print()
#         print()
#     print("Partite per città per giornata:")
#     print(par_pc.value())
#     print("Numero di partite in una specifica città in una giornata:" + str(func.value()))
# else:
#     print(pal_pc)
#     print("Nessuna soluzione trovata")

#endregion

# Funzione per generare dati randomizzati
def generate_random_data(n, m, c):
    squad_pp = np.zeros(n, dtype=int)
    pal_pc = np.zeros((m, c), dtype=int)
    
    random_squad_positions = random.sample(range(m * n), n)
    for i, pos in enumerate(random_squad_positions):
        squad_pp[i] = pos % m + 1
    
    random_pal_positions = random.sample(range(m * c), m)
    for i, pos in enumerate(random_pal_positions):
        pal_pc[pos // c, pos % c] = i + 1
    
    return squad_pp, pal_pc

# Crea il modello e risolve il problema
def solve_model(n, m, c):
    # Genera i dati randomizzati
    squad_pp, pal_pc = generate_random_data(n, m, c)
    
    # Calcola il numero di giornate
    giornate = (n-1)*2 if (n // 2) == (n / 2) else n*2

    # Crea il modello CPMpy
    model = Model()

    # Variabili
    calendario = boolvar(shape=(n, n, c, giornate))
    par_pc = intvar(0, m, shape=(c, giornate))

    # Vincoli
    # Una squadra non può giocare contro se stessa
    for i in range(n):
        for k in range(c):
            for g in range(giornate):
                model += (calendario[i,i,k,g] == 0)

    # Massimo una partita per palazzetto a giornata
    for g in range(giornate):
        for k in range(c):
            for j in range(n):
                model += (sum(calendario[:, j, k, g]) <= 1)
            for i in range(n):
                model += (sum(calendario[i, :, k, g]) <= 1)

    # Una giornata deve avere un numero di partite uguale alla parte intera inferiore di n/2
    for g in range(giornate):
        model += (sum(calendario[:, :, :, g]) == n // 2)

    # Massimo partite in campionato n*(n-1)
    model += (sum(calendario) == n * (n - 1))

    # Squadre giocano nelle città corrette
    for p in range(n):
        for q in range(c):
            if pal_pc[p % m, q] != 0:
                for g in range(giornate):
                    for k in range(c):
                        if k != q:
                            model += (sum(calendario[pal_pc[p % m, q]-1, :, k, g]) == 0)

    # Conta partite per città
    for g in range(giornate):
        for t in range(c):
            model += (par_pc[t,g] == sum(calendario[:,:,t,g]))

    # Ogni squadra gioca una partita per giornata
    for i in range(n):
        for j in range(n):
            for k in range(c):
                for g in range(giornate):
                    model += (calendario[i, j, k, g].implies(
                        (sum(calendario[j, :, cit, g] for cit in range(c) if cit != k) == 0) &
                        (sum(calendario[:, j, cit, g] for cit in range(c) if cit != k) == 0) &
                        (sum(calendario[i, :, cit, g] for cit in range(c) if cit != k) == 0) &
                        (sum(calendario[:, i, cit, g] for cit in range(c) if cit != k) == 0) &
                        (sum(calendario[j, row, k, g] for row in range(n)) == 0) &
                        (sum(calendario[col, i, k, g] for col in range(n)) == 0) &
                        (sum(calendario[i, j, k, gio] for gio in range(giornate)) == 1)
                    ))

    # Variabile obiettivo: minimizzare il numero di partite in una specifica città in una giornata
    func = par_pc[1,2]

    # Aggiungi l'obiettivo al modello
    model.minimize(func)

    # Risolvi il modello
    solver = CPM_ortools(model)
    if solver.solve():
        return True, func.value()
    else:
        return False, None, None

# Numero di volte da eseguire lo script per ogni combinazione
num_runs = 10

# Dati per i grafici
x_values = list(range(10, 15))  # Numero di squadre
y_values = [2, 3, 4]            # Numero di città


for n in x_values:
    plt.figure()  # Crea una nuova figura per ogni numero di squadre
    for c in y_values:
        success_count = 0
        total_func = 0
        max_func = float('-inf')
        min_func = float('inf')
        for _ in range(num_runs):
            success, func = solve_model(n, n, c)
            if success:
                success_count += 1
                total_func += func
                maximum = (max_func, func)
                minimum = (min_func, func)
                max_func = max(maximum)
                min_func = min(minimum)
        if success_count > 0:
            average_func = total_func / success_count
            plt.plot(c, average_func, marker='o', label=f'{c} città (media)')
            plt.plot(c, max_func, marker='^', linestyle='--', label=f'{c} città (massimo)')
            plt.plot(c, min_func, marker='v', linestyle='--', label=f'{c} città (minimo)')
            plt.xlabel('Numero di città')
            plt.ylabel('Media delle partite per città per giornata (funzione obiettivo)')
            plt.title(f'Media, massimo e minimo delle partite per città per giornata con {n} squadre')
            plt.legend()
            plt.grid(True)
# # Grafici
# for c in y_values:
#     for n in x_values:
#         success_count = 0
#         total_par_pc = 0
#         total_func = 0
#         max_func = float('-inf')
#         min_func = float('inf')
#         for _ in range(num_runs):
#             success, func = solve_model(n, n, c)
#             if success:
#                 success_count += 1
#                 total_func += func
#                 maximum = (max_func, func)
#                 minimum = (min_func, func)
#                 max_func = max(maximum)
#                 min_func = min(minimum)
#         if success_count > 0:
#             average_func = total_func / success_count
#             plt.plot(n, average_func, marker='o', label=f'{c} città (media)')
#             plt.plot(n, max_func, marker='x', linestyle='--', color='r', label=f'{c} città (massimo)')
#             plt.plot(n, min_func, marker='x', linestyle='--', color='g', label=f'{c} città (minimo)')

# # Impostazioni del grafico
# plt.xlabel('Numero di squadre')
# plt.ylabel('Media delle partite per città per giornata (funzione obiettivo)')
# plt.title('Media delle partite per città per giornata in base al numero di squadre (funzione obiettivo)')
# plt.legend()
# plt.grid(True)

# Mostra il grafico
plt.show()
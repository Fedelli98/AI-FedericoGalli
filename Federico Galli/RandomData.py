import os
import random

def zero_checker(matrix):
    numchecker = [0 for _ in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            if matrix[j][i] != 0:
                numchecker[i] += 1
    for i in range(len(matrix[0])):
        if numchecker[i]==0:
            j = 0
            while numchecker[j] <= 1:
                j+=1
            k = 0
            while matrix[k][j] == 0:
                k+=1
            matrix[1][i] = matrix[k][j]
            matrix[k][j] = 0
            numchecker[j] -= 1
            numchecker[i] += 1
    # for row in matrix:
    #     print(" ".join(map(str, row)))
    

def generate_matrix(n, m, c):
    # Primo Array n di palazzetti
    # first_matrix = [[0] * m for _ in range(n)]
    # for k in range(n+1):
    #     num = k
    #     row = random.randint(0, n - 1)
    #     col = random.randint(0, m - 1)
    #     while first_matrix[row][col] != 0:
    #         row = random.randint(0, n - 1)
    #         col = random.randint(0, m - 1)
    #     first_matrix[row][col] = num
    # zero_checker(first_matrix)
    array = [i for i in range(1, n+1)]
    random.shuffle(array)
    #print(array)


    # Seconda matrice c x m
    second_matrix = [[0] * c for _ in range(m)]
    for k in range(m+1):
        num = k
        row = random.randint(0, m - 1)
        col = random.randint(0, c - 1)
        while second_matrix[row][col] != 0:
            row = random.randint(0, m - 1)
            col = random.randint(0, c - 1)
        second_matrix[row][col] = num
    zero_checker(second_matrix)

    return array, second_matrix

def write_matrices_to_dzn_file(first_matrix, second_matrix, file_path):
    with open(file_path, 'w') as file:
        file.write("n = " + str(len(first_matrix)) + ";\n")
        file.write("m = " + str(len(first_matrix)) + ";\n")
        file.write("c = " + str(len(second_matrix[0])) + ";\n\n")
        # Scrive la prima matrice
        file.write("squad_pp = [")
        file.write(", ".join(map(str, first_matrix)))
        file.write("];\n\n")

        # Scrive la seconda matrice
        file.write("pal_pc = [|")
        for row in second_matrix:
            file.write("".join(f"{num}," for num in row)[:-1] + "|\n")
        file.write("|];\n")
    file.close()



def main(n = None, m = None, c = None):
    if n is None and m is None and c is None:
        # Chiede all'utente di inserire n, m e c
        n = int(input("Inserisci il numero di squadre (da 10 a 14): "))
        m = n
        c = int(input("Inserisci il numero di città (da 2 a 4): "))
    else:
         if n < 10 or n > 14 or m < 10 or m > 14 or c < 2 or c > 4:
             raise ValueError("I valori di n e c devono essere compresi tra i seguenti valori: n da 10 a 14, c da 2 a 4.")
         else:
            n=n
            m=n
            c=c

    #Percorso al file di dati per Minizinc da creare o modificare
    projrootdir = os.path.dirname(os.path.abspath(__file__))
    filename= "RandomData.dzn"
    file_path = os.path.join(projrootdir, filename)
    
    # Genera le matrici
    first_matrix, second_matrix = generate_matrix(n, m, c)

    # Scrive le matrici nel file .dzn
    write_matrices_to_dzn_file(first_matrix, second_matrix, file_path)
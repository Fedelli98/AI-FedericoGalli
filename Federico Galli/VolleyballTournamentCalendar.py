import os
from minizinc import Instance, Model, Solver
from RandomData import main
calendar = Model("./Playground.mzn")
OrToolsSat = Solver.lookup("com.google.ortools.sat")
print("Solver: ", OrToolsSat.name, ",", OrToolsSat.version)
OrToolsSat.stdFlags+=["--parallel 2"]
OrToolsSat.stdFlags.remove('-p')
instance = Instance(OrToolsSat, calendar)
projrootdir = os.path.dirname(os.path.abspath(__file__))
filename= "Result.txt"
run = input("Choose 1 for single run or 2 for automated multiple runs\n")
if run == "2":
    file_path = os.path.join(projrootdir, filename)
    with open(file_path, 'w') as file:
        file.write("Scelta Città: 2 e Giornata: 3 da minimizzare\n")
    for n in range(10,15):
        for c in range(2,5):
            for _ in range(5):
                main(n,n,c)
                result = instance.solve()
                with open(file_path, 'a') as file:
                    file.write(str(result))
    file.close() 
elif run == "1":
    main()
    result = instance.solve()
    print(result)

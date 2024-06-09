% Use this editor as a MiniZinc scratch book
include "alldifferent.mzn";
include "RandomData.dzn";

                                                            % VARIABILI
int: n;  set of int: SQUADRE = 1..n;      % Numero di squadre
int: m;  set of int: PALAZZETTI = 1..m;   % Numero di palazzetti
int: c;  set of int: CITTA = 1..c;        % Numero di città
int: giornate = if (n div 2) == n/2 then (n-1)*2 else n*2 endif; %calcolo delle giornate in base al numero di squadre
set of int: GIORNATE= 1..giornate;              % Numero di Giornate
array[SQUADRE] of int: squad_pp;          % Squadre per palazzetto
array[PALAZZETTI, CITTA] of int: pal_pc;        % Plazzetti per Città
array[CITTA, GIORNATE] of var 0..m: par_pc;          % Partite per città per giornata
array[SQUADRE, SQUADRE, CITTA, GIORNATE] of var 0..1: calendario;


                                                              %VINCOLI

                %diagonle di 0 su ogni matrice bidimensionale SQUADRE x SQUADRE per non far giocare una squadra contro se stessa
constraint forall(i in SQUADRE, j in SQUADRE, k in CITTA, g in GIORNATE where i=j)(calendario[i,j,k,g]=0);

                %massimo una partita per palazzetto a giornata
constraint forall(g in GIORNATE, k in CITTA, j in SQUADRE)(sum(i in SQUADRE)(calendario[i,j,k,g])<=1);
constraint forall(g in GIORNATE, k in CITTA, i in SQUADRE)(sum(j in SQUADRE)(calendario[i,j,k,g])<=1);


                %una giornata deve avere un numero di partite uguale alla parte intera inferiore di n/2,
                % per considerare anche i casi in cui ci siano numero di squadre dispari
constraint forall(g in GIORNATE)(sum(k in CITTA, i in SQUADRE, j in SQUADRE)(calendario[i,j,k,g])=n div 2);

                %due squadre possono giocare al massimo una partita per giornata, controllo su tutte le città è ridondante ma altrimenti dovrei controllare anche la matrice pal_pc
constraint forall(i in SQUADRE, j in SQUADRE, k in CITTA, g in GIORNATE)(if calendario[i,j,k,g]=1 then 
(forall(cit in CITTA where cit!=k)(sum(col in SQUADRE)(calendario[j,col,cit,g])=0)) /\
(forall(cit in CITTA where cit!=k)(sum(row in SQUADRE)(calendario[row,j,cit,g])=0)) /\
(forall(cit in CITTA where cit!=k)(sum(col in SQUADRE)(calendario[i,col,cit,g])=0)) /\
(forall(cit in CITTA where cit!=k)(sum(row in SQUADRE)(calendario[row,i,cit,g])=0)) /\
sum(row in SQUADRE)(calendario[j,row,k,g])=0 /\ sum(col in SQUADRE)(calendario[col,i,k,g])=0 /\
sum(gio in GIORNATE)(calendario[i,j,k,gio])=1 else true endif);

                % massimo partite in campionato n(n-1)
constraint count(i in SQUADRE, j in SQUADRE, k in CITTA, g in GIORNATE)(calendario[i,j,k,g]=1)=n*(n-1);

                %controllo su squadre che giocano nella giusta città
constraint forall(p in SQUADRE, q in CITTA where pal_pc[p,q]!=0)(forall(g in GIORNATE, k in CITTA where k!=q)(sum(j in SQUADRE)(calendario[pal_pc[p,q],j,k,g])=0));


                % Conta partite per città
constraint forall(g in GIORNATE) (
              forall(t in CITTA)(par_pc[t,g]=sum(i in SQUADRE, j in SQUADRE)(calendario[i,j,t,g])));

var int: func = par_pc[2,3];

                                                             %SOLVER
solve minimize(func);


/*output[
if i = 1 /\ j = 1 /\ k =1  then "Giornata " ++ show(g) ++ "\n" else "" endif ++
/*show(i) ++ show(j)++ show(k)++ show(g) ++ "[" ++show(calendario[i,j,k,g]) ++ "]" ++
if j = n then "| " else "" endif ++ 
if j = n /\ k = c then "\n" else " " endif ++ 
if i = n /\ j=n /\ k=m then "\n" else "" endif
  | g in GIORNATE, i in SQUADRE, k in CITTA, j in SQUADRE
];
*/

%output["\n" ++ show(tag_partite)++"\n"];



/*output[
show(tmpcounter[i,k,g])++" "++
%show(i)++show(k)++show(g)++" "++
if i = n*n then "| " else "" endif++
if k = m /\ i = n*n then "\n\n" else "" endif
| g in GIORNATE, k in PALAZZETTI, i in 1..n*n];*/


%output[show(tag_partite)++"\n"];
/*output["Squadre per Palazzetto:"];
output[if i =1 then "\n" else " " endif ++
        show(squad_pp[i])
        |i in SQUADRE];*/

output["\n\nPalazzetti per Città:\n"];
output[ show(pal_pc[i,j])++ 
        if i = n  then "\n" else " " endif
        |j in CITTA, i in PALAZZETTI];
        
output["\n\nPartite per giornata per città:\n"];
output[if j =1 then "\n" else " " endif ++
        show(par_pc[i,j])
        |i in CITTA, j in GIORNATE];
output["\nPartite:"++show(func)]

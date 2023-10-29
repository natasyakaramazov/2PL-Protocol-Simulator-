Kierra Ashford 1002018597
Tsebaot Meron  1001629719

README                                               
*************
File(s) included:Team19_Project1.py
****************
Database 2: Summer 2023 
Project1 : Two-phase Locking (2PL) protocol 
***

compilation instructions :
->this is built in Visual Studio Code 
->In terminal:
            Python project_1.py Input1.txt (no space between the 1)
-> To send to output file 
            Python project_1.py Input1.txt > output.txt

Sample run: For Input1.txt
b1;
r1(Y);
w1(Y);
r1(Z);
b2;
r2(Y);
b3;
r3(Z);
w1(Z);
e1;
w3(Z);
e3;

Output:
b1;

b1; T1  begins.TS=1  state=Active
r1(Y);

Y is read locked by T1
w1(Y);

T1 has been upgraded from read locked to write locked on data item Y
r1(Z);

Z is read locked by T1
b2;

b2; T2  begins.TS=2  state=Active
r2(Y);

Transaction 2 is aborted due to wait-die
b3;

b3; T3  begins.TS=3  state=Active
r3(Z);

Z is read locked by T3
w1(Z);

Transaction 1 is blocked/waiting due to wait-die
e1;

T1is going to be committed soon
w3(Z);

Transaction 3 is aborted due to wait-die
Transaction 1 is released from the waiting queue
 w1(Z);

T1 has been upgraded from read locked to write locked on data item Z
e1;

Transaction 1 is committed
 e1;

Transaction 1 is committed
e3;

Transaction 3 has already been aborted
T1 is commmited
T2 is aborted
T3 is aborted
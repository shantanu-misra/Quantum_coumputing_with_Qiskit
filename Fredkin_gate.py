from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

def fredkin():
    circuit = QuantumCircuit(3)
    circuit.cx(0,1)
    circuit.ccx(2,1,0)
    circuit.cx(0,1)
    return circuit

circuit = fredkin()

job = execute(circuit,Aer.get_backend('unitary_simulator'),shots=1)
u=job.result().get_unitary(circuit,decimals=3)
for i in range(len(u)):
    s=""
    for j in range(len(u)):
        val = str(u[i][j].real)
        while(len(val)<5): val  = " "+val
        s = s + val
    print(s)

circuit.draw(output="mpl")

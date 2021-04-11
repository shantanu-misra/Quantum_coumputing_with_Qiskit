from qiskit import QuantumCircuit, Aer, execute

# Define quantum circuit
qc = QuantumCircuit(3,1)

for input in ['00', '01', '10', '11']:

    # Initialise all qubits to ket 0 to make life easy
    if input[0] == '1':
        qc.x(0)
    if input[1] == '1':
        qc.x(1)

    qc.ccx(0,1,2)

    qc.measure(1,0)

    job = execute(qc,Aer.get_backend('qasm_simulator'),shots=1000)
    counts = job.result().get_counts(qc)
    print("Input:", input, "Output:", counts)

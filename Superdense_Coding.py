from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

def create_bell_pair(qc):
    qc.h(0)
    qc.cx(0,1)

def specify_state(qc, msg):
    if msg == "00":
        pass
    elif msg == "01":
        qc.z(0)
    elif msg == "10":
        qc.x(0)
    elif msg == "11":
        qc.x(0)
        qc.z(0)
    else:
        print("Invalid Message: Sending '00'")

def bell_measure(qc):
    qc.cx(0,1)
    qc.h(0)
    qc.measure([0,1],[0,1])

# Create the quantum circuit with 2 qubits
qc = QuantumCircuit(2,2)


# Step 1: Preparation
create_bell_pair(qc)

# Step 2: Travel
qc.barrier()

# Step 3: Encoding. Alice encodes her message onto qubit 0. In this case, we want to send the message '01'.
message = "11"
specify_state(qc, message)

# Step 4: Transmission
qc.barrier()

# Step 5: Decoding. After recieving qubit 0, Bob applies the decoding protocol.
bell_measure(qc)

# Draw our output
qc.draw(output = "mpl")

backend = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend, shots=1024)
sim_result = job_sim.result()


measurement_result = sim_result.get_counts(qc)
print(measurement_result)
plot_histogram(measurement_result)

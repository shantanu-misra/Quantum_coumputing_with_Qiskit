import qiskit as q
import numpy as np
import matplotlib.pyplot as plt

def create_bell_pair(qc, a, b):
    qc.h(a)
    qc.cx(a,b)

def alice_gates(qc, a, b):
    qc.cx(a,b)
    qc.h(a)

def measure_and_send(qc, a, b):
    qc.measure(a,0)
    qc.measure(b,1)

def bob_gates(qc, qubit, crz, crx):
    qc.x(qubit).c_if(crx, 1)
    qc.z(qubit).c_if(crz, 1)

def teleportation_circuit(psi):

    # First we make our state Psi into a initialisation gate
    init_gate = q.extensions.Initialize(psi)
    init_gate.label = "Secret Message!"

    # Create our circuit!
    qr = q.QuantumRegister(3, name="q")   # Create a 3 qubit quantum register
    c_0 = q.ClassicalRegister(1, name="c_0") # Create 2 single bit classical registers
    c_1 = q.ClassicalRegister(1, name="c_1")
    qc = q.QuantumCircuit(qr, c_0, c_1)

    # Initialise Alice's Qubit to have state Psi
    qc.append(init_gate, [0])
    # We use barrier to split up each segment
    qc.barrier()

    # Use snapshot magic to record the initial statevector
    qc.snapshot('1')
    # We use barrier to split up each segment
    qc.barrier()

    # Charlie creates the Bell pair
    create_bell_pair(qc, 1, 2)
    # We use barrier to split up each segment
    qc.barrier()

    # Alice does gate prep
    alice_gates(qc, 0, 1)
    # We use barrier to split up each segment
    qc.barrier()

    # Alice measures her state and sends to Bob
    measure_and_send(qc, 0, 1)
    # We use barrier to split up each segment
    qc.barrier()

    # Bob decodes the classical bits and re-creates Psi
    bob_gates(qc, 2, c_0, c_1)
    # We use barrier to split up each segment
    qc.barrier()

    # Use snapshot magic to record the final statevector
    qc.snapshot('2')

    # We want our function to return a fully prepared circuit
    return qc


psi = np.array([0.5533920757991503+0.3043529040180291j, 0.6147796854942953+0.4724113234904887j])
circ = teleportation_circuit(psi)

# Execute the circuit on the simulated backend
backend = q.Aer.get_backend('statevector_simulator')
result = q.execute(circ, backend).result()

# Put our snapshots into a list
snapshots = result.data()['snapshots']['statevector']

# Get Alice's state:
alice_state = snapshots['1']

# Get Bob's final state:
bob_state = snapshots['2']

def check_same_state(alice, bob, psi):
    a = alice[0]
    b = [c for c in bob[0] if c != 0]
    print("Psi state: ", psi[0], psi[1])
    print("Alice's state: ", a[0], a[1])
    print("Bob's state: ", b[0], b[1])
    # For simplicity I am rounding and summing to check for equality
    if np.round(a[0]+a[1], 5) == np.round(b[0]+ b[1], 5):
        print("State Successfully Teleported!")
    else:
        print("Error: Bob did not get the right state!")

check_same_state(alice_state, bob_state, psi)

circ.draw('mpl')

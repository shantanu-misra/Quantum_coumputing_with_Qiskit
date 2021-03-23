from random import getrandbits
import qiskit as q

key_length = 500
quantum_channel = []
classical_channel = []

def select_encoding(length):
    # This stores the states Alice will encode
    alice_bitstring = ""
    # This stores the bases that Alice will prepare the states in
    alice_bases = ""

    # For the length
    for i in range(length):
        # We use the function getrandbits to get either a 0 or 1 randomly,
        # The "1" in the function argument is the number of bits to be generated
        alice_bitstring += (str(getrandbits(1)))
        # 0 means encode in the (0,1) basis and 1 means encode in the (+,-) basis
        alice_bases += (str(getrandbits(1)))

    # return the string of bits and the list of bases they should be encoded in
    return alice_bitstring, alice_bases

def select_measurement(length):
    # Similar to before we store the bases that Bob will measure in a list
    bob_bases = ""

    for i in range(length):
        # Again we use getrandbits to generate a 0 or 1 randomly
        bob_bases += (str(getrandbits(1)))

    # return the list of random bases to measure in
    return bob_bases

def encode(alice_bitstring, alice_bases):
    encoded_qubits = []
    for i in range(len(alice_bitstring)):
        # create a brand new quantum circuit called qc. Remember that the qubit will be in state |0> by default
        qc = q.QuantumCircuit(1,1)

        if alice_bases[i] == "0":
            # 0 Means we are encoding in the z basis
            if alice_bitstring[i] == "0":
                # We want to encode a |0> state, as states are intialized
                # in |0> by default we don't need to add anything here
                pass

            elif alice_bitstring[i] == "1":
                # We want to encode a |1> state
                # We apply an X gate to generate |1>
                qc.x(0)

        elif alice_bases[i] == "1":
            # 1 Means we are encoding in the x basis
            if alice_bitstring[i] == "0":
                # We apply an H gate to generate |+>
                qc.h(0)
            elif alice_bitstring[i] == "1":
                # We apply an X and an H gate to generate |->
                qc.x(0)
                qc.h(0)

        # add this quantum circuit to the list of encoded_qubits
        encoded_qubits.append(qc)

    return encoded_qubits

def measure(bob_bases, encoded_qubits, backend):
    # Perform measurement on the qubits send by Alice
    # selected_measurements:
    # encoded_qubits: list of QuantumCircuits received from Alice
    # backend: IBMQ backend, either simulation or hardware

    # Stores the results of Bob's measurements
    bob_bitstring = ''

    for i in range(len(encoded_qubits)):
        qc = encoded_qubits[i]

        if bob_bases[i] == "0":
            # 0 means we want to measure in Z basis
            qc.measure(0,0)

        elif bob_bases[i] == "1":
            # 1 means we want to measure in X basis
            qc.h(0)
            qc.measure(0,0)

        # Now that the measurements have been added to the circuit, let's run them.
        job = q.execute(qc, backend=backend, shots = 1) # increase shots if running on hardware
        results = job.result()
        counts = results.get_counts()
        measured_bit = max(counts, key=counts.get)

        # Append measured bit to Bob's measured bitstring
        bob_bitstring += measured_bit

    return bob_bitstring

def bob_compare_bases(alices_bases, bobs_bases):
    indices = []

    for i in range(len(alices_bases)):
        if alices_bases[i] == bobs_bases[i]:
            indices.append(i)
    return indices

def construct_key_from_indices(bitstring, indices):
    key = ''
    for idx in indices:
        # For the indices where bases match, the bitstring bit is added to the key
        key = key + bitstring[idx]
    return key

alice_bitstring, alice_bases = select_encoding(key_length)
bob_bases = select_measurement(key_length)

# Alice can now create the encoded qubits using the bit_key and selected_bases from 1
encoded_qubits = encode(alice_bitstring, alice_bases)

# Alice Sends Bob her encoded qubits over the quantum_channel
quantum_channel = encoded_qubits

sim_backend = q.Aer.get_backend('qasm_simulator')
bob_bitstring = measure(bob_bases, quantum_channel, sim_backend)

# Alice sends the list of bases used to create her encoded qubits to bob over the classical channel
classical_channel = alice_bases

agreeing_bases = bob_compare_bases(classical_channel, bob_bases)

# Send the list of agreeing_bases from Bob to Alice over the Classical channel
classical_channel = agreeing_bases

alice_key = construct_key_from_indices(alice_bitstring, classical_channel)
bob_key = construct_key_from_indices(bob_bitstring, agreeing_bases)

# Preview the first 10 elements of each Key:
print("alice_key: ", alice_key[:10])
print("bob_key: ", bob_key[:10])
print("Alice's key is equal to Bob's key: ", alice_key == bob_key)

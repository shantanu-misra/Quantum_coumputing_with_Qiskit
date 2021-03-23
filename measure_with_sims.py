from qiskit import __qiskit_version__, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector, plot_bloch_multivector

"""
1. qasm_simulator: Allows ideal and noisy multi-shot execution of qiskit circuits
   and returns counts or memory

2. statevector_simulator: Allows ideal single-shot execution of qiskit circuits
   and returns the final statevector of the simulator after application

3. unitary_simulator: Allows ideal single-shot execution of qiskit circuits and
   returns the final unitary matrix of the circuit itself.
"""

def measure_with_sim(quantum_circuit, simulator):
    backend = Aer.get_backend(simulator) # Tell Qiskit how to simulate our circuit

    # Create a Quantum Program for execution. This statement runs the circuit. We have to ive execute two inputs
    # the circuit we want to run (circ_bell), and the simulator we want to use (backend = statevector simulator).
    job = execute(quantum_circuit, backend)

    # Grab the results from the job.
    result = job.result()

    state_vector = result.get_statevector(quantum_circuit)
    #return state_vector  # return the output state vector

    counts = result.get_counts(quantum_circuit)
    #return counts

    dictionary_of_counts_and_state_vector = {'Counts': counts, 'State Vector': state_vector}
    return dictionary_of_counts_and_state_vector
    #plot_histogram(counts)

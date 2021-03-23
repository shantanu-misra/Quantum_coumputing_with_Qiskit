from qiskit import __qiskit_version__, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector, plot_bloch_multivector

def create_bell_pair(desired_circuit):

    if desired_circuit.lower() == 'phi_plus':
        # Phi Plus
        phi_plus = QuantumCircuit(2)
        phi_plus.h(0)
        phi_plus.cx(0,1)
        return phi_plus

    elif desired_circuit.lower() == 'phi_minus':
        # Phi Minus
        phi_minus = QuantumCircuit(2)
        phi_minus.x(0)
        phi_minus.h(0)
        phi_minus.cx(0,1)
        return phi_minus

    elif desired_circuit.lower() == 'psi_plus':
        # Psi Plus
        psi_plus = QuantumCircuit(2)
        psi_plus.h(0)
        psi_plus.x(1)
        psi_plus.cx(0,1)
        return psi_plus

    elif desired_circuit.lower() == 'psi_minus':
        # Psi Minus
        desired_circuit = QuantumCircuit(2)
        psi_plus.h(0)
        psi_plus.x(1)
        psi_plus.cx(0,1)
        return psi_minus

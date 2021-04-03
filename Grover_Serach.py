import matplotlib.pyplot as plt
import numpy as np
import qiskit as q
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram

def initialise(qc):
    qc.h(0)
    qc.h(1)
    qc.barrier()

def oracle_00(qc):
    qc.x(0)
    qc.z(0)
    qc.cz(0,1)
    qc.x(0)
    qc.barrier()

def oracle_01(qc):
    qc.x(0)
    qc.z(0)
    qc.cz(0,1)
    qc.barrier()

def oracle_10(qc):
    qc.cz(0, 1)
    qc.x(0)
    qc.barrier()

def oracle_11(qc):
    qc.cz(0, 1)
    qc.barrier()

def u_g(qc):
    qc.h(0)
    qc.h(1)
    qc.z(0)
    qc.z(1)
    qc.cz(0,1)
    qc.h(0)
    qc.h(1)
    qc.barrier()

grover_circuit = q.QuantumCircuit(2)
initialise(grover_circuit)
oracle_00(grover_circuit)
u_g(grover_circuit)
grover_circuit.measure_all()
grover_circuit.draw('mpl')

# Simulating the Circuit
backend = q.Aer.get_backend('qasm_simulator')
job = q.execute(grover_circuit, backend, shots = 1024)
result = job.result()
counts = result.get_counts()
plot_histogram(counts)

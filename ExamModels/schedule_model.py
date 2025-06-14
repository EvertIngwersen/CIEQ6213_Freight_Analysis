# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 14:47:05 2025

@author: evert
"""

import pyomo.environ as pyo

# Define the data based on the provided tables for Case III 
jobs_data = {
    'j1': {'duration': 3},
    'j2': {'duration': 2}
}
machines = ['m1', 'm2']

# Create a Pyomo model
model = pyo.ConcreteModel()

# --- Sets ---
model.J = pyo.Set(initialize=jobs_data.keys(), doc='Set of jobs')
model.I = pyo.Set(initialize=machines, doc='Set of machines')

# --- Parameters ---
model.p = pyo.Param(model.J, initialize={j: data['duration'] for j, data in jobs_data.items()}, doc='Duration of job j')

# --- Variables ---
# x_ij = 1 if job j is assigned to machine i, 0 otherwise 
model.x = pyo.Var(model.I, model.J, within=pyo.Binary, doc='Assignment of job j to machine i')

# w: Makespan (maximum completion time) 
model.w = pyo.Var(within=pyo.NonNegativeReals, doc='Makespan')

# --- Objective Function ---
# Minimize the makespan 
model.objective = pyo.Objective(expr=model.w, sense=pyo.minimize)

# --- Constraints ---
# Constraint 1: Makespan must be greater than or equal to the completion time on each machine 
# On machine i, the last job is completed at sum(p_j * x_ij) 
def makespan_constraint_rule(model, i):
    return model.w >= sum(model.p[j] * model.x[i, j] for j in model.J)
model.makespan_constraint = pyo.Constraint(model.I, rule=makespan_constraint_rule, doc='Makespan constraint')

# Constraint 2: Each job must be assigned to exactly one machine 
def job_assignment_rule(model, j):
    return sum(model.x[i, j] for i in model.I) == 1
model.job_assignment = pyo.Constraint(model.J, rule=job_assignment_rule, doc='Job assignment constraint')

# --- Solve the model ---
# Use the Gurobi solver
solver = pyo.SolverFactory('gurobi')
results = solver.solve(model, tee=True) # tee=True shows solver output

# --- Display results ---
print("\n--- Optimization Results ---")
if (results.solver.status == pyo.SolverStatus.ok) and (results.solver.termination_condition == pyo.TerminationCondition.optimal):
    print(f"Optimal Makespan (w): {pyo.value(model.w)}")
    print("\nJob Assignments:")
    for i in model.I:
        assigned_jobs = [j for j in model.J if pyo.value(model.x[i, j]) > 0.5]
        total_duration_on_machine = sum(jobs_data[j]['duration'] for j in assigned_jobs)
        print(f"Machine {i}: {assigned_jobs} (Total duration: {total_duration_on_machine})")
else:
    print("Solver did not find an optimal solution.")
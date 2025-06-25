import streamlit as st
from treat_sim.model import Scenario, multiple_replications
import pandas as pd

st.title("Treatment Centre Simulation")

# Configuración del escenario
triage_bays = 1
exam_rooms = 3
treat_rooms = 1
exam_mean = 16.0
replications = 10

args = Scenario()
args.n_triage = triage_bays
args.n_exam = exam_rooms
args.n_cubicles_1 = treat_rooms
args.exam_mean = exam_mean

# Ejecutar simulación
results = multiple_replications(args, n_reps=replications)

# Mostrar resultados como tabla
df_results = results.mean().round(1).reset_index()
df_results.columns = ['Metric', 'Value']

st.table(df_results)

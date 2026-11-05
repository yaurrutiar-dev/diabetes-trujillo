"""Aplicación web (Streamlit) - Riesgo de diabetes. Apoyo a la decisión, no sustituye al profesional de salud."""
import joblib, numpy as np, pandas as pd, streamlit as st

st.set_page_config(page_title="Riesgo de diabetes", page_icon="🩺")
modelo = joblib.load("modelo_diabetes.joblib")
st.title("🩺 Estimación de riesgo de diabetes")
st.caption("Herramienta de tamizaje. No reemplaza el diagnóstico médico. No ingrese datos que identifiquen al paciente.")

c1, c2 = st.columns(2)
emb = c1.number_input("Embarazos", 0, 20, 0)
glu = c1.number_input("Glucosa (mg/dL, 0 = no disponible)", 0, 300, 100)
pa = c1.number_input("Presión diastólica (mm Hg, 0 = no disponible)", 0, 200, 70)
pli = c1.number_input("Pliegue del tríceps (mm, 0 = no disponible)", 0, 100, 0)
ins = c2.number_input("Insulina (µU/mL, 0 = no disponible)", 0, 900, 0)
imc = c2.number_input("IMC (kg/m², 0 = no disponible)", 0.0, 70.0, 25.0)
ped = c2.number_input("Pedigrí de diabetes", 0.0, 2.5, 0.4)
edad = c2.number_input("Edad (años)", 18, 100, 35)

if st.button("Calcular riesgo"):
    fila = pd.DataFrame([[emb, glu, pa, pli, ins, imc, ped, edad]],
        columns=["Embarazos","Glucosa","PresionArterial","PliegueCutaneo","Insulina","IMC","Pedigri","Edad"])
    fila[["Glucosa","PresionArterial","PliegueCutaneo","Insulina","IMC"]] = \
        fila[["Glucosa","PresionArterial","PliegueCutaneo","Insulina","IMC"]].replace(0, np.nan)
    p = float(modelo.predict_proba(fila)[0, 1])
    st.metric("Probabilidad estimada de diabetes", f"{p:.0%}")
    if p >= 0.5:
        st.error("Riesgo ALTO: se recomienda derivar a prueba de glucosa/HbA1c y evaluación clínica.")
    else:
        st.success("Riesgo BAJO según el modelo: mantener controles preventivos.")

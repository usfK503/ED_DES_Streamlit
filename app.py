import streamlit as st
from model import run_simulation
from decision import estimate_cost

st.title("ED Boarding DES – Decision Support Tool")

st.sidebar.header("Unit Design Parameters")
med_surg = st.sidebar.slider("Med-Surg Beds", 50, 200, 160)
stepdown = st.sidebar.slider("Stepdown Beds", 4, 20, 6)
triage = st.sidebar.slider("Triage Mean (min)", 3, 10, 5)

if st.button("Run Simulation"):
    avg_wait, sl = run_simulation(
        med_surg_beds=med_surg,
        stepdown_beds=stepdown,
        triage_mean=triage
    )

    cost = estimate_cost(med_surg, stepdown)

    st.subheader("Simulation Results")
    st.metric("Average Bed Wait (min)", round(avg_wait, 2))
    st.metric("Service Level (%)", round(sl, 2))
    st.metric("Estimated Cost", round(cost, 2))

    if sl >= 95:
        st.success("Design meets service-level target ✅")
    else:
        st.error("Design does NOT meet service-level target ❌")


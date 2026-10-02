import streamlit as st
from Methods import REGv3

# title
st.title("Random Encounter Generator")

#subtitle
st.subheader("Zoids TTRPG")

encounter_level = st.number_input(
    label = "Enter Encounter Level",
    min_value = 1,
    max_value = 50,
    value = 1,
    step = 1
)

if st.button("Generate Encounter"):
    st.write(REGv3.generate_encounter(encounter_level))

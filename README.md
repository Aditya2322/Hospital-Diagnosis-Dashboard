# Hospital-Discharges-Analysis
This project focuses on analyzing hospital discharge data to extract meaningful insights related to patient flow, discharge patterns, and resource utilization within healthcare facilities.

Features

Pie chart showing discharge proportions for the top diagnoses.
Clean legend and labeling for ease of interpretation.
Color-coded segments for clarity.

Diagnoses Included

Essential hypertension
Diabetes mellitus type 2
Heart failure
Chronic obstructive pulmonary disease (COPD)
Pneumonia
Sepsis
Acute kidney failure
Stroke
Asthma
Hip fracture


import streamlit as st
import plotly.express as px

# Data
labels = [
    'Essential hypertension', 'Diabetes mellitus type 2', 'Heart failure',
    'Chronic obstructive pulmonary', 'Pneumonia', 'Sepsis',
    'Acute kidney failure', 'Stroke', 'Asthma', 'Hip fracture'
]

sizes = [20.1, 16.1, 14.3, 12.5, 10.7, 8.85, 7.04, 5.23, 3.44, 1.79]

# Plot
fig = px.pie(
    names=labels,
    values=sizes,
    title='Discharges Proportion',
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Streamlit display
st.title('Number of Discharges')
st.plotly_chart(fig, use_container_width=True)






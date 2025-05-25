import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (replace with your actual data)
top_diagnoses = pd.Series({
    'Essential hypertension': 123456,
    'Diabetes mellitus type 2': 98765,
    'Heart failure': 87654,
    'Chronic obstructive pulmonary': 76543,
    'Pneumonia': 65432,
    'Sepsis': 54321,
    'Acute kidney failure': 43210,
    'Stroke': 32109,
    'Asthma': 21098,
    'Hip fracture': 10987
}).reset_index()

top_diagnoses.columns = ['Diagnosis Description', 'Number of Discharges']

st.title("Hospital Diagnosis Dashboard")

# Multi-select
selected = st.multiselect(
    "Select diagnosis descriptions to display:",
    options=top_diagnoses['Diagnosis Description'],
    default=top_diagnoses['Diagnosis Description'].tolist()
)

if not selected:
    st.write("Please select at least one diagnosis.")
else:
    filtered_df = top_diagnoses[top_diagnoses['Diagnosis Description'].isin(selected)]

    # KPIs
    total_discharges = filtered_df['Number of Discharges'].sum()
    max_diag = filtered_df.loc[filtered_df['Number of Discharges'].idxmax()]['Diagnosis Description']
    max_val = filtered_df['Number of Discharges'].max()

    col1, col2 = st.columns(2)
    col1.metric("Total Discharges", f"{total_discharges:,}")
    col2.metric("Top Diagnosis", f"{max_diag} ({max_val:,})")

    # Bar chart
    bar_fig = px.bar(
        filtered_df,
        x='Number of Discharges',
        y='Diagnosis Description',
        orientation='h',
        text='Number of Discharges',
        title='Number of Discharges by Diagnosis'
    )
    bar_fig.update_layout(yaxis=dict(autorange='reversed'))
    st.plotly_chart(bar_fig, use_container_width=True)

    # Pie chart
    pie_fig = px.pie(
        filtered_df,
        names='Diagnosis Description',
        values='Number of Discharges',
        title='Discharges Proportion'
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # Data table
    st.dataframe(filtered_df)

    # Download CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name='filtered_diagnoses.csv',
        mime='text/csv'
    )

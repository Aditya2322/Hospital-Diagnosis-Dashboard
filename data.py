import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import io
import base64

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

app = Dash(__name__)

def generate_csv_download_link(df):
    """Generate a CSV download link from dataframe"""
    csv_string = df.to_csv(index=False, encoding='utf-8')
    b64 = base64.b64encode(csv_string.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'data:text/csv;base64,{b64}'
    return href

app.layout = html.Div([
    html.H1("Hospital Diagnosis Dashboard"),
    html.P("Select diagnosis descriptions to display:"),

    dcc.Dropdown(
        id='diagnosis-dropdown',
        options=[
            {'label': diag, 'value': diag} for diag in top_diagnoses['Diagnosis Description']
        ],
        value=top_diagnoses['Diagnosis Description'].tolist(),  # default all selected
        multi=True,
        placeholder="Select one or more diagnosis descriptions"
    ),

    html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '40px', 'marginTop': '20px'}),

    dcc.Graph(id='bar-chart'),

    dcc.Graph(id='pie-chart'),

    html.H3("Data Table"),
    html.Div(id='data-table'),

    html.Br(),
    html.A(
        'Download Filtered Data as CSV',
        id='download-link',
        download='filtered_diagnoses.csv',
        href='',
        target='_blank',
        style={'fontSize': '18px', 'color': 'blue'}
    )
])

@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('data-table', 'children'),
    Output('kpi-cards', 'children'),
    Output('download-link', 'href'),
    Input('diagnosis-dropdown', 'value')
)
def update_dashboard(selected_diagnoses):
    if not selected_diagnoses:
        return {}, {}, html.Div("No diagnoses selected."), [], ''

    filtered_df = top_diagnoses[top_diagnoses['Diagnosis Description'].isin(selected_diagnoses)]

    # Bar chart
    bar_fig = px.bar(
        filtered_df,
        x='Number of Discharges',
        y='Diagnosis Description',
        orientation='h',
        text='Number of Discharges',
        template='plotly_white',
        title='Selected Diagnosis Descriptions by Number of Discharges'
    )
    bar_fig.update_layout(yaxis=dict(autorange='reversed'))
    bar_fig.update_traces(textposition='outside')

    # Pie chart
    pie_fig = px.pie(
        filtered_df,
        names='Diagnosis Description',
        values='Number of Discharges',
        title='Proportion of Discharges by Diagnosis',
        template='plotly_white'
    )

    # Data table
    table_header = [
        html.Thead(html.Tr([html.Th("Diagnosis Description"), html.Th("Number of Discharges")]))
    ]
    table_body = [
        html.Tr([html.Td(row['Diagnosis Description']), html.Td(row['Number of Discharges'])])
        for _, row in filtered_df.iterrows()
    ]
    table = html.Table(table_header + [html.Tbody(table_body)],
                       style={'width': '50%', 'border': '1px solid black', 'borderCollapse': 'collapse'})

    # KPI cards
    total_discharges = filtered_df['Number of Discharges'].sum()
    max_diagnosis = filtered_df.loc[filtered_df['Number of Discharges'].idxmax()]['Diagnosis Description']
    max_value = filtered_df['Number of Discharges'].max()

    kpi_style = {
        'padding': '20px',
        'border': '1px solid #ccc',
        'borderRadius': '8px',
        'width': '200px',
        'textAlign': 'center',
        'backgroundColor': '#f9f9f9'
    }

    kpi_cards = [
        html.Div([
            html.H4("Total Discharges"),
            html.P(f"{total_discharges:,}")
        ], style=kpi_style),
        html.Div([
            html.H4("Top Diagnosis"),
            html.P(f"{max_diagnosis} ({max_value:,})")
        ], style=kpi_style)
    ]

    # Download link
    csv_href = generate_csv_download_link(filtered_df)

    return bar_fig, pie_fig, table, kpi_cards, csv_href


if __name__ == '__main__':
    app.run(debug=True)

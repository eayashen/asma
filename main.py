import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Load the Data
df = pd.read_csv('data.csv')

# Create the Dash App
app = dash.Dash(__name__)
server = app.server

# Define the Layout with all components
app.layout = html.Div([
    html.H1("Diamond Data Dashboard"),

    # Tabs for Table, Description, and Visualization
    dcc.Tabs(id="tabs", value='table', children=[
        dcc.Tab(label='Table', value='table'),
        dcc.Tab(label='Description', value='description'),
        dcc.Tab(label='Visualization', value='visualization'),
    ]),

    html.Div(id='content'),

    # Hidden components for Visualization (initially hidden)
    html.Div(id='visualization-content', style={'display': 'none'}, children=[
        dcc.Dropdown(
            id='column-dropdown',
            options=[{'label': col, 'value': col} for col in df.select_dtypes(include='number').columns],
            value='carat'  # default value
        ),
        dcc.Graph(id='column-graph')
    ])
])

# Callback to update content based on selected tab
@app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'table':
        return html.Div([
            html.H2("Data Table"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.head(10).to_dict('records')
            )
        ])
    elif tab == 'description':
        return html.Div([
            html.H2("Variable Descriptions"),
            html.P("This dataset contains information about diamonds, including variables such as carat, cut, color, clarity, and price.")
        ])
    elif tab == 'visualization':
        # Show the dropdown and graph components when the Visualization tab is selected
        return html.Div(id='visualization-content', children=[
            html.H2("Column Graph"),
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include='number').columns],
                value='carat'
            ),
            dcc.Graph(id='column-graph')
        ])

# Callback to update graph based on selected column
@app.callback(
    Output('column-graph', 'figure'),
    Input('column-dropdown', 'value')
)
def update_graph(selected_column):
    fig = px.histogram(df, x=selected_column)
    fig.update_layout(title=f'Histogram of {selected_column}')
    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

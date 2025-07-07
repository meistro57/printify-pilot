import json
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import os

# Load JSON data
file_path = os.path.join(os.path.dirname(__file__), 'blueprints_data.json')
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Ensure images column contains only strings (first image from list)
if 'images' in df.columns:
    df['images'] = df['images'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "")

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Blueprints Data Viewer", className="text-center mt-4"),
    
    dcc.Input(id='search-box', type='text', placeholder='Search products...', className="form-control mb-3"),
    
    dash_table.DataTable(
        id='data-table',
        columns=[
            {'name': 'ID', 'id': 'id'},
            {'name': 'Title', 'id': 'title'},
            {'name': 'Brand', 'id': 'brand'},
            {'name': 'Model', 'id': 'model'}
        ],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        row_selectable='single'
    ),
    
    html.Div(id='product-details', className='mt-4')
])

@app.callback(
    Output('data-table', 'data'),
    Input('search-box', 'value')
)
def update_table(search_value):
    if not search_value:
        return df.to_dict('records')
    filtered_df = df[df['title'].str.contains(search_value, case=False, na=False)]
    return filtered_df.to_dict('records')

@app.callback(
    Output('product-details', 'children'),
    Input('data-table', 'selected_rows')
)
def display_product_details(selected_rows):
    if not selected_rows:
        return "Select a product to view details."
    
    row = df.iloc[selected_rows[0]]
    
    return dbc.Card([
        dbc.CardHeader(html.H4(row['title'])),
        dbc.CardBody([
            html.P(f"Brand: {row['brand']}", className="card-text"),
            html.P(f"Model: {row['model']}", className="card-text"),
            html.P(html.B("Description:")),
            html.P(html.Span(row['description'], className="card-text")),
            html.Img(src=row['images'], style={'width': '100%', 'marginTop': '10px'}) if row['images'] else ""
        ])
    ], className="shadow-lg p-3 mb-5 bg-white rounded")

if __name__ == '__main__':
    app.run(debug=True)

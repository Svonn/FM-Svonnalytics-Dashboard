import os
from dash import dcc, html


def create_navbar(position_options, role_options, nationality_options, division_options, directory):
    file_options = [{'label': file, 'value': os.path.join(directory, file)}
                    for file in os.listdir(directory) if file.endswith('.html')]

    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='file-dropdown',
                className='custom-dropdown',
                options=file_options,
                placeholder="Select a file",
                style={'backgroundColor': 'white', 'color': 'black'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '1%'}),
        html.Div([
            dcc.Dropdown(
                id='position-dropdown',
                options=[{'label': pos, 'value': pos} for pos in position_options],
                multi=True,
                placeholder="Select Positions",
                style={'backgroundColor': 'white', 'color': 'black'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '5%'}),
        html.Div([
            dcc.Dropdown(
                id='role-dropdown',
                options=role_options,
                multi=True,
                placeholder="Select Roles",
                style={'backgroundColor': 'white', 'color': 'black'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '5%'}),
        html.Div([
            dcc.Dropdown(
                id='nationality-dropdown',
                options=[{'label': nat, 'value': nat} for nat in nationality_options],
                multi=True,
                placeholder="Select Nationalities",
                style={'backgroundColor': 'white', 'color': 'black'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '5%'}),
        html.Div([
            dcc.Dropdown(
                id='division-dropdown',
                options=[{'label': div, 'value': div} for div in division_options],
                multi=True,
                placeholder="Select Divisions",
                style={'backgroundColor': 'white', 'color': 'black'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '5%'})
    ], style={'backgroundColor': '#444444', 'padding': '20px', 'color': 'white', 'display': 'flex', 'justifyContent': 'space-between'})


def create_app_layout(app, directory):
    app.layout = html.Div([
        create_navbar([], [], [], [], directory),

        dcc.Loading(
            id="loading-1",
            type="cube",
            children=[
                html.Div(id='data-table-container', style={'width': '100%'}),
                dcc.Store(id='processed-data-store'),
                dcc.Store(id='filtered-data-store'),
                dcc.Store(id='filtered-role-weightings-store'),
                dcc.Store(id='mode-store'),
            ],
            style={'marginTop': '200px'},
        ),
    ])

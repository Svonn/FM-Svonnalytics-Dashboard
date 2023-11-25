import time
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from data_processing import compute_averages_and_max, compute_league_averages, compute_overall_league_scores, get_relevant_columns, precompute_filtered_dataframes
from visualization import create_sorted_bar_chart
from configurations import role_mapping


def create_tabs(processed_data_frame, filtered_role_weightings):
    start_ts = time.time()

    tabs = []
    roles = list(filtered_role_weightings.keys())

    role_dfs = precompute_filtered_dataframes(processed_data_frame, roles)
    avg_per_club_per_role, max_per_club_per_role = compute_averages_and_max(
        role_dfs, roles)
    avg_per_league_per_role, max_per_league_per_role, avg_per_club, avg_max_per_club = compute_league_averages(
        role_dfs, roles, avg_per_club_per_role, max_per_club_per_role)
    avg_per_league, avg_of_max_per_club_per_role_per_league = compute_overall_league_scores(
        processed_data_frame, roles, avg_per_club_per_role, max_per_club_per_role)
    print(
        f"Calculating scores took {round(time.time() - start_ts, 2)} seconds")

    # Common dropdown options
    league_options = [{'label': league, 'value': league}
                      for league in processed_data_frame['Division'].unique()]
    league_options.append({'label': 'All', 'value': 'All'})

    # All Players Tab
    relevant_columns = get_relevant_columns("all", filtered_role_weightings)
    df_general_stats = processed_data_frame[relevant_columns]
    tabs.append(create_data_table_tab('All Players',
                df_general_stats, 'tab-all-players', 'Best Rating'))

    # Role-specific Tabs
    for role in roles:
        relevant_columns = get_relevant_columns(role, filtered_role_weightings)
        df_role_specific_stats = role_dfs[role][relevant_columns]
        tabs.append(create_data_table_tab(
            f'{role.upper()} Players', df_role_specific_stats, f'tab-{role}-players', f'{role} (Score)'))

        # Adding visualizations for each role
        tabs.extend(create_visualization_tabs(role, avg_per_club_per_role[role], max_per_club_per_role[role],
                                              avg_per_league_per_role[role], max_per_league_per_role[role]))

    # Aggregate Tabs
    tabs.append(create_aggregate_tab(
        'Player Average per Club', avg_per_club, league_options, 0))
    tabs.append(create_aggregate_tab('Best Player Average per Club',
                avg_max_per_club, league_options, 1))
    tabs.append(create_visualization_tab(
        'Average Players for Each League', avg_per_league, 'tab-aggregates-league-score'))
    tabs.append(create_visualization_tab('Average over best Players for each League',
                avg_of_max_per_club_per_role_per_league, 'tab-aggregates-league-max'))

    print(f"Creating tabs took {round(time.time() - start_ts, 2)} seconds")
    return tabs, avg_per_club, avg_max_per_club

# Helper functions for creating tabs


def create_data_table_tab(label, dataframe, tab_id, sort_column):
    data_table = dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[
            {
                'name': i,
                'id': i,
                'type': 'text',
                'presentation': 'input',
            } for i in dataframe.columns
        ],
        fixed_columns={'headers': True, 'data': 1},
        fixed_rows={'headers': True},
        style_table={'height': 'auto',
                     'overflowY': 'auto', 'minHeight': '300px'},
        style_cell={
            'minWidth': '100px', 'width': '150px', 'maxWidth': '250px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_header={
            'textAlign': 'center',
        },
        filter_action='native',
        sort_action='native',
        sort_mode='single',
        # Default sorting
        sort_by=[{'column_id': sort_column, 'direction': 'desc'}],
        page_size=25,
    )
    return dcc.Tab(id=tab_id, label=label, children=[data_table])


def create_visualization_tabs(role, club_avg, club_max, league_avg, league_max_avg):
    tabs = []
    # AVERAGE SCORES BY CLUB
    club_averages_sorted = dict(
        sorted(club_avg.items(), key=lambda item: item[1]))
    fig_club_averages = create_sorted_bar_chart(
        x=list(club_averages_sorted.keys()),
        y=list(club_averages_sorted.values()),
        title=f'Average {role.upper()} Score by Club',
        xaxis_label='Club',
        yaxis_label=f'{role.upper()} Average Score'
    )
    tabs.append(dcc.Tab(id=f"tab-{role}-club-averages", label=f'{role.upper()} Club Averages',
                children=[dcc.Graph(figure=fig_club_averages)]))

    # MAX SCORES BY CLUB
    club_max_sorted = dict(sorted(club_max.items(), key=lambda item: item[1]))
    fig_club_averages = create_sorted_bar_chart(
        x=list(club_max_sorted.keys()),
        y=list(club_max_sorted.values()),
        title=f'Max {role.upper()} Score by Club',
        xaxis_label='Club',
        yaxis_label=f'{role.upper()} Max Score'
    )
    tabs.append(dcc.Tab(id=f"tab-{role}-club-max", label=f'{role.upper()} Club Maximum',
                children=[dcc.Graph(figure=fig_club_averages)]))

    # AVERAGE SCORES BY LEAGUE
    league_averages_sorted = dict(
        sorted(league_avg.items(), key=lambda item: item[1]))
    fig_league_averages = create_sorted_bar_chart(
        x=list(league_averages_sorted.keys()),
        y=list(league_averages_sorted.values()),
        title=f'Average {role.upper()} Score by League',
        xaxis_label='League',
        yaxis_label=f'{role.upper()} Average Score'
    )
    tabs.append(dcc.Tab(id=f"tab-{role}-league-averages", label=f'{role.upper()} League Averages',
                children=[dcc.Graph(figure=fig_league_averages)]))

    # AVERAGE MAX SCORES BY CLUB
    max_club_averages_sorted = dict(
        sorted(league_max_avg.items(), key=lambda item: item[1]))
    fig_max_club_averages = create_sorted_bar_chart(
        x=list(max_club_averages_sorted.keys()),
        y=list(max_club_averages_sorted.values()),
        title=f'Average of Maximum {role.upper()} Score per Club per League',
        xaxis_label='League',
        yaxis_label=f'Average of Max {role.upper()} Score'
    )
    tabs.append(dcc.Tab(id=f"tab-{role}-max-club-averages", label=f'Max {role.upper()} Club Averages',
                children=[dcc.Graph(figure=fig_max_club_averages)]))

    return tabs


def create_aggregate_tab(label, scores, league_options, index):
    dropdown = dcc.Dropdown(
        id={'type': 'dynamic-dropdown', 'index': index},
        options=league_options,
        value=None,
        placeholder="Select a league to highlight",
    )
    figure = create_sorted_bar_chart(
        x=list(scores.keys()),
        y=list(scores.values()),
        title=label,
        xaxis_label='Club',
        yaxis_label='Average Score'
    )
    return dcc.Tab(
        id={'type': 'dynamic-tab', 'index': index},
        label=label,
        children=[
            html.Div([html.Label('Select a league to highlight:'),
                     dropdown], className='dropdown-container'),
            dcc.Graph(id={'type': 'dynamic-graph',
                      'index': index}, figure=figure)
        ]
    )


def create_visualization_tab(label, scores, tab_id):
    figure = create_sorted_bar_chart(
        x=list(scores.keys()),
        y=list(scores.values()),
        title=label,
        xaxis_label='Club',
        yaxis_label='Average Best Player'
    )
    return dcc.Tab(id=tab_id, label=label, children=[dcc.Graph(figure=figure)])


def create_tabs_content(roles):

    role_tabs_content = []

    for role in roles:
        dropdown_items = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Players", href=f"#tab-{role}-players"),
                dbc.DropdownMenuItem(
                    "Club Averages", href=f"#tab-{role}-club-averages"),
                dbc.DropdownMenuItem(
                    "Club Best", href=f"#tab-{role}-club-max"),
                dbc.DropdownMenuItem(
                    "League Averages", href=f"#tab-{role}-league-averages"),
                dbc.DropdownMenuItem(
                    "League Best", href=f"#tab-{role}-max-club-averages"),
            ],
            nav=True,
            in_navbar=True,
            label=f"{role.upper()}",
            style={'color': 'white'}
        )
        role_tabs_content.append(dbc.NavItem(dropdown_items, className="ms-auto"))

    dropdown_items = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Club Overall Scores",
                                 href="#tab-aggregates-club-score"),
            dbc.DropdownMenuItem(
                "Club Max Scores", href="#tab-aggregates-club-max"),
            dbc.DropdownMenuItem("League Overall Scores",
                                 href="#tab-aggregates-league-score"),
            dbc.DropdownMenuItem("League Max Scores",
                                 href="#tab-aggregates-league-max"),
        ],
        nav=True,
        in_navbar=True,
        label=f"Aggregated",
        style={'color': 'white'}
    )
    role_tabs_content.append(dbc.NavItem(dropdown_items, className="ms-auto"))
    return role_tabs_content


def create_app_layout(app, html_export_path):

    dropdown_style = {
        'minWidth': '250px',
        'width': '100%',
        'border': 'none',
        'color': 'white',  # Text color
        'backgroundColor': '#343a40',  # Match the navbar's dark background color
    }
    directory_dropdown = dcc.Dropdown(
        id='directory-dropdown',
        options=[
            {'label': 'FM24 Files', 'value': html_export_path}
        ],
        value=html_export_path,  # default value
        className='custom-dropdown',
        style=dropdown_style
    )

    file_dropdown = dcc.Dropdown(
        id='file-dropdown',
        className='custom-dropdown',
        style=dropdown_style
    )

    current_tab_label = html.Div(
        id='current-tab-label',
        className='ms-3',  # Add some left margin to separate it from the delimiter
        style={'color': 'white'}
    )

    navbar_collapse = dbc.Collapse(
        children=dbc.Nav([], className="ms-auto", navbar=True),
        id="navbar-collapse",
        navbar=True,
        style={'marginLeft': '200px'},
    )

    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    "FM Analytics Dashboard",
                    href="#",
                    className="me-auto",
                    style={'marginLeft': '25px'}
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(directory_dropdown),
                        dbc.NavItem(file_dropdown),
                    ],
                    # Use d-flex to apply flexbox properties
                    className="align-items-center d-flex",
                    navbar=True,
                    style={'marginLeft': '25px'}
                ),
                current_tab_label,
                navbar_collapse
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-4",
    )

    file_update_interval = dcc.Interval(
        id='interval-update-files',
        interval=5*1000,  # in milliseconds, so 5*1000 for 5 seconds
        n_intervals=0
    )

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        navbar,
        dcc.Loading(
            id="loading-1",
            type="cube",  # You can choose from 'graph', 'cube', 'circle', 'dot', or 'default'
            children=html.Div(id="tab-content", className="p-4"),
            style={'marginTop': '200px'},
        ),
        html.Div(id='dummy-div', style={'display': 'none'}),
        file_update_interval
    ])

import html
import json
import os
from dash.dependencies import Input, Output, MATCH, State
from app_layout import create_tabs
from data_processing import  process_file  
from visualization import create_sorted_bar_chart  
from configurations import role_mapping
import dash  
from dash import callback_context

club_league_mapping = None  # Initialize as None, will be set by calling function  
roles = list(role_mapping.keys())  
tabs = None
processed_data_frame = None
avg_per_club = None
avg_max_per_club = None

def set_processed_data_frame(p):
    global processed_data_frame
    processed_data_frame = p

def set_tabs(t):
    global tabs
    tabs = t

def set_aggregated_dfs(avg_club, max_club):
    global avg_per_club
    avg_per_club = avg_club
    global avg_max_per_club
    avg_max_per_club = max_club

def set_club_league_mapping(processed_data_frame):  
    global club_league_mapping  
    club_league_mapping = processed_data_frame[['Verein', 'Liga']].drop_duplicates().set_index('Verein').to_dict()['Liga']  
  
def register_callbacks(app: dash.Dash):
    @app.callback(
        Output('file-dropdown', 'options'),
        [Input('directory-dropdown', 'value'), Input('interval-update-files', 'n_intervals')]
    )
    def set_file_options(selected_directory, _):
        if selected_directory is None:
            raise dash.exceptions.PreventUpdate

        files = os.listdir(selected_directory)
        return [{'label': file, 'value': os.path.join(selected_directory, file)} for file in files]


    @app.callback(
        [Output("tab-content", "children"), Output("current-tab-label", "children")],
        [Input("url", "hash"), Input("file-dropdown", "value")],
        [State("directory-dropdown", "value")]
    )
    def display_tab_content(hash_value, selected_file, selected_directory):
        if selected_file is None:
            raise dash.exceptions.PreventUpdate

        def parse_hash(hash_value):
            if hash_value is None or hash_value == '':
                return None
            hash_parts = hash_value.lstrip('#').split('-', 2)
            if len(hash_parts) == 3 and hash_parts[0] == 'tab':
                return hash_parts[1], hash_parts[2]
            return None

        current_tab = parse_hash(hash_value)

        ctx = callback_context
        if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == "file-dropdown":
            if not selected_file:
                raise dash.exceptions.PreventUpdate
            processed_data_frame = process_file(selected_file)
            new_tabs, avg_club, avg_max_club = create_tabs(processed_data_frame)
            set_club_league_mapping(processed_data_frame) 
            set_tabs(new_tabs)
            set_aggregated_dfs(avg_club, avg_max_club)
            set_processed_data_frame(processed_data_frame)

        if current_tab:
            role, view = current_tab
            if role in roles:
                if view == "players":
                    index = roles.index(role) * 5 + 1
                elif view == "club-averages":
                    index = roles.index(role) * 5 + 2
                elif view == "club-max":
                    index = roles.index(role) * 5 + 3
                elif view == "league-averages":
                    index = roles.index(role) * 5 + 4
                elif view == "max-club-averages":
                    index = roles.index(role) * 5 + 5
                else:
                    return "Content not found"
                return tabs[index].children, tabs[index].label
            elif role == "aggregates":
                aggregates_mapping = {
                    "club-score": 0,
                    "club-max": 1,
                    "league-score": 2,
                    "league-max": 3,
                }
                index = aggregates_mapping.get(view)
                if index is not None:
                    return tabs[-4 + index].children, tabs[-4 + index].label
                else:
                    return "Aggregate not found"

        return tabs[0].children, tabs[0].label

    @app.callback(
        Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
        [Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value')],
        prevent_initial_call=True
    )
    def update_graph(selected_league):
        ctx = dash.callback_context

        if not ctx.triggered:
            return dash.no_update

        # Get the 'index' and 'type' from the triggered element's ID
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        trigger_id_dict = json.loads(trigger_id)
        index = trigger_id_dict['index']
        graph_type = trigger_id_dict['type']

        # Depending on the 'index', update the appropriate graph
        if graph_type == 'dynamic-dropdown':
            if index == 0:
                updated_figure = create_figure_for_average_score(selected_league)
            elif index == 1:
                updated_figure = create_figure_for_max_score(selected_league)
        else:
            return dash.no_update

        return updated_figure
            
    def create_figure_for_average_score(selected_league):
                
        return create_sorted_bar_chart(
            x=list(avg_per_club.keys()),
            y=list(avg_per_club.values()),
            title='Player Average per Club',
            xaxis_label='Club',
            yaxis_label='Average Score',
            highlighted_league=selected_league,
            club_league_mapping=club_league_mapping
        )
        
    def create_figure_for_max_score(selected_league):
        
        return create_sorted_bar_chart(
            x=list(avg_max_per_club.keys()),
            y=list(avg_max_per_club.values()),
            title='Best Player Average per Club',
            xaxis_label='Club',
            yaxis_label='Average Best Player',
            highlighted_league=selected_league,
            club_league_mapping=club_league_mapping
        )
        
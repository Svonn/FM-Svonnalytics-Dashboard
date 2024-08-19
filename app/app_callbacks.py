from io import StringIO

import dash
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output, State
from data_processing import process_file, get_hidden_columns, get_relevant_columns


def register_callbacks(app: dash.Dash):
    @app.callback(
        [Output('position-dropdown', 'options'),
         Output('role-dropdown', 'options'),
         Output('nationality-dropdown', 'options'),
         Output('division-dropdown', 'options'),
         Output('processed-data-store', 'data'),
         Output('filtered-role-weightings-store', 'data'),
         Output('mode-store', 'data'),
         # Add outputs to reset dropdown values
         Output('position-dropdown', 'value'),
         Output('role-dropdown', 'value'),
         Output('nationality-dropdown', 'value'),
         Output('division-dropdown', 'value')],
        [Input('file-dropdown', 'value')]
    )
    def update_file_selection(file_path):
        if not file_path:
            raise dash.exceptions.PreventUpdate
        df, filtered_role_weightings, position_options, mode = process_file(file_path)
        roles = list(filtered_role_weightings.keys())
        position_dropdown_options = [{'label': pos, 'value': pos} for pos in position_options]
        role_dropdown_options = [{'label': role, 'value': role} for role in roles]
        # check if df has Nat 1 and Nat 2 columns
        if 'Nat 1' in df.columns and 'Nat 2' in df.columns:
            nationality_options = [{'label': nat, 'value': nat} for nat in pd.concat([df['Nat 1'], df['Nat 2']]).unique()]
        else:
            nationality_options = []

        if 'Division' in df.columns:
            division_options = [{'label': div, 'value': div} for div in df['Division'].unique()]
        else:
            division_options = []
        processed_data = df.to_json(date_format='iso', orient='split')
        return (position_dropdown_options, role_dropdown_options, nationality_options, division_options,
                processed_data, filtered_role_weightings, mode, None, [], [], [])

    @app.callback(
        [Output('data-table-container', 'children'),
         Output('filtered-data-store', 'data')],
        [Input('position-dropdown', 'value'),
         Input('role-dropdown', 'value'),
         Input('nationality-dropdown', 'value'),
         Input('division-dropdown', 'value')],
        [State('processed-data-store', 'data'),
         State('filtered-role-weightings-store', 'data'),
         State('mode-store', 'data')]
    )
    def update_data_table(selected_positions, selected_role, selected_nationalities, selected_divisions, processed_data_json, filtered_role_weightings, mode):
        if not processed_data_json:
            raise dash.exceptions.PreventUpdate
        print(f"Selected positions: {selected_positions}, Selected role: {selected_role}")

        processed_df = pd.read_json(StringIO(processed_data_json), orient='split')

        if selected_positions:
            processed_df = processed_df[processed_df['Position'].apply(lambda x: any(pos in x for pos in selected_positions))]
        if selected_nationalities:
            processed_df = processed_df[processed_df['Nat 1'].isin(selected_nationalities) | processed_df['Nat 2'].isin(selected_nationalities)]
        if selected_divisions:
            processed_df = processed_df[processed_df['Division'].isin(selected_divisions)]

        if selected_role:
            # TODO: Handle multi role selection
            selected_role = selected_role[0]
        else:
            selected_role = "all"

        relevant_columns = get_relevant_columns(selected_role, filtered_role_weightings, mode)
        hidden_columns = get_hidden_columns(selected_role, filtered_role_weightings, mode)
        sort_column = f'{selected_role} (Rating)' if selected_role != "all" else "Best Rating"

        data_table = dash_table.DataTable(
            data=processed_df.to_dict('records'),
            id={'type': 'dynamic-datatable'},
            columns=[
                        {
                            'name': i,
                            'id': i,
                            'type': 'text',
                            'presentation': 'input',
                            'format': {'specifier': '.1f'},
                            'hideable': True
                        } for i in relevant_columns
                    ] + [
                        {
                            'name': i,
                            'id': i,
                            'hideable': True
                        } for i in hidden_columns
                    ],
            hidden_columns=[i for i in hidden_columns],
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
            filter_action='custom',
            sort_action='custom',
            sort_mode='single',
            # Default sorting
            sort_by=[{'column_id': sort_column, 'direction': 'desc'}],
            page_size=100,
        )

        return data_table, processed_df.to_json(date_format='iso', orient='split')

    @app.callback(
        Output({'type': 'dynamic-datatable'}, 'data'),
        [Input({'type': 'dynamic-datatable'}, 'sort_by'),
         Input({'type': 'dynamic-datatable'}, 'filter_query')],
        [State('filtered-data-store', 'data')]
    )
    def update_table(sort_by, filter_query, filtered_data_json):
        if not filtered_data_json or not (sort_by or filter_query):
            raise dash.exceptions.PreventUpdate

        print(f"Sort by: {sort_by}, Filter query: {filter_query}")
        df = pd.read_json(StringIO(filtered_data_json), orient='split')

        # Handle filtering
        if filter_query:
            filter_query = filter_query.replace(' s', ' ')
            filtering_expressions = filter_query.split(' && ')
            for filter_part in filtering_expressions:
                col_name, operator, filter_value = split_filter_part(filter_part)

                if col_name.endswith('Value') and not col_name.startswith('Full'):
                    col_name = f"Full {col_name}"

                if col_name == "Wage":
                    col_name = "Wage numerical"

                if isinstance(filter_value, str) and ("Wage" in col_name or "Value" in col_name):
                    filter_value = filter_value.lower().replace("k", "e3").replace("mio", "e6").replace("m", "e6")

                if operator == 'contains':
                    query_string = f"""`{col_name}`.str.contains("{filter_value}")"""
                else:
                    query_string = f"`{col_name}` {operator} {filter_value}"
                print(f"Executing query: {query_string}")
                df = df.query(query_string, engine='python')

        # Handle sorting
        if sort_by:
            col_id = sort_by[0]['column_id']
            direction = sort_by[0]['direction']

            if col_id.endswith('(Rating)'):
                col_id = col_id.replace('(Rating)', '(Average Rating)')

            if col_id.endswith('Value'):
                col_id = f"Full {col_id}"

            if col_id == "Wage":
                col_id = "Wage numerical"

            df = df.sort_values(by=col_id, ascending=(direction == 'asc'))

        records = df.to_dict('records')
        return records

    def split_filter_part(filter_part):
        """Utility function to split the filter expression into parts"""
        operators = ['>= ', '<= ', '>', '<', '!= ', '= ', ' contains ']
        for operator in operators:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                # Remove leading and trailing whitespaces from column name and value
                name = name.strip()
                value_part = value_part.strip()
                # If value is numeric, convert it
                if value_part.replace('.', '', 1).isdigit():
                    value_part = float(value_part)
                return name, operator.strip(), value_part
        return [None] * 3

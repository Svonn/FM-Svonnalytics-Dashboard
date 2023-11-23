import numpy as np
import pandas as pd
from configurations import foot_rating_conversion, role_attributes, stat_groups, role_mapping
import re

def calculate_score_optimized(squad_rawdata, attribute_weightings, threshold=14):
    for attr, weight in attribute_weightings.items():
        attribute_values = squad_rawdata[attr]
        base = 1.3 + (weight * 0.1)
        try:
            malus = np.where(attribute_values < threshold, np.power(base, threshold - attribute_values) - 1, 0)
        except Exception as e:
            print("Error in attribute: ", attr)
            raise e
        adjusted_attribute_values = np.maximum(0, attribute_values - malus)
        squad_rawdata[attr + '_score'] = adjusted_attribute_values * weight
    total_score = squad_rawdata[[attr + '_score' for attr in attribute_weightings]].sum(axis=1)
    return total_score

def normalize_and_round(scores, total_weighting):
    return np.round(scores / total_weighting, 1)

def process_file(file_path):
    print()
    print("Processing file: ", file_path)
    start_ts = pd.Timestamp.now()
    squad_rawdata_list = pd.read_html(file_path, header=0, encoding="utf-8", keep_default_na=False)
    squad_rawdata = squad_rawdata_list[0]

    # FM23/24 specific column mappings
    column_mappings = {
        'Verw. %': 'Chancenverwertung (%)',
        'PrsErf/90': 'PrsErf',
        'Zwk/90': 'Tck/90',
        'xG/Schuss': 'xG/Sch (%)'
    }
    squad_rawdata.rename(columns=column_mappings, inplace=True)

    left_foot_scores = squad_rawdata['Linker Fuß'].map(foot_rating_conversion)
    right_foot_scores = squad_rawdata['Rechter Fuß'].map(foot_rating_conversion)
    squad_rawdata['WeakFoot'] = np.minimum(left_foot_scores, right_foot_scores)

    for role, config in role_attributes.items():
        total_weighting = sum(config['attributes'].values())
        score_column = f'{role}_score'
        
        squad_rawdata[score_column] = calculate_score_optimized(squad_rawdata, config['attributes'])
        normalized_column = f'{role}'
        squad_rawdata[normalized_column] = normalize_and_round(squad_rawdata[score_column], total_weighting)

    role_columns = [f'{role}' for role in role_attributes.keys()]
    squad_rawdata['best_role_score'] = squad_rawdata[role_columns].max(axis=1)
    squad_rawdata['best_role'] = squad_rawdata[role_columns].idxmax(axis=1)

    all_stats = list(role_attributes.keys())
    all_stats.extend(['Start11', 'Ø Note'])

    for role, config in role_attributes.items():
        role_stats = config['stats']
        all_stats.extend([stat for group in role_stats for stat in stat_groups[group]])
    all_stats = sorted(set(all_stats))

    for col in all_stats:
        if squad_rawdata[col].dtype == 'object':
            if squad_rawdata[col].str.contains('%').any():
                squad_rawdata[col] = squad_rawdata[col].str.rstrip('%').replace('-', '0').astype(float) / 100
            elif squad_rawdata[col].str.contains('km').any():
                squad_rawdata[col] = squad_rawdata[col].str.rstrip('km').replace('-', '0').astype(float)
            else:
                squad_rawdata[col] = pd.to_numeric(squad_rawdata[col].replace('-', '0'), errors='coerce').fillna(0)
        else:
            # If not an object type, convert directly to numeric
            squad_rawdata[col] = pd.to_numeric(squad_rawdata[col], errors='coerce').fillna(0)


    columns_to_display = [
        'Name', 'Alter', 'Verein', 'Liga', 'Transferwert', 'Gehalt', 'Position', 
        'Persönlichkeit', 'Medienumgang', 'Linker Fuß', 'Rechter Fuß', 'best_role', 
        'best_role_score'
    ]
    columns_to_display.extend(all_stats)
    
    print(f"Processing time: {round((pd.Timestamp.now() - start_ts).total_seconds(), 2)} seconds")
    print("Data points: ", len(squad_rawdata))
    return squad_rawdata[columns_to_display]


def get_relevant_columns(role):
    if role == "all":
        stats_to_include = [role for role in role_attributes.keys()]
        fixed_columns = ['Name', 'Verein', 'Alter', 'Start11', 'Ø Note', 'best_role', 'best_role_score',  'Liga', 'Transferwert', 'Gehalt', 'Position', 'Persönlichkeit', 'Medienumgang', 'Linker Fuß', 'Rechter Fuß']
        return fixed_columns[:7] + stats_to_include + fixed_columns[7:]
    else:
        stats_to_include = [stat for group in role_attributes[role]['stats'] for stat in stat_groups[group]]
        fixed_columns = ['Name', 'Verein', 'Alter', 'Transferwert', 'Gehalt',  role, 'best_role', 'best_role_score', 'Start11', 'Ø Note',  'Liga',  'Position', 'Persönlichkeit', 'Medienumgang', 'Linker Fuß', 'Rechter Fuß']
        return fixed_columns[:8] + stats_to_include + fixed_columns[8:]


def parse_positions(position_string):
    positions = position_string.split(', ')
    all_positions = []
    for position in positions:
        if '(' not in position:
            all_positions.append(position.strip())
            continue
        
        field_position, locations = re.match(r'([A-Z/]+) ?\(([A-Z]+)\)', position).groups()
        field_positions = field_position.split('/')
        
        for fp in field_positions:
            for loc in locations:
                all_positions.append(f'{fp}({loc})')
    return all_positions

def can_play_role(data_frame, role):
    valid_positions = set(role_mapping[role])
    return data_frame['Position'].apply(lambda positions: bool(set(parse_positions(positions)) & valid_positions))

def filter_by_role(data_frame, role):
    return data_frame[can_play_role(data_frame, role)]

def precompute_filtered_dataframes(data_frame, roles):
    filtered_dfs = {}
    for role in roles:
        filtered_dfs[role] = filter_by_role(data_frame, role)
    return filtered_dfs

def compute_averages_and_max(filtered_dfs, roles):
    avg_per_club_per_role = {}
    max_per_club_per_role = {}
    for role in roles:
        squad_data = filtered_dfs[role]
        avg_per_club_per_role[role] = squad_data.groupby('Verein')[role].mean().to_dict()
        max_per_club_per_role[role] = squad_data.groupby('Verein')[role].max().to_dict()
    return avg_per_club_per_role, max_per_club_per_role

def compute_league_averages(filtered_dfs, roles, avg_per_club_per_role, max_per_club_per_role):
    avg_per_league_per_role = {}
    max_per_league_per_role = {}
    unique_clubs = set()
    
    for role in roles:
        squad_data = filtered_dfs[role]
        avg_per_league_per_role[role] = squad_data.groupby(['Liga', 'Verein'])[role].mean().groupby('Liga').mean().to_dict()
        max_per_league_per_role[role] = squad_data.groupby(['Liga', 'Verein'])[role].max().groupby('Liga').mean().to_dict()
        unique_clubs.update(squad_data['Verein'].unique())

    avg_per_club = {club: pd.Series({role: avg_per_club_per_role[role].get(club, 0) for role in roles}).mean()
                    for club in unique_clubs}
    
    avg_max_per_club = {club: pd.Series({role: max_per_club_per_role[role].get(club, 0) for role in roles}).mean()
                    for club in unique_clubs}

    return avg_per_league_per_role, max_per_league_per_role, avg_per_club, avg_max_per_club


def compute_overall_league_scores(data_frame, roles, avg_per_club_per_role, max_per_club_per_role):
    avg_per_league = {}
    avg_of_max_per_club_per_role_per_league = {}
    for league in data_frame['Liga'].unique():
        league_data = data_frame[data_frame['Liga'] == league]
        club_averages = []
        club_best_averages = []
        for club in league_data['Verein'].unique():
            club_averages.append(pd.Series({role: avg_per_club_per_role[role].get(club, 0) for role in roles}).mean())
            club_best_averages.append(pd.Series({role: max_per_club_per_role[role].get(club, 0) for role in roles}).mean())
        avg_per_league[league] = pd.Series(club_averages).mean()
        avg_of_max_per_club_per_role_per_league[league] = pd.Series(club_best_averages).mean()

    return avg_per_league, avg_of_max_per_club_per_role_per_league
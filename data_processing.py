import json
import math
import numpy as np
import pandas as pd
from configurations import foot_rating_conversion, role_mapping, stat_sets, role_weightings
import re
from sklearn.preprocessing import PowerTransformer


def calculate_score_with_malus(data, weightings, threshold=14, max_score=20, invert_negative=False):
    scores = {}
    for stat, weight in weightings.items():
        stat_values = data[stat] if isinstance(data, pd.DataFrame) else data

        if invert_negative:
            stat_values = max_score - stat_values

        base = 1.3 + (weight * 0.1)
        try:
            malus = np.where(stat_values < threshold, np.power(
                base, threshold - stat_values) - 1, 0)
        except Exception as e:
            print(f"Error in stat: {stat}")
            raise e

        adjusted_stat_values = np.maximum(0, stat_values - malus)
        scores[stat + '_score'] = adjusted_stat_values * weight

    total_score = sum(scores.values())
    return pd.Series(total_score)

def calculate_score_range_with_malus(data, weightings, threshold=12):
    scores_lower = {}
    scores_upper = {}
    for attribute_value, weight in weightings.items():
        lower_range = np.array(data[f'{attribute_value}_lower'])
        upper_range = np.array(data[f'{attribute_value}_upper'])
        base = 1.25 + (weight * 0.1)
        try:
            lower_malus = np.where(lower_range < threshold, np.power(base, threshold - lower_range) - 1, 0)
            upper_malus = np.where(upper_range < threshold, np.power(base, threshold - upper_range) - 1, 0)
        except Exception as e:
            print(f"Error in stat: {attribute_value}")
            raise e

        scores_lower[attribute_value + '_score'] = np.maximum(0, lower_range - lower_malus) * weight
        scores_upper[attribute_value + '_score'] = np.maximum(0, upper_range - upper_malus) * weight

    total_score_lower = sum(scores_lower.values())
    total_score_upper = sum(scores_upper.values())
    return pd.Series(total_score_lower), pd.Series(total_score_upper)


def normalize_and_round(scores, total_weighting):
    return np.round(scores / total_weighting, 1)


def convert_stats_to_scores(squad_df, stat_sets, max_score=20, role=None):
    if role:
        # Filter data for players suitable for the specified role
        players_for_role = can_play_role(squad_df, role)
        filtered_df = squad_df[players_for_role]
    else:
        filtered_df = squad_df

    percentile = filtered_df['Starting 11'].quantile(0.4)
    min_starting_11 = min(10, math.ceil(percentile))
    # Filter the data to include only players above this threshold
    filtered_data = filtered_df[filtered_df['Starting 11'] >= min_starting_11]
    all_stats = list(set([stat for set_stats in stat_sets.values()
                     for stat in set_stats.keys()]))
    # Apply PowerTransformer on the filtered data
    pt = PowerTransformer()
    transformed_data = pt.fit_transform(filtered_data[all_stats])
    transformed_df = pd.DataFrame(
        transformed_data, columns=all_stats, index=filtered_data.index)

    min_val, max_val = transformed_df.min(), transformed_df.max()
    inverted_stats = ['Possession Lost per 90 minutes',
                      'Team Goals Conceded per 90 minutes']

    for stat in all_stats:
        if stat in inverted_stats and stat in transformed_df.columns:
            transformed_df[stat] = max_val[stat] - transformed_df[stat]

    normalized_stats = (transformed_df - min_val) / (max_val - min_val)
    normalized_stats = normalized_stats.clip(0, 1) * max_score

    # Initialize a DataFrame with zeros for all stats, using a floating-point data type
    zero_data = pd.DataFrame(0.0, index=filtered_df.index, columns=[
                             stat for stat in all_stats])

    # Update this DataFrame with the transformed stats for eligible players
    for stat in all_stats:
        if stat in normalized_stats.columns:
            zero_data.loc[filtered_data.index, stat] = normalized_stats[stat]

    return zero_data


def calculate_stat_set_scores(squad_df, stat_sets, filtered_role_weightings, max_score=20):

    new_scores = {}
    normalized_stats = convert_stats_to_scores(squad_df, stat_sets, max_score)
    for set_name, stats in stat_sets.items():
        total_set_weight = sum(stats.values())
        normalized_set_score = calculate_score_with_malus(
            normalized_stats, stats, threshold=0, max_score=max_score)
        new_scores[set_name] = normalize_and_round(
            normalized_set_score, total_set_weight)

    for role in filtered_role_weightings.keys():
        normalized_stats_role = convert_stats_to_scores(
            squad_df, stat_sets, max_score, role)
        for set_name, stats in stat_sets.items():
            if set_name in filtered_role_weightings[role].get('stats', {}):
                role_set_score = calculate_score_with_malus(
                    normalized_stats_role, stats, threshold=0, max_score=max_score)
                normalized_role_set_score = normalize_and_round(
                    role_set_score, sum(stats.values()))
                new_scores[f'{set_name} ({role})'] = normalized_role_set_score

    return pd.concat([squad_df, pd.DataFrame(new_scores)], axis=1)


def calculate_role_scores_based_on_stats(squad_df, filtered_role_weightings):
    for role, config in filtered_role_weightings.items():
        if 'stats' in config:
            total_stat_weight = sum(config['stats'].values())
            role_stat_scores = np.sum(
                [squad_df[f'{set_name} ({role})'] * weight for set_name, weight in config['stats'].items()], axis=0)
            normalized_role_stat_score = normalize_and_round(
                role_stat_scores, total_stat_weight)

            if np.isnan(normalized_role_stat_score).any():
                normalized_role_stat_score = np.nan_to_num(
                    normalized_role_stat_score)

            # Scale the Stats scores
            max_role_score = squad_df[f'{role} (Average Score)'].max()
            min_stat_score = np.min(normalized_role_stat_score)
            max_stat_score = np.max(normalized_role_stat_score)

            # Check for constant stat scores and avoid division by zero
            if max_stat_score != min_stat_score:
                scaled_role_stat_score = (normalized_role_stat_score - min_stat_score) * (
                    max_role_score / (max_stat_score - min_stat_score))
            else:
                scaled_role_stat_score = normalized_role_stat_score * max_role_score

            squad_df[f'{role} (Stats)'] = np.round(scaled_role_stat_score, 1)

    return squad_df

def calculate_combined_role_scores(squad_df, filtered_role_weightings):
    for role in filtered_role_weightings.keys():
        score_col = f'{role} (Average Score)'
        stats_col = f'{role} (Stats)'
        combined_col = f'{role} (Combined)'

        squad_df[combined_col] = np.round(squad_df[[score_col, stats_col]].mean(axis=1), 1)

    return squad_df

def calculate_performance(squad_df, filtered_role_weightings):
    for role in filtered_role_weightings.keys():
        score_col = f'{role} (Average Score)'
        stats_col = f'{role} (Stats)'
        performance_col = f'{role} (Performance)'

        # Calculate performance as Stats / Score * 100%
        # Replace division by zero with NaN
        with np.errstate(divide='ignore', invalid='ignore'):
            squad_df[performance_col] = np.round((squad_df[stats_col] / squad_df[score_col]) * 100, 1)
            squad_df[performance_col].replace([np.inf, -np.inf], np.nan, inplace=True)

    return squad_df

def filter_role_weightings(squad_df, role_weightings):
    filtered_role_weightings = {}

    for role in role_weightings.keys():
        if can_play_role(squad_df, role).any():
            filtered_role_weightings[role] = role_weightings[role]
            
    return filtered_role_weightings

def process_attribute_column(col):
    # Check if the column contains any '-' or range patterns
    if col.str.contains('-').any() or col.eq('-').any():
        # Handle the mix of Integers, Integer Ranges, and "-" cases
        split_col = col.str.split('-', expand=True)
        split_col[1].fillna(split_col[0], inplace=True)  # Duplicate integers where no range is present

        # Replace empty strings (originally '-') with '1' for lower bound and '20' for upper bound
        split_col[0] = split_col[0].replace({'': '1'}).fillna('1')
        split_col[1] = split_col[1].replace({'': '20'}).fillna('20')
    else:
        # For columns with only integers, duplicate the column
        split_col = pd.concat([col, col], axis=1)

    # Convert to float
    try:
        split_col = split_col.astype(float)
    except ValueError:
        print(f"Error converting column {col.name} to float")
        raise

    # Rename columns to lower and upper
    split_col.columns = [f'{col.name}_lower', f'{col.name}_upper']

    return split_col

def process_transfer_value(value):
    if value == "Not for Sale" or value == "Steht nicht zum Verkauf":
        return np.inf, np.inf, "∞", "∞"
    if value == "Unknown" or value == "Unbekannt":
        return np.nan, np.nan, "Unbekannt", "Unbekannt"
    currency_symbols_regex = r'[\$\£\€\¥\₹\₩\₪\₺\₦\₡\₴\₲\₱\฿\₫\₭\₼\₽\₾\₸\៛\₠\₢\₣\₤\₥\₦\₧\₨\₩\₪\₫\€\₭\₮\₯\₰\₱\₲\₳\₴\₵\₶\₷\₸\₹\₺\₻\₼\₽\₾\₿\₽\﷼\￦]+'
    full_value = re.sub(currency_symbols_regex, "", value).replace("K", "e3").replace("Mio", "e6").replace("M", "e6")

    if '-' in value:
        full_lower, full_upper = full_value.split(" - ")
        lower, upper = value.split(" - ")
        return float(eval(full_lower)), float(eval(full_upper)), lower, upper
    else:
        full_value = float(eval(full_value))
        return full_value, full_value, value, value

def process_transfer_value_column(col):
    split_col = col.apply(lambda x: process_transfer_value(x)).apply(pd.Series)
    split_col.columns = ['Full Min Value', 'Full Max Value', 'Min Value', 'Max Value']
    return split_col

def process_wage(value):
    if value in ["n.a.", "N/A", "-"]:
        return 0

    # Regular expression to extract the numeric value
    regex = r'(\d[\d\s\.,]*)'
    match = re.search(regex, value)
    if not match:
        return 0

    numeric_value = match.group(1)
    numeric_value = re.sub(r'[^\d.]', '', numeric_value)
    return float(numeric_value)

def process_wage_column(col):
    return col.apply(process_wage)


def calculate_weakfoot_score(squad_df):
    def process_foot_rating(rating):
        if rating == "-":
            return (1, 20)
        else:
            return (foot_rating_conversion.get(rating, 0), foot_rating_conversion.get(rating, 0))

    # Apply the processing to both left and right foot ratings
    squad_df[['Left Foot_lower', 'Left Foot_upper']] = squad_df['Left Foot'].apply(
        lambda x: process_foot_rating(x)).apply(pd.Series)
    squad_df[['Right Foot_lower', 'Right Foot_upper']] = squad_df['Right Foot'].apply(
        lambda x: process_foot_rating(x)).apply(pd.Series)
    # Calculate the WeakFoot score as the minimum of left and right, for both lower and upper bounds
    squad_df['WeakFoot_lower'] = squad_df[['Left Foot_lower', 'Right Foot_lower']].min(axis=1)
    squad_df['WeakFoot_upper'] = squad_df[['Left Foot_upper', 'Right Foot_upper']].min(axis=1)

def process_file(file_path):
    print()
    print("Processing file: ", file_path)
    start_ts = pd.Timestamp.now()
    header_json_path = 'header.json'
    with open(header_json_path, 'r', encoding="utf-8") as f:
        custom_header = json.load(f)

    squad_rawdata_list = pd.read_html(file_path, header=None, encoding="utf-8", keep_default_na=False)

    squad_df = squad_rawdata_list[0]
    squad_df.columns = custom_header
    attribute_columns = set()
    for role_config in role_weightings.values():
        attribute_columns.update(role_config['attributes'].keys())

    # Skip the first 15 columns with regular string data
    for col in squad_df.columns[15:]:
        if col in attribute_columns:
            processed_cols = process_attribute_column(squad_df[col].astype(str))
            squad_df = pd.concat([squad_df, processed_cols], axis=1)
        
        if squad_df[col].dtype == 'object':
            if squad_df[col].str.contains('%').any():
                squad_df[col] = squad_df[col].str.rstrip(
                    '%').replace('-', '0').astype(float) / 100
            elif squad_df[col].str.contains('km').any():
                squad_df[col] = squad_df[col].str.rstrip(
                    'km').replace('-', '0').astype(float)
            else:
                squad_df[col] = pd.to_numeric(squad_df[col].replace(
                    '-', '0'), errors='coerce').fillna(0)
        else:
            # If not an object type, convert directly to numeric
            squad_df[col] = pd.to_numeric(
                squad_df[col], errors='coerce').fillna(0)


    squad_df[['Full Min Value', 'Full Max Value', 'Min Value', 'Max Value']] = process_transfer_value_column(squad_df['Transfer Value'])
    squad_df['Wage numerical'] = process_wage_column(squad_df['Wage'])
    
    calculate_weakfoot_score(squad_df)
    filtered_role_weightings = filter_role_weightings(squad_df, role_weightings)

    new_scores = {}
    for role, config in filtered_role_weightings.items():
        total_weighting = sum(config['attributes'].values())
        worst_case_scores, best_case_scores = calculate_score_range_with_malus(squad_df, config['attributes'], threshold=14)
        average_score = (worst_case_scores + best_case_scores) / 2
        worst_case_scores = normalize_and_round(worst_case_scores, total_weighting)
        best_case_scores = normalize_and_round(best_case_scores, total_weighting)
        average_score = normalize_and_round(average_score, total_weighting)
        combined_score = np.where(worst_case_scores == best_case_scores,
                          best_case_scores.astype(str),
                          worst_case_scores.astype(str) + " - " + best_case_scores.astype(str))

        new_scores[f'{role} (Score)'] = combined_score
        new_scores[f'{role} (Average Score)'] = average_score
        

    squad_df = pd.concat([squad_df, pd.DataFrame(new_scores)], axis=1)

    squad_df = calculate_stat_set_scores(squad_df, stat_sets, filtered_role_weightings)
    squad_df = calculate_role_scores_based_on_stats(squad_df, filtered_role_weightings)
    squad_df = calculate_combined_role_scores(squad_df, filtered_role_weightings)
    squad_df = calculate_performance(squad_df, filtered_role_weightings)

    role_score_range_columns = [f'{role} (Score)' for role in filtered_role_weightings.keys()]
    role_score_average_columns = [f'{role} (Average Score)' for role in filtered_role_weightings.keys()]
    stat_columns = [f'{set_name}' for set_name in stat_sets.keys()]
    role_stat_columns = [f'{role} (Stats)' for role in filtered_role_weightings.keys()]
    squad_df['Best Rating'] = squad_df[role_score_average_columns].max(axis=1)
    squad_df['Best Role'] = squad_df[role_score_average_columns].idxmax(axis=1)

    all_attributes = role_score_range_columns
    all_attributes.extend(role_score_average_columns)
    all_attributes.extend(['Starting 11', 'Average Rating'])
    all_attributes.extend(stat_columns)
    all_attributes.extend(role_stat_columns)

    columns_to_include = [
        'Name', 'Age', 'Club', 'Division', 'Full Min Value', 'Full Max Value', 'Min Value', 'Max Value', 'Wage', 'Wage numerical', 'Position',
        'Personality', 'Media-Style', 'Left Foot', 'Right Foot', 'Best Role',
        'Best Rating'
    ]
    columns_to_include.extend(all_attributes)
    
    columns_to_include.extend([f'{role} (Combined)' for role in filtered_role_weightings.keys()])
    columns_to_include.extend([f'{role} (Performance)' for role in filtered_role_weightings.keys()])

    # Add role-specific stat set columns
    for role in filtered_role_weightings.keys():
        for set_name in stat_sets.keys():
            if set_name in filtered_role_weightings[role].get('stats', {}):
                role_specific_column = f'{set_name} ({role})'
                if role_specific_column in squad_df.columns:
                    columns_to_include.append(role_specific_column)

    print(
        f"Processing time: {round((pd.Timestamp.now() - start_ts).total_seconds(), 2)} seconds")
    print("Data points: ", len(squad_df))
    return squad_df[columns_to_include], filtered_role_weightings


def get_relevant_columns(role, filtered_role_weightings):
    fixed_columns = [
        'Name', 'Club', 'Age', 'Min Value', 'Max Value', 'Wage', 'Starting 11', 'Average Rating', 'Best Role',
        'Best Rating', 'Division', 'Position', 'Personality', 'Media-Style', 'Left Foot', 'Right Foot'
    ]

    if role == "all":
        role_score_columns = [f'{r} (Score)' for r in filtered_role_weightings.keys()]
        role_stat_columns = [f'{r} (Stats)' for r in filtered_role_weightings.keys()]
        all_stat_set_columns = [set_name for set_name in stat_sets.keys()]
        role_combined_columns = [f'{role} (Combined)' for role in filtered_role_weightings.keys()]
        alternating_role_columns = [item for pair in zip(
            role_score_columns, role_stat_columns, role_combined_columns) for item in pair]

        return fixed_columns[:10] + alternating_role_columns + all_stat_set_columns + fixed_columns[10:]
    else:
        role_score_column = f'{role} (Score)'
        role_stat_score_column = f'{role} (Stats)'
        role_combined_column = f'{role} (Combined)'
        role_performance_column = f'{role} (Performance)'
        relevant_stat_sets = filtered_role_weightings[role].get('stats', {})
        role_specific_stat_set_columns = [
            f'{set_name} ({role})' for set_name in relevant_stat_sets]

        return fixed_columns[:8] + [role_score_column, role_stat_score_column, role_combined_column, role_performance_column] + role_specific_stat_set_columns + fixed_columns[8:]


def get_hidden_columns(role, filtered_role_weightings):
    columns = [f'{role} (Average Score)']
    if role == "all":
        columns = [f'{r} (Average Score)' for r in filtered_role_weightings.keys()]
    columns.extend(['Full Min Value', 'Full Max Value', 'Wage numerical'])
    return columns

def parse_positions(position_string):
    positions = position_string.split(', ')
    all_positions = []
    for position in positions:
        if '(' not in position:
            all_positions.append(position.strip())
            continue

        field_position, locations = re.match(
            r'([A-Z/]+) ?\(([A-Z]+)\)', position).groups()
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
        avg_per_club_per_role[role] = squad_data.groupby(
            'Club')[f'{role} (Average Score)'].mean().to_dict()
        max_per_club_per_role[role] = squad_data.groupby(
            'Club')[f'{role} (Average Score)'].max().to_dict()
    return avg_per_club_per_role, max_per_club_per_role


def compute_league_averages(processed_data_frame, filtered_dfs, roles):
    avg_per_league_per_role = {}
    max_per_league_per_role = {}
    unique_clubs = set()

    for role in roles:
        squad_data = filtered_dfs[role]
        avg_per_league_per_role[role] = squad_data.groupby(['Division', 'Club'])[
            f'{role} (Average Score)'].mean().groupby('Division').mean().to_dict()
        max_per_league_per_role[role] = squad_data.groupby(['Division', 'Club'])[
            f'{role} (Average Score)'].max().groupby('Division').mean().to_dict()
        unique_clubs.update(squad_data['Club'].unique())

    avg_per_club = {club: processed_data_frame[processed_data_frame['Club'] == club]['Best Rating'].mean()
                    for club in unique_clubs}

    avg_max_per_club = {club: processed_data_frame[processed_data_frame['Club'] == club]['Best Rating'].nlargest(11).mean()
                        for club in unique_clubs}
    
    return avg_per_league_per_role, max_per_league_per_role, avg_per_club, avg_max_per_club


def compute_overall_league_scores(processed_data_frame):
    avg_per_league = {}
    avg_of_max_per_club_per_role_per_league = {}

    for league in processed_data_frame['Division'].unique():
        league_data = processed_data_frame[processed_data_frame['Division'] == league]

        # Calculate the average 'Best Rating' for each club in the league
        club_averages = [league_data[league_data['Club'] == club]['Best Rating'].mean()
                         for club in league_data['Club'].unique()]

        # Calculate the average of the top 11 'Best Ratings' for each club in the league
        club_best_averages = [league_data[league_data['Club'] == club]['Best Rating'].nlargest(11).mean()
                              for club in league_data['Club'].unique()]

        # Average these values for the entire league
        avg_per_league[league] = pd.Series(club_averages).mean()
        avg_of_max_per_club_per_role_per_league[league] = pd.Series(club_best_averages).mean()

    return avg_per_league, avg_of_max_per_club_per_role_per_league

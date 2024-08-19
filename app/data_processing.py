import json
import re

import numpy as np
import pandas as pd

from configurations import foot_rating_conversion, role_mapping, role_weightings, column_mapping


def calculate_rating_range_with_malus(data, weightings, threshold=15, factor=0.01):
    ratings_lower = {}
    ratings_upper = {}
    for attribute_value, weight in weightings.items():
        lower_range = np.array(data[f'{attribute_value}_lower'])
        upper_range = np.array(data[f'{attribute_value}_upper'])
        adjusted_lower_malus = np.maximum(0, (threshold - lower_range)) * weight * factor
        adjusted_upper_malus = np.maximum(0, (threshold - upper_range)) * weight * factor

        ratings_lower[attribute_value + '_rating'] = np.maximum(-20, (lower_range - adjusted_lower_malus) * weight)
        ratings_upper[attribute_value + '_rating'] = np.maximum(-20, (upper_range - adjusted_upper_malus) * weight)

    total_rating_lower = sum(ratings_lower.values())
    total_rating_upper = sum(ratings_upper.values())

    return pd.Series(total_rating_lower), pd.Series(total_rating_upper)


def normalize_and_round(ratings, total_weighting):
    return np.round(ratings / total_weighting, 1)


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
    if value == "Not for Sale" or value == "Steht nicht zum Verkauf" or len(value) == 0:
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
        try:
            full_value = float(eval(full_value))
        except:
            print(f"Error converting value: {value}")
            raise
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


def calculate_weak_foot_rating(squad_df):
    def process_foot_rating(rating):
        if rating == "-":
            return 1, 20
        else:
            return foot_rating_conversion.get(rating, 0), foot_rating_conversion.get(rating, 0)

    # Apply the processing to both left and right foot ratings
    squad_df[['Left Foot_lower', 'Left Foot_upper']] = squad_df['Left Foot'].apply(
        lambda x: process_foot_rating(x)).apply(pd.Series)
    squad_df[['Right Foot_lower', 'Right Foot_upper']] = squad_df['Right Foot'].apply(
        lambda x: process_foot_rating(x)).apply(pd.Series)
    # Calculate the WeakFoot rating as the minimum of left and right, for both lower and upper bounds
    squad_df['WeakFoot_lower'] = squad_df[['Left Foot_lower', 'Right Foot_lower']].min(axis=1)
    squad_df['WeakFoot_upper'] = squad_df[['Left Foot_upper', 'Right Foot_upper']].min(axis=1)


def process_file(file_path):
    print(f"Processing file '{file_path}'")
    start_ts = pd.Timestamp.now()

    # Read the file to determine the mode based on column count
    df = pd.read_html(file_path, encoding="utf-8", keep_default_na=False)[0]

    if len(df.columns) == 60:
        print("Detected 'Versus' mode")
        mode = 'versus'
        header_json_path = '../data/header_vs.json'
        id_mapping_df = pd.read_csv('../data/id_name_mapping.csv')
        id_mapping_df['EID'] = id_mapping_df['EID'].astype(str)
    else:
        print("Detected regular mode")
        mode = 'regular'
        header_json_path = id_mapping_df = None
        df.columns = df.columns.str.upper()
        if "ABS.1" in df.columns:
            print("WARNING: Duplicate ABS column detected")
        new_column_mapping = {col: column_mapping.get(col, col) for col in df.columns}
        df.rename(columns=new_column_mapping, inplace=True)

    if header_json_path:
        with open(header_json_path, 'r', encoding="utf-8") as f:
            custom_header = json.load(f)
        df.columns = custom_header
    print(f"Reading file took: {round((pd.Timestamp.now() - start_ts).total_seconds(), 2)} seconds")

    if id_mapping_df is not None:
        df['EID'] = df['EID'].astype(str)
        df = pd.merge(df, id_mapping_df, on='EID', how='left')

    start_ts = pd.Timestamp.now()
    attribute_columns = set()
    for role_config in role_weightings.values():
        attribute_columns.update(role_config['attributes'].keys())

    for col in df.columns:
        if col in attribute_columns:
            processed_cols = process_attribute_column(df[col].astype(str))
            df = pd.concat([df, processed_cols], axis=1)

    df[['Full Min Value', 'Full Max Value', 'Min Value', 'Max Value']] = process_transfer_value_column(df['Transfer Value'])
    if mode != 'versus':
        df['Wage numerical'] = process_wage_column(df['Wage'])
    df['Position'] = df['Position'].apply(parse_positions)

    calculate_weak_foot_rating(df)
    filtered_role_weightings = filter_role_weightings(df, role_weightings)

    new_ratings = {}
    for role, config in filtered_role_weightings.items():
        total_weighting = sum(config['attributes'].values())
        worst_case_ratings, best_case_ratings = calculate_rating_range_with_malus(df, config['attributes'])
        average_rating = (worst_case_ratings + best_case_ratings) / 2
        worst_case_ratings = normalize_and_round(worst_case_ratings, total_weighting)
        best_case_ratings = normalize_and_round(best_case_ratings, total_weighting)
        average_rating = normalize_and_round(average_rating, total_weighting)
        combined_rating = np.where(worst_case_ratings == best_case_ratings,
                                   best_case_ratings.astype(str),
                                   worst_case_ratings.astype(str) + " - " + best_case_ratings.astype(str))

        new_ratings[f'{role} (Rating)'] = combined_rating
        new_ratings[f'{role} (Average Rating)'] = average_rating

    df = pd.concat([df, pd.DataFrame(new_ratings)], axis=1)

    print(f"Finished calculating ratings: {round((pd.Timestamp.now() - start_ts).total_seconds(), 2)} seconds")
    start_ts = pd.Timestamp.now()
    role_rating_range_columns = [f'{role} (Rating)' for role in filtered_role_weightings.keys()]
    role_rating_average_columns = [f'{role} (Average Rating)' for role in filtered_role_weightings.keys()]
    df['Best Rating'] = df[role_rating_average_columns].max(axis=1)
    df['Best Role'] = df[role_rating_average_columns].idxmax(axis=1)
    # remove 'Average Rating' part in Best Role
    df['Best Role'] = df['Best Role'].str.replace(' (Average Rating)', '')

    all_attributes = role_rating_range_columns
    all_attributes.extend(role_rating_average_columns)

    position_options = sorted(set(position for sublist in df['Position'] for position in sublist))
    role_rating_columns = [col for col in df.columns if col.endswith('(Rating)')]

    for col in role_rating_columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass

    calculate_value_per_cost(df)

    print(f"Preparing final structure: {round((pd.Timestamp.now() - start_ts).total_seconds(), 2)} seconds")
    print("Data points: ", len(df))
    return df, filtered_role_weightings, position_options, mode


def calculate_value_per_cost(df, base=2):
    role_rating_columns = [col for col in df.columns if col.endswith('(Rating)')]
    for col in role_rating_columns:
        # check if col contains float values
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            continue

        role = col.replace('(Rating)', '').strip()
        df[f'{role} Exp Rating'] = df[col].apply(lambda x: base ** x)
        df[f'{role} Recommendation'] = df[f'{role} Exp Rating'] * 10000 / df['Full Max Value']
        df[f'{role} Recommendation'] = df[f'{role} Recommendation'].replace([float('inf'), -float('inf')], float('nan')).fillna(0)
        df[f'{role} Recommendation'] = df[f'{role} Recommendation'].round(0).astype(int)
        df[f'{role} Exp Rating'] = df[f'{role} Exp Rating'].round(0).astype(int)
    return df


def get_relevant_columns(role, filtered_role_weightings, mode):
    priority_columns = ['Name', 'Club', 'Age', 'Position']
    other_columns = ['Max Value', 'Wage', 'Best Role', 'Best Rating', 'Personality', 'Media-Style', ]

    if mode == 'versus':
        priority_columns = ['Name', 'Full Max Value']
        other_columns = ["Consistency", "Big Matches", "Pressure", "Corners", "Crossing", 'Best Role', 'Best Rating', "CA", ]
    if role == "all":
        return priority_columns + other_columns
    else:
        role_rating_column = f'{role} (Rating)'
        # get all relevant attributes with a weight of at least 2.5
        relevant_attributes = [attr for attr, weight in filtered_role_weightings[role]['attributes'].items() if weight >= 50]
        return priority_columns + [f'{role} Recommendation'] + [role_rating_column] + other_columns + relevant_attributes


def get_hidden_columns(role, filtered_role_weightings, mode):
    columns = [f'{role} (Average Rating)']
    if role == "all":
        columns = [f'{r} (Average Rating)' for r in filtered_role_weightings.keys()]
    if mode != 'versus':
        columns.extend(['Full Min Value', 'Full Max Value'])
        columns.extend(['Wage numerical'])
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
    return data_frame['Position'].apply(lambda positions: bool(set(positions) & valid_positions))


def filter_by_role(data_frame, role):
    return data_frame[can_play_role(data_frame, role)]

column_mapping = {
    # GK
    'HB': 'Aerial Reach', 'STK': 'Command Of Area', 'KOM': 'Communication',
    'HAL': 'Handling', '1V1': 'One On Ones',
    'REF': 'Reflexes',
    # Technisch
    'FLA': 'Crossing', 'DRI': 'Dribbling', 'ABS': 'Finishing',
    'ANN': 'First Touch', 'KPF': 'Heading', 'WS': 'Long Shots',
    'DCK': 'Marking', 'PAS': 'Passing', 'TCK': 'Tackling',
    'TEC': 'Technique',
    # Mental
    'AGG': 'Aggression', 'AZP': 'Anticipation', 'MUT': 'Bravery',
    'NER': 'Composure', 'KON': 'Concentration', 'ENT': 'Decisions',
    'ZIE': 'Determination', 'FLR': 'Flair', 'OHN': 'Off The Ball',
    'STE': 'Positioning', 'TEA': 'Teamwork', 'ÜBS': 'Vision', 'ESF': 'Work Rate',
    # Physisch
    'ANT': 'Acceleration', 'BEW': 'Agility', 'BAL': 'Balance', 'SPR': 'Jumping Reach',
    'GFT': 'Natural Fitness', 'SCH': 'Pace', 'AUS': 'Stamina', 'KRA': 'Strength',
    # Other
    'ALTER': 'Age', 'LINKER FUSS': 'Left Foot', 'RECHTER FUSS': 'Right Foot',
    'PERSÖNLICHKEIT': 'Personality', 'MEDIENUMGANG': 'Media-Style', 'VEREIN': 'Club',
    'TRANSFERWERT': 'Transfer Value', 'GEHALT': 'Wage', 'POSITION': 'Position', 'NAME': 'Name',
    'NATION': 'Nat 1', "2. NATION": 'Nat 2', 'LIGA': 'Division'
}


role_mapping = {
    'GK': ['TW', 'GK'],
    'BPD': ['V(Z)', 'D(C)'],
    'LIB': ['V(Z)', 'D(C)'],
    'WBR': ['V(R)', 'FV(R)', 'D(R)', 'WB(R)'],
    'FBR': ['V(R)', 'FV(R)', 'D(R)', 'WB(R)'],
    'WBL': ['V(L)', 'FV(L)', 'D(L)', 'WB(L)'],
    'FBL': ['V(L)', 'FV(L)', 'D(L)', 'WB(L)'],
    '6er': ['DM'],
    '8er': ['DM', 'M(Z)', 'M(C)'],
    '10er': ['OM(Z)', 'AM(C)'],
    'IAS': ['ST(Z)', 'ST(C)', 'OM(R)', 'AM(R)', 'OM(L)', 'AM(L)'],
    'ST': ['ST(Z)', 'ST(C)'],
}

role_weightings = {
    'GK': {
        'attributes': {
            # Technisch
            'Aerial Reach': 100, 'Command Of Area': 40, 'Communication': 40,
            'First Touch': 5, 'Handling': 10,  'One On Ones': 80,
            'Passing': 5, 'Reflexes': 100, 'WeakFoot': 10,
            # Mental
            'Anticipation': 20, 'Bravery': 5, 'Composure': 30,
            'Concentration': 40, 'Decisions': 5, 'Determination': 5,
            'Positioning': 5, 'Vision': 5,
            # Physisch
            'Acceleration': 5, 'Agility': 100, 'Balance': 20,
            'Jumping Reach': 20, 'Natural Fitness': 0,
        }
    },
    'BPD': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 20, 'Finishing': 0,
            'First Touch': 25, 'Heading': 33, 'Long Shots': 0,
            'Marking': 33, 'Passing': 25, "Tackling": 33,
            'Technique': 0, 'WeakFoot': 10,
            # Mental
            'Aggression': 10, 'Anticipation': 10, 'Bravery': 33,
            'Composure': 33, 'Concentration': 40, 'Decisions': 10,
            'Determination': 10, 'Flair': 0, 'Off The Ball': 0,
            'Positioning': 25, 'Teamwork': 10, 'Vision': 10, 'Work Rate': 0,
            # Physisch
            'Acceleration': 100, 'Agility': 10, 'Balance': 25, 'Jumping Reach': 80,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 20, 'Strength': 40,
        }
    },
    'LIB': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 25, 'Finishing': 0,
            'First Touch': 33, 'Heading': 33, 'Long Shots': 10,
            'Marking': 25, 'Passing': 33, "Tackling": 33,
            'Technique': 10, 'WeakFoot': 20,
            # Mental
            'Aggression': 10, 'Anticipation': 20, 'Bravery': 33,
            'Composure': 40, 'Concentration': 40, 'Decisions': 20,
            'Determination': 10, 'Flair': 0, 'Off The Ball': 10,
            'Positioning': 25, 'Teamwork': 20, 'Vision': 20, 'Work Rate': 10,
            # Physisch
            'Acceleration': 100, 'Agility': 20, 'Balance': 33, 'Jumping Reach': 80,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 20, 'Strength': 40,
        }
    },
    'FB': {
        'attributes': {
            # Technisch
            'Crossing': 40, 'Dribbling': 33, 'Finishing': 0,
            'First Touch': 20, 'Heading': 10, 'Long Shots': 5,
            'Marking': 25, 'Passing': 20, "Tackling": 25,
            'Technique': 20, 'WeakFoot': 10,
            # Mental
            'Aggression': 10, 'Anticipation': 20, 'Bravery': 10,
            'Composure': 33, 'Concentration': 40, 'Decisions': 25,
            'Determination': 10, 'Flair': 0, 'Off The Ball': 25,
            'Positioning': 33, 'Teamwork': 20, 'Vision': 10, 'Work Rate': 25,
            # Physisch
            'Acceleration': 100, 'Agility': 33, 'Balance': 33, 'Jumping Reach': 50,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 33, 'Strength': 20,
        }
    },
    'WB': {
        'attributes': {
            # Technisch
            'Crossing': 50, 'Dribbling': 40, 'Finishing': 10,
            'First Touch': 15, 'Heading': 10, 'Long Shots': 10,
            'Marking': 20, 'Passing': 20, "Tackling": 20,
            'Technique': 20, 'WeakFoot': 15,
            # Mental
            'Aggression': 10, 'Anticipation': 25, 'Bravery': 5,
            'Composure': 25, 'Concentration': 33, 'Decisions': 33,
            'Determination': 20, 'Flair': 0, 'Off The Ball': 33,
            'Positioning': 20, 'Teamwork': 20, 'Vision': 20, 'Work Rate': 40,
            # Physisch
            'Acceleration': 100, 'Agility': 33, 'Balance': 33, 'Jumping Reach': 33,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 40, 'Strength': 15,
        }
    },
    '6er': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 25, 'Finishing': 5,
            'First Touch': 33, 'Heading': 10, 'Long Shots': 20,
            'Marking': 33, 'Passing': 33, "Tackling": 33,
            'Technique': 10, 'WeakFoot': 20,
            # Mental
            'Aggression': 20, 'Anticipation': 25, 'Bravery': 20,
            'Composure': 33, 'Concentration': 50, 'Decisions': 33,
            'Determination': 20, 'Flair': 10, 'Off The Ball': 25,
            'Positioning': 33, 'Teamwork': 33, 'Vision': 25, 'Work Rate': 25,
            # Physisch
            'Acceleration': 100, 'Agility': 30, 'Balance': 40, 'Jumping Reach': 60,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 25, 'Strength': 25,
        }
    },
    '8er': {
        'attributes': {
            # Technisch
            'Crossing': 10, 'Dribbling': 40, 'Finishing': 25,
            'First Touch': 25, 'Heading': 10, 'Long Shots': 25,
            'Marking': 10, 'Passing': 25, "Tackling": 20,
            'Technique': 20, 'WeakFoot': 25,
            # Mental
            'Aggression': 20, 'Anticipation': 40, 'Bravery': 10,
            'Composure': 25, 'Concentration': 40, 'Decisions': 50,
            'Determination': 20, 'Flair': 10, 'Off The Ball': 40,
            'Positioning': 20, 'Teamwork': 25, 'Vision': 50, 'Work Rate': 40,
            # Physisch
            'Acceleration': 100, 'Agility': 40, 'Balance': 40, 'Jumping Reach': 50,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 33, 'Strength': 20,
        }
    },
    '10er': {
        'attributes': {
            # Technisch
            'Crossing': 10, 'Dribbling': 33, 'Finishing': 25,
            'First Touch': 25, 'Heading': 10, 'Long Shots': 20,
            'Marking': 0, 'Passing': 20, "Tackling": 0,
            'Technique': 20, 'WeakFoot': 20,
            # Mental
            'Aggression': 0, 'Anticipation': 33, 'Bravery': 0,
            'Composure': 25, 'Concentration': 33, 'Decisions': 50,
            'Determination': 10, 'Flair': 25, 'Off The Ball': 25,
            'Positioning': 0, 'Teamwork': 20, 'Vision': 40, 'Work Rate': 20,
            # Physisch
            'Acceleration': 100, 'Agility': 40, 'Balance': 33, 'Jumping Reach': 33,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 20, 'Strength': 5,
        }
    },
    'IAS': {
        'attributes': {
            # Technisch
            'Crossing': 25, 'Dribbling': 40, 'Finishing': 25,
            'First Touch': 15, 'Heading': 25, 'Long Shots': 10,
            'Marking': 0, 'Passing': 10, "Tackling": 0,
            'Technique': 15, 'WeakFoot': 25,
            # Mental
            'Aggression': 0, 'Anticipation': 25, 'Bravery': 10,
            'Composure': 33, 'Concentration': 20, 'Decisions': 20,
            'Determination': 10, 'Flair': 10, 'Off The Ball': 33,
            'Positioning': 0, 'Teamwork': 10, 'Vision': 10, 'Work Rate': 25,
            # Physisch
            'Acceleration': 100, 'Agility': 25, 'Balance': 25, 'Jumping Reach': 50,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 25, 'Strength': 10,
        }
    },
    'ST': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 33, 'Finishing': 33,
            'First Touch': 25, 'Heading': 33, 'Long Shots': 5,
            'Marking': 0, 'Passing': 5, "Tackling": 0,
            'Technique': 10, 'WeakFoot': 25,
            # Mental
            'Aggression': 0, 'Anticipation': 25, 'Bravery': 10,
            'Composure': 33, 'Concentration': 20, 'Decisions': 20,
            'Determination': 10, 'Flair': 10, 'Off The Ball': 25,
            'Positioning': 0, 'Teamwork': 10, 'Vision': 10, 'Work Rate': 25,
            # Physisch
            'Acceleration': 100, 'Agility': 25, 'Balance': 25, 'Jumping Reach': 70,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 25, 'Strength': 20,
        }
    },
}

roles_where_left_or_right_matters = ["WB", "W", "IW", "WT", "FB"]
new_role_weightings = {}

for key, value in role_weightings.items():
    if key in roles_where_left_or_right_matters:
        left_key = key + "L"
        right_key = key + "R"
        new_role_weightings[left_key] = value
        new_role_weightings[right_key] = value
    else:
        new_role_weightings[key] = value

role_weightings = new_role_weightings
foot_rating_conversion = {
    "Sehr stark": 20, "Stark": 16, "Gut": 12, "Passabel": 8, "Schwach": 4, "Sehr schwach": 0,
    "Very Strong": 20, "Strong": 16, "Fairly Strong": 12, "Reasonable": 8, "Weak": 4, "Very Weak": 0,
}

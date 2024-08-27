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

role_weightings = {
    'GK': {
        'attributes': {
            # Technisch
            'Aerial Reach': 100, 'Command Of Area': 40, 'Communication': 40,
            'First Touch': 5, 'Handling': 10,  'One On Ones': 80,
            'Passing': 5, 'Reflexes': 100, 'WeakFoot': 10,
            # Mental
            'Anticipation': 20, 'Bravery': 5, 'Composure': 30,
            'Concentration': 50, 'Decisions': 5, 'Determination': 10,
            'Positioning': 5, 'Vision': 5,
            # Physisch
            'Acceleration': 5, 'Agility': 100, 'Balance': 20,
            'Jumping Reach': 20, 'Natural Fitness': 0,
        }
    },
    'BPD': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 33, 'Finishing': 0,
            'First Touch': 20, 'Heading': 25, 'Long Shots': 0,
            'Marking': 20, 'Passing': 5, "Tackling": 20,
            'Technique': 0, 'WeakFoot': 10,
            # Mental
            'Aggression': 20, 'Anticipation': 20, 'Bravery': 20,
            'Composure': 20, 'Concentration': 40, 'Decisions': 5,
            'Determination': 10, 'Flair': 0, 'Off The Ball': 0,
            'Positioning': 15, 'Teamwork': 5, 'Vision': 5, 'Work Rate': 0,
            # Physisch
            'Acceleration': 120, 'Agility': 10, 'Balance': 33, 'Jumping Reach': 100,
            'Natural Fitness': 0, 'Pace': 120, 'Stamina': 20, 'Strength': 40,
        }
    },
    'LIB': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 33, 'Finishing': 0,
            'First Touch': 25, 'Heading': 25, 'Long Shots': 0,
            'Marking': 20, 'Passing': 10, "Tackling": 20,
            'Technique': 5, 'WeakFoot': 10,
            # Mental
            'Aggression': 20, 'Anticipation': 25, 'Bravery': 20,
            'Composure': 25, 'Concentration': 40, 'Decisions': 10,
            'Determination': 10, 'Flair': 0, 'Off The Ball': 5,
            'Positioning': 15, 'Teamwork': 10, 'Vision': 10, 'Work Rate': 10,
            # Physisch
            'Acceleration': 120, 'Agility': 20, 'Balance': 33, 'Jumping Reach': 100,
            'Natural Fitness': 0, 'Pace': 120, 'Stamina': 20, 'Strength': 40,
        }
    },
    'FB': {
        'attributes': {
            # Technisch
            'Crossing': 20, 'Dribbling': 33, 'Finishing': 0,
            'First Touch': 10, 'Heading': 0, 'Long Shots': 0,
            'Marking': 15, 'Passing': 5, "Tackling": 20,
            'Technique': 5, 'WeakFoot': 10,
            # Mental
            'Aggression': 20, 'Anticipation': 25, 'Bravery': 10,
            'Composure': 10, 'Concentration': 40, 'Decisions': 5,
            'Determination': 20, 'Flair': 0, 'Off The Ball': 5,
            'Positioning': 15, 'Teamwork': 10, 'Vision': 5, 'Work Rate': 25,
            # Physisch
            'Acceleration': 140, 'Agility': 20, 'Balance': 33, 'Jumping Reach': 40,
            'Natural Fitness': 0, 'Pace': 140, 'Stamina': 25, 'Strength': 10,
        }
    },
    'WB': {
        'attributes': {
            # Technisch
            'Crossing': 20, 'Dribbling': 40, 'Finishing': 10,
            'First Touch': 10, 'Heading': 0, 'Long Shots': 5,
            'Marking': 0, 'Passing': 5, "Tackling": 20,
            'Technique': 10, 'WeakFoot': 20,
            # Mental
            'Aggression': 25, 'Anticipation': 25, 'Bravery': 0,
            'Composure': 10, 'Concentration': 33, 'Decisions': 10,
            'Determination': 20, 'Flair': 0, 'Off The Ball': 10,
            'Positioning': 5, 'Teamwork': 10, 'Vision': 10, 'Work Rate': 33,
            # Physisch
            'Acceleration': 150, 'Agility': 40, 'Balance': 40, 'Jumping Reach': 33,
            'Natural Fitness': 0, 'Pace': 150, 'Stamina': 33, 'Strength': 10,
        }
    },
    '6er': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 25, 'Finishing': 5,
            'First Touch': 25, 'Heading': 0, 'Long Shots': 15,
            'Marking': 15, 'Passing': 15, "Tackling": 15,
            'Technique': 10, 'WeakFoot': 20,
            # Mental
            'Aggression': 33, 'Anticipation': 33, 'Bravery': 10,
            'Composure': 25, 'Concentration': 40, 'Decisions': 10,
            'Determination': 20, 'Flair': 0, 'Off The Ball': 10,
            'Positioning': 20, 'Teamwork': 20, 'Vision': 15, 'Work Rate': 25,
            # Physisch
            'Acceleration': 100, 'Agility': 33, 'Balance': 40, 'Jumping Reach': 60,
            'Natural Fitness': 0, 'Pace': 100, 'Stamina': 20, 'Strength': 20,
        }
    },
    '8er': {
        'attributes': {
            # Technisch
            'Crossing': 5, 'Dribbling': 33, 'Finishing': 25,
            'First Touch': 25, 'Heading': 5, 'Long Shots': 25,
            'Marking': 10, 'Passing': 20, "Tackling": 20,
            'Technique': 20, 'WeakFoot': 25,
            # Mental
            'Aggression': 25, 'Anticipation': 40, 'Bravery': 5,
            'Composure': 25, 'Concentration': 40, 'Decisions': 25,
            'Determination': 25, 'Flair': 20, 'Off The Ball': 20,
            'Positioning': 10, 'Teamwork': 20, 'Vision': 25, 'Work Rate': 33,
            # Physisch
            'Acceleration': 110, 'Agility': 40, 'Balance': 40, 'Jumping Reach': 33,
            'Natural Fitness': 0, 'Pace': 110, 'Stamina': 33, 'Strength': 10,
        }
    },
    '10er': {
        'attributes': {
            # Technisch
            'Crossing': 5, 'Dribbling': 33, 'Finishing': 25,
            'First Touch': 25, 'Heading': 5, 'Long Shots': 25,
            'Marking': 10, 'Passing': 25, "Tackling": 20,
            'Technique': 25, 'WeakFoot': 33,
            # Mental
            'Aggression': 25, 'Anticipation': 40, 'Bravery': 5,
            'Composure': 25, 'Concentration': 40, 'Decisions': 25,
            'Determination': 25, 'Flair': 33, 'Off The Ball': 33,
            'Positioning': 5, 'Teamwork': 20, 'Vision': 33, 'Work Rate': 33,
            # Physisch
            'Acceleration': 110, 'Agility': 40, 'Balance': 33, 'Jumping Reach': 20,
            'Natural Fitness': 0, 'Pace': 110, 'Stamina': 33, 'Strength': 5,
        }
    },
    'IAS': {
        'attributes': {
            # Technisch
            'Crossing': 15, 'Dribbling': 40, 'Finishing': 25,
            'First Touch': 20, 'Heading': 20, 'Long Shots': 10,
            'Marking': 0, 'Passing': 10, "Tackling": 0,
            'Technique': 15, 'WeakFoot': 25,
            # Mental
            'Aggression': 10, 'Anticipation': 40, 'Bravery': 5,
            'Composure': 33, 'Concentration': 33, 'Decisions': 10,
            'Determination': 20, 'Flair': 20, 'Off The Ball': 25,
            'Positioning': 0, 'Teamwork': 5, 'Vision': 10, 'Work Rate': 20,
            # Physisch
            'Acceleration': 150, 'Agility': 40, 'Balance': 25, 'Jumping Reach': 75,
            'Natural Fitness': 0, 'Pace': 150, 'Stamina': 25, 'Strength': 5,
        }
    },
    'ST': {
        'attributes': {
            # Technisch
            'Crossing': 0, 'Dribbling': 33, 'Finishing': 25,
            'First Touch': 20, 'Heading': 25, 'Long Shots': 10,
            'Marking': 0, 'Passing': 5, "Tackling": 5,
            'Technique': 10, 'WeakFoot': 25,
            # Mental
            'Aggression': 10, 'Anticipation': 33, 'Bravery': 5,
            'Composure': 33, 'Concentration': 33, 'Decisions': 10,
            'Determination': 20, 'Flair': 15, 'Off The Ball': 25,
            'Positioning': 0, 'Teamwork': 5, 'Vision': 5, 'Work Rate': 20,
            # Physisch
            'Acceleration': 150, 'Agility': 25, 'Balance': 25, 'Jumping Reach': 100,
            'Natural Fitness': 0, 'Pace': 150, 'Stamina': 20, 'Strength': 20,
        }
    },
}

foot_rating_conversion = {
    "Sehr stark": 20, "Stark": 16, "Gut": 12, "Passabel": 8, "Schwach": 4, "Sehr schwach": 0,
    "Very Strong": 20, "Strong": 16, "Fairly Strong": 12, "Reasonable": 8, "Weak": 4, "Very Weak": 0,
}

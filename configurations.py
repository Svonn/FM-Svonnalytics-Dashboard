stat_sets = {
    'Goalkeeping':
    {
        'Expected Goals Prevented per 90 minutes': 3,
        'Save Ratio': 2,
        'Expected Save Percentage': 2,
        'Penalties Saved Ratio': 1,
    },
    'Defensive Play': {
        'Possession Won per 90 minutes': 8,
        'Key Tackles per 90 minutes': 5,
        'Interceptions per 90 minutes': 5,
        'Clearances per 90 minutes': 4,
        'Blocks per 90 minutes': 4,
        'Tackle completion ratio': 3,
        'Tackles per 90 minutes': 2,
        'Team Goals Conceded per 90 minutes': 2,
        'Pressures completed per 90 minutes': 1,
    },
    'Aerial Ability': {
        'Key Headers per 90 minutes': 8,
        'Headers Won per 90 minutes': 6,
        'Aerial Challenges attempted per 90 minutes': 1
    },
    'Build-up Play': {
        'Progressive Passes per 90 minutes': 8,
        'Passes completed per 90 minutes': 5,
        'Possession Lost per 90 minutes': 5,
        'Open Play Key Passes per 90 minutes': 3,
        'Key Passes per 90 minutes': 3,
        'Passes attempted per 90 minutes': 1
    },
    'Wing Play': {
        'Crosses completed per 90 minutes': 8,
        'Dribbles Made per 90 minutes': 1,
        'Crosses attempted per 90 minutes': 1,
    },
    'Creation': {
        'Expected Assists per 90 minutes': 2,
        'Chances Created per 90 minutes': 2,
        'Assists per 90 minutes': 1,
        'Open Play Key Passes per 90 minutes': 1,
    },
    'Presence': {
        'Pressures completed per 90 minutes': 1,
        'Distance Covered per 90 minutes': 1,
        'Pressures attempted per 90 minutes': 1,
    },
    'Goal Scoring': {
        'Goals per 90 minutes': 8,
        'Expected Goals Overperformance': 7,
        'Conversion Rate (%)': 6,
        'Shots On Target per 90 minutes': 1,
        'Shots per 90 minutes': 0.5,
    },
    'Pressing': {
        'Possession Won per 90 minutes': 3,
        'Pressures completed per 90 minutes': 3,
        'Distance Covered per 90 minutes': 2,
        'Interceptions per 90 minutes': 2,
        'Pressures attempted per 90 minutes': 2,
    }
}


role_mapping = {
    'GK': ['TW', 'GK'],
    'CD': ['V(Z)', 'D(C)'],
    'WBR': ['V(R)', 'FV(R)', 'D(R)', 'WB(R)'],
    'IWBR': ['V(R)', 'D(R)'],
    'WBL': ['V(L)', 'FV(L)', 'D(L)', 'WB(L)'],
    'IWBL': ['V(L)', 'D(L)'],
    'DM/BeM': ['DM', 'M(Z)', 'M(C)'],
    'MC': ['M(Z)', 'M(C)'],
    'SV/B2B': ['DM', 'M(Z)', 'M(C)'],
    'PM': ['DM', 'M(Z)', 'OM(Z)', 'M(C)', 'AM(C)'],
    'AM': ['M(Z)', 'OM(Z)', 'M(C)', 'AM(C)'],
    'WR': ['M(R)', 'OM(R)', 'AM(R)'],
    'WL': ['M(L)', 'OM(L)', 'AM(L)'],
    'IWR': ['M(R)', 'OM(R)', 'AM(R)'],
    'IWL': ['M(L)', 'OM(L)', 'AM(L)'],
    'ST': ['ST(Z)', 'ST(C)']
}

role_weightings = {
    'GK': {
        'attributes': {
            # Technisch
            'Reflexes': 3, 'Aerial Reach': 2, 'Command Of Area': 2, 'Communication': 2, 'Handling': 2, 'One On Ones': 2, 'Passing': 1, 'Throwing': 1,
            # Mental
            'Anticipation': 2, 'Composure': 2, 'Concentration': 2, 'Decisions': 2, 'Positioning': 1, 'Vision': 1, 'Determination': 1,
            # Physisch
            'Agility': 3, 'Jumping Reach': 1, 'Balance': 1, 'Acceleration': 1,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Goalkeeping': 3,
            'Build-up Play': 1
        }
    },
    'CD': {
        'attributes': {
            # Technisch
            'Tackling': 2, 'Marking': 2, 'Dribbling': 2, 'Heading': 2, 'Passing': 1, 'First Touch': 1, 
            # Mental
            'Anticipation': 3, 'Bravery': 3, 'Composure': 3, 'Concentration': 2, 'Positioning': 2, 'Decisions': 1, 'Determination': 1,
            # Physisch
            'Pace': 6, 'Jumping Reach': 6, 'Acceleration': 6, 'Strength': 3, 'Agility': 3, 'Balance': 3,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Defensive Play': 10,
            'Aerial Ability': 4,
            'Build-up Play': 2,
        }
    },
    'WB': {
        'attributes': {
            # Technisch
            'Dribbling': 6, 'Crossing': 3,  'Passing': 1, 'First Touch': 1, 'Tackling': 1, 'Marking': 0.5,
            # Mental
            'Work Rate': 3, 'Decisions': 2, 'Off The Ball': 2, 'Anticipation': 1, 'Composure': 1, 'Concentration': 1, 'Positioning': 1, 'Teamwork': 1, 'Aggression': 1,  'Determination': 1,
            # Physisch
            'Pace': 6, 'Acceleration': 6, 'Jumping Reach': 3, 'Agility': 3, 'Balance': 3, 'Stamina': 2,  'Strength': 2, 
        },
        'stats': {
            'Wing Play': 8,
            'Defensive Play': 4,
            'Presence': 6,
            'Build-up Play': 3,
            'Pressing': 1,
        }
    },
    'IWB': {
        'attributes': {
            # Technisch
            'Passing': 2, 'First Touch': 2, 'Marking': 1, 'Tackling': 1, 'Technique': 0.5,
            # Mental
            'Decisions': 2,  'Composure': 2, 'Positioning': 2, 'Work Rate': 2, 'Aggression': 2, 'Off The Ball': 2, 'Anticipation': 2, 'Concentration': 2, 'Teamwork': 1,  'Determination': 1,
            # Physisch
            'Acceleration': 4, "Pace": 4,'Jumping Reach': 2, 'Strength': 2, 'Agility': 2, 'Balance': 2,  'Stamina': 1,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Build-up Play': 8,
            'Defensive Play': 6,
            'Presence': 1,
            'Pressing': 1,
            'Wing Play': 1,
        }
    },
    'DM/BeM': {
        'attributes': {
            # Technisch
            'Tackling': 2, 'First Touch': 2, 'Marking': 1, 'Passing': 1, 
            # Mental
            'Work Rate': 3, 'Aggression': 3, 'Composure': 2, 'Positioning': 2, 'Anticipation': 2, 'Bravery': 2, 'Concentration': 2, 'Teamwork': 1,  'Decisions': 1,  'Off The Ball': 1, 'Determination': 1,
            # Physisch
             'Acceleration': 4, "Pace": 4,'Jumping Reach': 4, 'Strength': 3, 'Agility': 2, 'Balance': 2,  'Stamina': 1,
        },
        'stats': {
            'Defensive Play': 5,
            'Build-up Play': 5,
            'Pressing': 2,
        }
    },
    'SV/B2B': {
        'attributes': {
            # Technisch
            'Dribbling': 4, 'First Touch': 3, 'Long Shots': 1,  'Technique': 1, 'Finishing': 1, 'Tackling': 1, 'Marking': 1, 'Passing': 1,
            # Mental
            'Off The Ball': 3, 'Work Rate': 3, 'Vision': 2, 'Decisions': 2, 'Anticipation': 1, 'Composure': 1, 'Concentration': 1, 'Teamwork': 1, 'Positioning': 1, 'Concentration': 1, 'Determination': 1,
            # Physisch
            'Pace': 6, 'Acceleration': 6, 'Jumping Reach': 3, 'Stamina': 2, 'Balance': 2, 'Agility': 2,
        },
        'stats': {
            'Build-up Play': 8,
            'Creation': 5,
            'Presence': 5,
            'Goal Scoring': 2,
            'Defensive Play': 2,
            'Pressing': 1,
        }
    },
    'MC': {
        'attributes': {
            # Technisch
            'Dribbling': 2, 'First Touch': 2, 'Tackling': 1,  'Passing': 1, 'Marking': 0.5, 'Technique': 0.5,
            # Mental
            'Off The Ball': 2, 'Work Rate': 2, 'Vision': 1, 'Decisions': 1, 'Anticipation': 0.5, 'Composure': 1, 'Concentration': 1, 'Teamwork': 0.5, 'Positioning': 1, 'Concentration': 1, 'Determination': 1,
            # Physisch
            'Pace': 2, 'Acceleration': 2, 'Jumping Reach': 1, 'Stamina': 1, 'Balance': 1, 'Agility': 1,
        },
        'stats': {
            'Build-up Play': 6,
            'Creation': 4,
            'Presence': 4,
            'Defensive Play': 4,
            'Goal Scoring': 2,
            'Pressing': 2,
        }
    },
    'PM': {
        'attributes': {
            # Technisch
            'Passing': 2, 'First Touch': 2, 'Dribbling': 2, 'Technique': 1, 'Finishing': 0.5, 'Long Shots': 0.5,
            # Mental
            'Vision': 3, 'Off The Ball': 3,  'Decisions': 3, 'Anticipation': 2, 'Composure': 2, 'Concentration': 2, 'Determination': 1,
            # Physisch
            'Pace': 4, 'Acceleration': 4, 'Jumping Reach': 2, 'Stamina': 2, 'Balance': 3, 'Agility': 3,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Build-up Play': 8,
            'Creation': 8,
            'Goal Scoring': 3,
            'Presence': 2,
            'Pressing': 1,
        }
    },
    'AM': {
        'attributes': {
            # Technisch
            'Dribbling': 3, 'First Touch': 2, 'Passing': 1, 'Technique': 1, 'Finishing': 1, 'Long Shots': 1, 
            # Mental
            'Off The Ball': 2, 'Vision': 1, 'Decisions': 1, 'Anticipation': 1, 'Composure': 1, 'Concentration': 1, 'Determination': 1,
            # Physisch
            'Pace': 5, 'Acceleration': 5, 'Jumping Reach': 2, 'Stamina': 2, 'Balance': 3, 'Agility': 3,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Creation': 8,
            'Build-up Play': 8,
            'Goal Scoring': 6,
            'Presence': 4,
            'Pressing': 1,
        }
    },
    'W': {
        'attributes': {
            # Technisch
            'Dribbling': 5, 'Crossing': 2, 'Passing': 1, 'Technique': 1, 'Finishing': 1, 'Long Shots': 1, 'First Touch': 2,
            # Mental
            'Off The Ball': 3, 'Work Rate': 3, 'Anticipation': 1, 'Composure': 1, 'Concentration': 1, 'Decisions': 1, 'Vision': 1, 'Determination': 1,
            # Physisch
            'Pace': 8, 'Acceleration': 8, 'Jumping Reach': 3, 'Stamina': 2, 'Balance': 4, 'Agility': 4,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Wing Play': 8,
            'Creation': 7,
            'Presence': 4,
            'Goal Scoring': 3,
            'Pressing': 1,
        }
    },
    'IW': {
        'attributes': {
            # Technisch
            'Dribbling': 5, 'Crossing': 1, 'Passing': 1, 'Technique': 1, 'Finishing': 2, 'Long Shots': 2, 'First Touch': 2,
            # Mental
            'Off The Ball': 3, 'Work Rate': 3, 'Anticipation': 1, 'Composure': 2, 'Concentration': 1, 'Decisions': 1, 'Vision': 1, 'Determination': 1,
            # Physisch
            'Pace': 8, 'Acceleration': 8, 'Jumping Reach': 3, 'Stamina': 2, 'Balance': 4, 'Agility': 4,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Creation': 8,
            'Goal Scoring': 8,
            'Wing Play': 4,
            'Presence': 4,
            'Pressing': 1,
        }
    },
    'ST': {
        'attributes': {
            # Technisch
            'Dribbling': 5, 'Finishing': 2,  'Heading': 2,
            # Mental
            'Off The Ball': 3, 'Anticipation': 3, 'Composure': 2, 'Concentration': 1, 'Decisions': 1, 'Determination': 1,
            # Physisch
            'Pace': 8, 'Acceleration': 8, 'Jumping Reach': 6, 'Stamina': 2, 'Balance': 4, 'Agility': 4,
            # WeakFoot
            'WeakFoot': 0.2
        },
        'stats': {
            'Goal Scoring': 10,
            'Creation': 4,
            'Pressing': 1,
            'Build-up Play': 1,
        }
    },
}

roles_where_left_or_right_matters = ["WB", "W", "IWB", "IW"]
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

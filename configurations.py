stat_groups = {
    'GoalScoring': ['Sch/90', 'Chancenverwertung (%)', 'SaT/90', 'xG/Sch (%)', 'xG/90', 'xG-ohn11/90', 'xG-OP', 'Tor/90'],
    'Assisting': ['xA/90', 'Vorl/90', 'Ch/90'],
    'Opening': ['Ps V/90', 'Pr Pässe/90', 'Ps A/90', 'E Pä/90', 'EntP(S)/90', 'Ballverl/90', 'Drb/90'],
    'Wingplay': ['Vers Fla/90', 'Ang Fla/90', 'Lauf/90'],
    'Pressing': ['PrsV/90', 'PrsErf'],
    'Defense': ['Ballgew/90', 'AbB/90', 'Klär/90', 'Ent Zwk/90', 'Zwk %', 'Tck/90', 'Blk/90', 'TGgt/90'],
    'Aerial': ['Kop V/90', 'Kopf G/90', 'Ent Kopf/90'],
    'Goalkeeper': ['Parierte Elfmeter (%)', 'xSv %', 'Par %', 'xG verh/90']
}

role_mapping = {
    'gk': ['TW'],
    'cd': ['V(Z)'],
    'wbr': ['V(R)','FV(R)'],
    'iwbr': ['V(R)'],
    'wbl': ['V(L)','FV(L)'],
    'iwbl': ['V(L)'],
    'dm': ['DM'],
    'sv': ['DM'],
    'pm': ['DM', 'M(Z)', 'OM(Z)'],
    'am': ['M(Z)', 'OM(Z)'],
    'wr': ['M(R)', 'OM(R)'],
    'wl': ['M(L)','OM(L)'],
    'iwr': ['M(R)', 'OM(R)'],
    'iwl': ['M(L)', 'OM(L)'],
    'st': ['ST(Z)']
}

role_attributes = {
    'gk': {
        'attributes': {
            # Technisch
            'Ref': 3, 'HB': 2, 'StK': 2, 'Kom': 2, 'Hal': 2, '1v1': 2, 'Pas': 1, 'Abw': 1, 
            # Mental
            'Azp': 2,'Ner': 2,'Kon': 2, 'Ent': 2, 'Ste': 1, 'Übs': 1,
            # Physisch
            'Bew': 3, 'Spr': 1, 'Bal': 1, 'Ant': 1, 
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['Goalkeeper']
    },
    'cd': {
        'attributes': {
            # Technisch
            'Tck': 3,'Dck': 3,'Kpf': 1, 'Pas': 1, 'Ann': 1,
            # Mental
            'Azp': 2, 'Mut': 2, 'Ner': 2,'Kon': 2, 'Ste': 2, 'Ent': 1, 
            # Physisch
            'Sch': 4,'Spr': 4,'Ant': 4,'Kra': 3, 'Bew': 2, 'Bal': 2,
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['Defense', 'Aerial']
    },
    'wb': {
        'attributes': {
            # Technisch
            'Fla': 3, 'Dri': 3, 'Pas': 2, 'Ann': 2, 'Tck': 1, 'Dck': 0.5, 
            # Mental
            'Ent': 3, 'Esf': 3, 'Azp': 1, 'Ner': 1, 'Kon': 1, 'Ste': 1, 'Tea': 1, 'Agg': 1, 'Ohn': 1,
            # Physisch
            'Sch': 4, 'Ant': 4, 'Bew': 1, 'Aus': 2, 'Kra': 1, 'Bal': 1,   
        },
        'stats': ['Defense', 'Assisting', 'Wingplay', 'Opening', 'Pressing']
    },
    'iwb': {
        'attributes': {
            # Technisch
            'Pas': 4, 'Ann': 4, 'Dck': 2, 'Tck': 2, 'Tec': 1, 
            # Mental
            'Tea': 4, 'Ent': 4,  'Ner': 3, 'Ste': 2, 'Esf': 2, 'Agg': 2, 'Ohn': 2, 'Azp': 2, 'Kon': 1, 
            # Physisch
            'Spr': 1, 'Kra': 1, 'Ant': 2, "Sch": 2, 'Aus': 1, 
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['Defense', 'Assisting', 'Opening', 'Pressing']
    },
    'dm': {
        'attributes': {
            # Technisch
            'Tck': 2, 'Pas': 2, 'Ann': 2, 'Dck': 2,
            # Mental
            'Esf': 3, 'Agg': 4, 'Tea': 2, 'Ste': 2, 'Azp': 2, 'Mut': 2, 'Kon': 2, 'Ent': 1, 'Ner': 1, 'Ohn': 1,
            # Physisch
            'Spr': 2, 'Kra': 2, 'Aus': 1, 'Ant': 1, "Sch": 1,
        },
        'stats': ['Defense', 'Opening', 'Aerial', 'Pressing']
    },
    'sv': {
        'attributes': {
            # Technisch
            'Pas': 2, 'Dri': 2, 'WS': 2, 'Ann': 2, 'Tec': 1, 'Abs': 1, 
            # Mental
             'Ohn': 4, 'Esf': 3, 'Übs': 2, 'Ent': 3, 'Azp': 1, 'Ner': 1, 'Kon': 1, 
            # Physisch
             'Sch': 4, 'Ant': 4, 'Bal': 2, 'Bew': 2, 
        },
        'stats': ['Opening', 'Assisting', 'GoalScoring']
    },
    'pm': {
        'attributes': {
            # Technisch
            'Pas': 5, 'Ann': 4, 'Dri': 1, 'Tec': 3, 'Abs': 1, 'WS': 1, 
            # Mental
            'Übs': 5, 'Ohn': 4,  'Ent': 4, 'Azp': 1, 'Ner': 1, 'Kon': 1, 
            # Physisch
            'Bal': 2, 'Bew': 2, 'Sch': 1, 'Ant': 1, 
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['Opening', 'Assisting']
    },
    'am': {
        'attributes': {
            # Technisch
            'Pas': 2, 'Dri': 2, 'Tec': 2, 'Abs': 2, 'WS': 2, 'Ann': 2,
            # Mental
             'Ohn': 3, 'Übs': 2, 'Ent': 2, 'Azp': 1, 'Ner': 1, 'Kon': 1, 
            # Physisch
             'Sch': 3, 'Ant': 3, 'Bal': 2, 'Bew': 2, 
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['GoalScoring', 'Assisting', 'Opening', 'Pressing']
    },
    'w': {
        'attributes': {
            # Technisch
            'Dri': 3, 'Fla': 3, 'Pas': 2, 'Tec': 2, 'Abs': 1, 'WS': 1, 'Ann': 1,
            # Mental
            'Ohn': 3, 'Esf': 2, 'Azp': 1, 'Ner': 1, 'Kon': 1, 'Ent': 1,'Übs': 1, 
            # Physisch
            'Sch': 4, 'Ant': 4, 'Bew': 2, 'Bal': 2,
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['GoalScoring', 'Assisting', 'Wingplay', 'Opening', 'Pressing']
    },
    'iw': {
        'attributes': {
            # Technisch
            'Dri': 3, 'Pas': 2, 'Tec': 2,  'Abs': 2, 'WS': 2, 'Ann': 1, 'Fla': 1,
            # Mental
            'Ohn': 3, 'Esf': 2, 'Azp': 1, 'Ner': 1, 'Kon': 1, 'Ent': 1,'Übs': 1, 
            # Physisch
            'Sch': 4, 'Ant': 4, 'Bew': 2, 'Bal': 2,
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['GoalScoring', 'Assisting', 'Wingplay', 'Opening', 'Pressing']
    },
    'st': {
        'attributes': {
            # Technisch
            'Abs': 3, 'Dri': 1, 'Kpf': 2, 'Pas': 1, 'Tec': 1, 
            # Mental
            'Ohn': 3,'Azp': 3, 'Ner': 2, 'Kon': 1, 'Ent': 1,
            # Physisch
            'Ant': 6, 'Sch': 6, 'Spr': 4, 'Bew': 2, 'Bal': 4, 'Kra': 2,
            # WeakFoot
            'WeakFoot': 1
        },
        'stats': ['GoalScoring', 'Aerial', 'Pressing']
    },
}

role_attributes["wbl"] = role_attributes["wb"]
role_attributes["wbr"] = role_attributes["wb"]
role_attributes["wl"] = role_attributes["w"]
role_attributes["wr"] = role_attributes["w"]
role_attributes["iwbr"] = role_attributes["iwb"]
role_attributes["iwbl"] = role_attributes["iwb"]
role_attributes["iwl"] = role_attributes["iw"]
role_attributes["iwr"] = role_attributes["iw"]




foot_rating_conversion = {
    "Sehr stark": 20, "Stark": 16, "Gut": 12, "Passabel": 8, "Schwach": 4, "Sehr schwach": 0
}

"""Monster/Creature database."""

MONSTERS = {
    # Starter monsters
    "flarion": {
        "name": "Flarion",
        "types": ["fire"],
        "base_stats": {"hp": 45, "attack": 60, "defense": 40, "speed": 70, "special": 50},
        "moves_learned": ["scratch", "growl", "ember", "quick_attack", "flame_wheel", "fire_fang", "flamethrower", "fire_blast"],
        "evolution": {"at_level": 16, "into": "pyrethon"},
        "description": "A small flame creature that thrives in warm climates.",
    },
    "pyrethon": {
        "name": "Pyrethon",
        "types": ["fire"],
        "base_stats": {"hp": 60, "attack": 80, "defense": 55, "speed": 90, "special": 70},
        "moves_learned": ["ember", "quick_attack", "flame_wheel", "fire_fang", "flamethrower", "inferno", "fire_blast", "blast_burn"],
        "evolution": {"at_level": 36, "into": "infernoth"},
        "description": "Its body temperature can melt stone.",
    },
    "infernoth": {
        "name": "Infernoth",
        "types": ["fire", "fighting"],
        "base_stats": {"hp": 80, "attack": 110, "defense": 75, "speed": 100, "special": 90},
        "moves_learned": ["flame_wheel", "fire_fang", "flamethrower", "inferno", "fire_blast", "blast_burn", "close_combat", "flare_blitz"],
        "evolution": None,
        "description": "Legends say it can incinerate mountains with a roar.",
    },

    "aquan": {
        "name": "Aquan",
        "types": ["water"],
        "base_stats": {"hp": 50, "attack": 45, "defense": 60, "speed": 45, "special": 55},
        "moves_learned": ["tackle", "tail_whip", "water_gun", "bubble", "bite", "water_pulse", "aqua_tail", "hydro_pump"],
        "evolution": {"at_level": 16, "into": "marinaqua"},
        "description": "It stores water in its body to survive on land.",
    },
    "marinaqua": {
        "name": "Marinaqua",
        "types": ["water"],
        "base_stats": {"hp": 70, "attack": 60, "defense": 80, "speed": 65, "special": 75},
        "moves_learned": ["water_gun", "bubble", "bite", "water_pulse", "aqua_tail", "hydro_pump", "surf", "ice_beam"],
        "evolution": {"at_level": 36, "into": "leviathan"},
        "description": "Its powerful tail can create tidal waves.",
    },
    "leviathan": {
        "name": "Leviathan",
        "types": ["water", "dragon"],
        "base_stats": {"hp": 95, "attack": 85, "defense": 100, "speed": 80, "special": 105},
        "moves_learned": ["water_pulse", "aqua_tail", "hydro_pump", "surf", "ice_beam", "dragon_pulse", "hydro_cannon", "draco_meteor"],
        "evolution": None,
        "description": "Ancient sailors feared its destructive power.",
    },

    "leaflet": {
        "name": "Leaflet",
        "types": ["grass"],
        "base_stats": {"hp": 45, "attack": 50, "defense": 55, "speed": 60, "special": 65},
        "moves_learned": ["tackle", "growl", "vine_whip", "absorb", "razor_leaf", "sleep_powder", "energy_ball", "solar_beam"],
        "evolution": {"at_level": 16, "into": "chloros"},
        "description": "Its leaves can sense changes in weather.",
    },
    "chloros": {
        "name": "Chloros",
        "types": ["grass"],
        "base_stats": {"hp": 65, "attack": 70, "defense": 75, "speed": 80, "special": 85},
        "moves_learned": ["vine_whip", "absorb", "razor_leaf", "sleep_powder", "energy_ball", "solar_beam", "petal_dance", "synthesis"],
        "evolution": {"at_level": 36, "into": "verdanos"},
        "description": "It can regenerate any wound using sunlight.",
    },
    "verdanos": {
        "name": "Verdanos",
        "types": ["grass", "fairy"],
        "base_stats": {"hp": 80, "attack": 85, "defense": 90, "speed": 95, "special": 110},
        "moves_learned": ["razor_leaf", "sleep_powder", "energy_ball", "solar_beam", "petal_dance", "synthesis", "moonblast", "frenzy_plant"],
        "evolution": None,
        "description": "Forests bloom wherever it walks.",
    },

    # Common monsters
    "ratling": {
        "name": "Ratling",
        "types": ["normal"],
        "base_stats": {"hp": 30, "attack": 56, "defense": 35, "speed": 72, "special": 25},
        "moves_learned": ["tackle", "tail_whip", "quick_attack", "bite", "hyper_fang", "crunch", "double_edge"],
        "evolution": {"at_level": 20, "into": "ratclaw"},
        "description": "Common in cities, it scavenges for food.",
    },
    "ratclaw": {
        "name": "Ratclaw",
        "types": ["normal", "dark"],
        "base_stats": {"hp": 55, "attack": 91, "defense": 60, "speed": 107, "special": 50},
        "moves_learned": ["quick_attack", "bite", "hyper_fang", "crunch", "night_slash", "double_edge", "sucker_punch"],
        "evolution": None,
        "description": "Its claws can cut through steel.",
    },

    "buzzling": {
        "name": "Buzzling",
        "types": ["bug", "flying"],
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "speed": 55, "special": 35},
        "moves_learned": ["tackle", "string_shot", "bug_bite", "gust", "air_cutter", "bug_buzz", "hurricane"],
        "evolution": {"at_level": 15, "into": "flutterwing"},
        "description": "Its wings beat so fast they blur.",
    },
    "flutterwing": {
        "name": "Flutterwing",
        "types": ["bug", "flying"],
        "base_stats": {"hp": 70, "attack": 65, "defense": 60, "speed": 95, "special": 80},
        "moves_learned": ["bug_bite", "gust", "air_cutter", "bug_buzz", "hurricane", "quiver_dance", "psychic"],
        "evolution": None,
        "description": "Its scales have a hypnotic effect.",
    },

    "pebblet": {
        "name": "Pebblet",
        "types": ["rock"],
        "base_stats": {"hp": 40, "attack": 65, "defense": 95, "speed": 20, "special": 30},
        "moves_learned": ["tackle", "harden", "rock_throw", "rollout", "rock_slide", "stone_edge", "earthquake", "head_smash"],
        "evolution": {"at_level": 25, "into": "bouldron"},
        "description": "It remains motionless for years at a time.",
    },
    "bouldron": {
        "name": "Bouldron",
        "types": ["rock", "ground"],
        "base_stats": {"hp": 80, "attack": 110, "defense": 130, "speed": 45, "special": 55},
        "moves_learned": ["rock_throw", "rollout", "rock_slide", "stone_edge", "earthquake", "head_smash", "heavy_slam", "stealth_rock"],
        "evolution": None,
        "description": "Mountains tremble when it moves.",
    },

    "zaprat": {
        "name": "Zaprat",
        "types": ["electric"],
        "base_stats": {"hp": 35, "attack": 55, "defense": 40, "speed": 90, "special": 65},
        "moves_learned": ["tackle", "tail_whip", "thunder_shock", "quick_attack", "spark", "thunder_fang", "thunderbolt", "thunder"],
        "evolution": {"at_level": 26, "into": "voltiger"},
        "description": "Electricity crackles in its fur constantly.",
    },
    "voltiger": {
        "name": "Voltiger",
        "types": ["electric"],
        "base_stats": {"hp": 65, "attack": 85, "defense": 60, "speed": 120, "special": 95},
        "moves_learned": ["spark", "thunder_fang", "thunderbolt", "thunder", "wild_charge", "volt_switch", "ion_deluge"],
        "evolution": None,
        "description": "It can generate 100,000 volts of electricity.",
    },

    "spookling": {
        "name": "Spookling",
        "types": ["ghost"],
        "base_stats": {"hp": 30, "attack": 35, "defense": 30, "speed": 80, "special": 100},
        "moves_learned": ["lick", "hypnosis", "night_shade", "confuse_ray", "shadow_ball", "dark_pulse", "dream_eater"],
        "evolution": {"at_level": 25, "into": "phantasm"},
        "description": "It feeds on the fears of the living.",
    },
    "phantasm": {
        "name": "Phantasm",
        "types": ["ghost", "dark"],
        "base_stats": {"hp": 60, "attack": 65, "defense": 60, "speed": 110, "special": 130},
        "moves_learned": ["night_shade", "confuse_ray", "shadow_ball", "dark_pulse", "dream_eater", "hex", "shadow_force"],
        "evolution": None,
        "description": "It can drag souls into the void.",
    },

    "drakelet": {
        "name": "Drakelet",
        "types": ["dragon"],
        "base_stats": {"hp": 50, "attack": 70, "defense": 45, "speed": 60, "special": 60},
        "moves_learned": ["scratch", "leer", "dragon_rage", "bite", "dragon_breath", "dragon_claw", "dragon_pulse", "outrage"],
        "evolution": {"at_level": 30, "into": "drakona"},
        "description": "A rare creature sought by collectors.",
    },
    "drakona": {
        "name": "Drakona",
        "types": ["dragon"],
        "base_stats": {"hp": 80, "attack": 120, "defense": 75, "speed": 100, "special": 90},
        "moves_learned": ["dragon_breath", "dragon_claw", "dragon_pulse", "outrage", "draco_meteor", "dragon_dance", "iron_tail"],
        "evolution": {"at_level": 55, "into": "dragoloth"},
        "description": "Its roar can be heard for miles.",
    },
    "dragoloth": {
        "name": "Dragoloth",
        "types": ["dragon", "flying"],
        "base_stats": {"hp": 95, "attack": 145, "defense": 90, "speed": 120, "special": 120},
        "moves_learned": ["dragon_pulse", "outrage", "draco_meteor", "dragon_dance", "hurricane", "fire_blast", "extreme_speed"],
        "evolution": None,
        "description": "Ancient texts speak of its world-ending power.",
    },

    # Legendary
    "lunaris": {
        "name": "Lunaris",
        "types": ["psychic", "dark"],
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "speed": 100, "special": 150},
        "moves_learned": ["psyshock", "dark_pulse", "moonblast", "psychic", "night_daze", "future_sight", "lunar_dance"],
        "evolution": None,
        "description": "The moon incarnate. Its power waxes and wanes.",
    },
    "solaris": {
        "name": "Solaris",
        "types": ["fire", "psychic"],
        "base_stats": {"hp": 100, "attack": 120, "defense": 100, "speed": 120, "special": 150},
        "moves_learned": ["flamethrower", "psychic", "solar_beam", "blue_fire", "morning_sun", "stored_power", "solar_charge"],
        "evolution": None,
        "description": "The sun incarnate. Its light never fades.",
    },
}

def get_monster_data(monster_id):
    """Get monster data by ID."""
    return MONSTERS.get(monster_id, None)

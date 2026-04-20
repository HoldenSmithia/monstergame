"""Move database."""

MOVES = {
    # Normal moves
    "tackle": {"name": "Tackle", "type": "normal", "power": 40, "accuracy": 100, "category": "physical", "pp": 35, "description": "A physical attack in which the user charges, full body, into the target."},
    "scratch": {"name": "Scratch", "type": "normal", "power": 40, "accuracy": 100, "category": "physical", "pp": 35, "description": "Hard, pointed, sharp claws rake the target to inflict damage."},
    "quick_attack": {"name": "Quick Attack", "type": "normal", "power": 40, "accuracy": 100, "category": "physical", "pp": 30, "priority": 1, "description": "The user lunges at the target at a speed that makes it almost invisible. This move always goes first."},
    "bite": {"name": "Bite", "type": "dark", "power": 60, "accuracy": 100, "category": "physical", "pp": 25, "effect": "flinch_30", "description": "The target is bitten with viciously sharp fangs. This may also make the target flinch."},
    "crunch": {"name": "Crunch", "type": "dark", "power": 80, "accuracy": 100, "category": "physical", "pp": 15, "effect": "lower_defense_20", "description": "The user crunches up the target with sharp fangs. This may also lower the target's Defense stat."},
    "hyper_fang": {"name": "Hyper Fang", "type": "normal", "power": 80, "accuracy": 90, "category": "physical", "pp": 15, "description": "The user bites hard on the target with its sharp front fangs. This may also make the target flinch."},
    "double_edge": {"name": "Double-Edge", "type": "normal", "power": 120, "accuracy": 100, "category": "physical", "pp": 15, "recoil": 0.33, "description": "A reckless, life-risking tackle in which the user rushes the target. This also damages the user quite a lot."},
    "extreme_speed": {"name": "Extreme Speed", "type": "normal", "power": 80, "accuracy": 100, "category": "physical", "pp": 5, "priority": 2, "description": "The user charges the target at blinding speed. This move always goes first."},
    "giga_impact": {"name": "Giga Impact", "type": "normal", "power": 150, "accuracy": 90, "category": "physical", "pp": 5, "recharge": True, "description": "The user charges at the target using every bit of its power. The user can't move on the next turn."},

    # Status moves
    "growl": {"name": "Growl", "type": "normal", "power": 0, "accuracy": 100, "category": "status", "pp": 40, "effect": "lower_attack", "description": "The user growls in an endearing way, making opposing monsters less wary. This lowers their Attack stats."},
    "tail_whip": {"name": "Tail Whip", "type": "normal", "power": 0, "accuracy": 100, "category": "status", "pp": 30, "effect": "lower_defense", "description": "The user wags its tail cutely, making opposing monsters less wary and lowering their Defense stats."},
    "leer": {"name": "Leer", "type": "normal", "power": 0, "accuracy": 100, "category": "status", "pp": 30, "effect": "lower_defense", "description": "The user gives opposing monsters an intimidating leer that lowers their Defense stats."},
    "harden": {"name": "Harden", "type": "normal", "power": 0, "accuracy": None, "category": "status", "pp": 30, "effect": "raise_defense", "description": "The user stiffens all the muscles in its body to raise its Defense stat."},
    "string_shot": {"name": "String Shot", "type": "bug", "power": 0, "accuracy": 95, "category": "status", "pp": 40, "effect": "lower_speed", "description": "The user binds the target with thin silk. This silk reduces the target's Speed stat."},

    # Fire moves
    "ember": {"name": "Ember", "type": "fire", "power": 40, "accuracy": 100, "category": "special", "pp": 25, "description": "The target is attacked with small flames. This may also leave the target with a burn."},
    "flame_wheel": {"name": "Flame Wheel", "type": "fire", "power": 60, "accuracy": 100, "category": "physical", "pp": 25, "description": "The user cloaks itself in fire and charges at the target. This may also leave the target with a burn."},
    "fire_fang": {"name": "Fire Fang", "type": "fire", "power": 65, "accuracy": 95, "category": "physical", "pp": 15, "description": "The user bites with flame-cloaked fangs. This may also make the target flinch or leave it with a burn."},
    "flamethrower": {"name": "Flamethrower", "type": "fire", "power": 90, "accuracy": 100, "category": "special", "pp": 15, "description": "The target is scorched with an intense blast of fire. This may also leave the target with a burn."},
    "fire_blast": {"name": "Fire Blast", "type": "fire", "power": 110, "accuracy": 85, "category": "special", "pp": 5, "description": "The target is attacked with an intense blast of all-consuming fire. This may also leave the target with a burn."},
    "inferno": {"name": "Inferno", "type": "fire", "power": 100, "accuracy": 50, "category": "special", "pp": 5, "effect": "burn", "description": "The user attacks by engulfing the target in an intense fire. This leaves the target with a burn."},
    "blast_burn": {"name": "Blast Burn", "type": "fire", "power": 150, "accuracy": 90, "category": "special", "pp": 5, "recharge": True, "description": "The target is razed by a fiery explosion. The user can't move on the next turn."},
    "flare_blitz": {"name": "Flare Blitz", "type": "fire", "power": 120, "accuracy": 100, "category": "physical", "pp": 15, "recoil": 0.33, "description": "The user attacks by shrouding itself in fire and charging at the target. This also damages the user and may burn the target."},
    "blue_fire": {"name": "Blue Fire", "type": "fire", "power": 130, "accuracy": 85, "category": "special", "pp": 5, "description": "The user attacks with the sacred blue flames of the sun."},

    # Water moves
    "water_gun": {"name": "Water Gun", "type": "water", "power": 40, "accuracy": 100, "category": "special", "pp": 25, "description": "The target is blasted with a forceful shot of water."},
    "bubble": {"name": "Bubble", "type": "water", "power": 40, "accuracy": 100, "category": "special", "pp": 30, "description": "A spray of countless bubbles is jetted at the opposing monsters. This may also lower their Speed stats."},
    "water_pulse": {"name": "Water Pulse", "type": "water", "power": 60, "accuracy": 100, "category": "special", "pp": 20, "description": "The user attacks the target with a pulsing blast of water. This may also confuse the target."},
    "aqua_tail": {"name": "Aqua Tail", "type": "water", "power": 90, "accuracy": 90, "category": "physical", "pp": 10, "description": "The user attacks by swinging its tail as if it were a vicious wave in a raging storm."},
    "hydro_pump": {"name": "Hydro Pump", "type": "water", "power": 110, "accuracy": 80, "category": "special", "pp": 5, "description": "The target is blasted by a huge volume of water launched under great pressure."},
    "surf": {"name": "Surf", "type": "water", "power": 90, "accuracy": 100, "category": "special", "pp": 15, "description": "The user attacks everything around it by swamping its surroundings with a giant wave."},
    "hydro_cannon": {"name": "Hydro Cannon", "type": "water", "power": 150, "accuracy": 90, "category": "special", "pp": 5, "recharge": True, "description": "The target is hit with a watery blast. The user can't move on the next turn."},

    # Grass moves
    "vine_whip": {"name": "Vine Whip", "type": "grass", "power": 45, "accuracy": 100, "category": "physical", "pp": 25, "description": "The target is struck with slender, whiplike vines to inflict damage."},
    "absorb": {"name": "Absorb", "type": "grass", "power": 20, "accuracy": 100, "category": "special", "pp": 25, "drain": 0.5, "description": "A nutrient-draining attack. The user's HP is restored by half the damage taken by the target."},
    "razor_leaf": {"name": "Razor Leaf", "type": "grass", "power": 55, "accuracy": 95, "category": "physical", "pp": 25, "high_crit": True, "description": "Sharp-edged leaves are launched to slash at opposing monsters. Critical hits land more easily."},
    "sleep_powder": {"name": "Sleep Powder", "type": "grass", "power": 0, "accuracy": 75, "category": "status", "pp": 15, "effect": "sleep", "description": "The user scatters a cloud of soporific powder that puts the target to sleep."},
    "energy_ball": {"name": "Energy Ball", "type": "grass", "power": 90, "accuracy": 100, "category": "special", "pp": 10, "description": "The user draws power from nature and fires it at the target. This may also lower the target's Sp. Def."},
    "solar_beam": {"name": "Solar Beam", "type": "grass", "power": 120, "accuracy": 100, "category": "special", "pp": 10, "charge": True, "description": "In this two-turn attack, the user gathers light, then blasts a bundled beam on the next turn."},
    "petal_dance": {"name": "Petal Dance", "type": "grass", "power": 120, "accuracy": 100, "category": "special", "pp": 10, "locked": True, "description": "The user attacks the target by scattering petals for two to three turns. The user then becomes confused."},
    "synthesis": {"name": "Synthesis", "type": "grass", "power": 0, "accuracy": None, "category": "status", "pp": 5, "heal": 0.5, "description": "The user restores its own HP. The amount of HP regained varies with the weather."},
    "frenzy_plant": {"name": "Frenzy Plant", "type": "grass", "power": 150, "accuracy": 90, "category": "special", "pp": 5, "recharge": True, "description": "The user slams the target with an enormous tree. The user can't move on the next turn."},

    # Electric moves
    "thunder_shock": {"name": "Thunder Shock", "type": "electric", "power": 40, "accuracy": 100, "category": "special", "pp": 30, "description": "A jolt of electricity crashes down on the target to inflict damage. This may also leave the target with paralysis."},
    "spark": {"name": "Spark", "type": "electric", "power": 65, "accuracy": 100, "category": "physical", "pp": 20, "description": "The user throws an electrically charged tackle at the target. This may also leave the target with paralysis."},
    "thunder_fang": {"name": "Thunder Fang", "type": "electric", "power": 65, "accuracy": 95, "category": "physical", "pp": 15, "description": "The user bites with electrified fangs. This may also make the target flinch or leave it with paralysis."},
    "thunderbolt": {"name": "Thunderbolt", "type": "electric", "power": 90, "accuracy": 100, "category": "special", "pp": 15, "description": "A strong electric blast crashes down on the target. This may also leave the target with paralysis."},
    "thunder": {"name": "Thunder", "type": "electric", "power": 110, "accuracy": 70, "category": "special", "pp": 10, "description": "A wicked thunderbolt is dropped on the target to inflict damage. This may also leave the target with paralysis."},
    "wild_charge": {"name": "Wild Charge", "type": "electric", "power": 90, "accuracy": 100, "category": "physical", "pp": 15, "recoil": 0.25, "description": "The user shrouds itself in electricity and smashes into the target. This also damages the user."},
    "volt_switch": {"name": "Volt Switch", "type": "electric", "power": 70, "accuracy": 100, "category": "special", "pp": 20, "description": "After making its attack, the user rushes back to switch places with a party monster in waiting."},

    # Ice moves
    "ice_beam": {"name": "Ice Beam", "type": "ice", "power": 90, "accuracy": 100, "category": "special", "pp": 10, "description": "The target is struck with an icy-cold beam of energy. This may also leave the target frozen."},
    "blizzard": {"name": "Blizzard", "type": "ice", "power": 110, "accuracy": 70, "category": "special", "pp": 5, "description": "A howling blizzard is summoned to strike opposing monsters. This may also leave the opposing monsters frozen."},

    # Fighting moves
    "close_combat": {"name": "Close Combat", "type": "fighting", "power": 120, "accuracy": 100, "category": "physical", "pp": 5, "effect": "lower_own_defenses", "description": "The user fights the target up close without guarding itself. This also lowers the user's Defense and Sp. Def."},
    "mach_punch": {"name": "Mach Punch", "type": "fighting", "power": 40, "accuracy": 100, "category": "physical", "pp": 30, "priority": 1, "description": "The user throws a punch at blinding speed. This move always goes first."},

    # Poison moves
    "poison_sting": {"name": "Poison Sting", "type": "poison", "power": 15, "accuracy": 100, "category": "physical", "pp": 35, "description": "The user stabs the target with a poisonous stinger. This may also poison the target."},
    "sludge_bomb": {"name": "Sludge Bomb", "type": "poison", "power": 90, "accuracy": 100, "category": "special", "pp": 10, "description": "Unsanitary sludge is hurled at the target. This may also poison the target."},

    # Ground moves
    "sand_attack": {"name": "Sand Attack", "type": "ground", "power": 0, "accuracy": 100, "category": "status", "pp": 15, "effect": "lower_accuracy", "description": "Sand is hurled in the target's face, reducing the target's accuracy."},
    "earthquake": {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "category": "physical", "pp": 10, "description": "The user sets off an earthquake that strikes every monster around it."},

    # Flying moves
    "gust": {"name": "Gust", "type": "flying", "power": 40, "accuracy": 100, "category": "special", "pp": 35, "description": "A gust of wind is whipped up by wings and launched at the target to inflict damage."},
    "air_cutter": {"name": "Air Cutter", "type": "flying", "power": 60, "accuracy": 95, "category": "special", "pp": 25, "high_crit": True, "description": "The user launches razor-like wind to slash the opposing monsters. Critical hits land more easily."},
    "hurricane": {"name": "Hurricane", "type": "flying", "power": 110, "accuracy": 70, "category": "special", "pp": 10, "description": "The user attacks by wrapping its opponent in a fierce wind. This may also confuse the target."},

    # Psychic moves
    "confusion": {"name": "Confusion", "type": "psychic", "power": 50, "accuracy": 100, "category": "special", "pp": 25, "description": "The target is hit by a weak telekinetic force. This may also confuse the target."},
    "psychic": {"name": "Psychic", "type": "psychic", "power": 90, "accuracy": 100, "category": "special", "pp": 10, "description": "The target is hit by a strong telekinetic force. This may also lower the target's Sp. Def stat."},
    "psyshock": {"name": "Psyshock", "type": "psychic", "power": 80, "accuracy": 100, "category": "special", "pp": 10, "description": "The user materializes an odd psychic wave to attack the target. This attack does physical damage."},
    "dream_eater": {"name": "Dream Eater", "type": "psychic", "power": 100, "accuracy": 100, "category": "special", "pp": 15, "drain": 0.5, "description": "The user eats the dreams of a sleeping target. The user's HP is restored by half the damage taken."},
    "future_sight": {"name": "Future Sight", "type": "psychic", "power": 120, "accuracy": 100, "category": "special", "pp": 10, "delay": True, "description": "Two turns after this move is used, a hunk of psychic energy attacks the target."},

    # Bug moves
    "bug_bite": {"name": "Bug Bite", "type": "bug", "power": 60, "accuracy": 100, "category": "physical", "pp": 20, "description": "The user bites the target. If the target is holding a Berry, the user eats it and gains its effect."},
    "bug_buzz": {"name": "Bug Buzz", "type": "bug", "power": 90, "accuracy": 100, "category": "special", "pp": 10, "description": "The user generates a damaging sound wave by vibration. This may also lower the target's Sp. Def stat."},
    "quiver_dance": {"name": "Quiver Dance", "type": "bug", "power": 0, "accuracy": None, "category": "status", "pp": 20, "effect": "boost_special", "description": "The user lightly performs a beautiful, mystic dance. This boosts the user's Sp. Atk, Sp. Def, and Speed stats."},

    # Rock moves
    "rock_throw": {"name": "Rock Throw", "type": "rock", "power": 50, "accuracy": 90, "category": "physical", "pp": 15, "description": "The user picks up and throws a small rock at the target to inflict damage."},
    "rollout": {"name": "Rollout", "type": "rock", "power": 30, "accuracy": 90, "category": "physical", "pp": 20, "description": "The user continually rolls into the target over five turns. It becomes more powerful each time it hits."},
    "rock_slide": {"name": "Rock Slide", "type": "rock", "power": 75, "accuracy": 90, "category": "physical", "pp": 10, "description": "Large boulders are hurled at the opposing monsters to inflict damage. This may also make the targets flinch."},
    "stone_edge": {"name": "Stone Edge", "type": "rock", "power": 100, "accuracy": 80, "category": "physical", "pp": 5, "high_crit": True, "description": "The user stabs the target from below with sharpened stones. Critical hits land more easily."},
    "head_smash": {"name": "Head Smash", "type": "rock", "power": 150, "accuracy": 80, "category": "physical", "pp": 5, "recoil": 0.5, "description": "The user attacks the target with a hazardous, full-power headbutt. This also damages the user terribly."},
    "stealth_rock": {"name": "Stealth Rock", "type": "rock", "power": 0, "accuracy": None, "category": "status", "pp": 20, "hazard": True, "description": "The user lays a trap of levitating stones around the opposing team. The stones hurt opposing monsters that switch in."},

    # Ghost moves
    "lick": {"name": "Lick", "type": "ghost", "power": 30, "accuracy": 100, "category": "physical", "pp": 30, "description": "The target is licked with a long tongue, causing damage. This may also leave the target with paralysis."},
    "night_shade": {"name": "Night Shade", "type": "ghost", "power": 0, "accuracy": 100, "category": "special", "pp": 15, "level_damage": True, "description": "The user makes the target see a frightening mirage. It inflicts damage equal to the user's level."},
    "shadow_ball": {"name": "Shadow Ball", "type": "ghost", "power": 80, "accuracy": 100, "category": "special", "pp": 15, "description": "The user hurls a shadowy blob at the target. This may also lower the target's Sp. Def stat."},
    "hex": {"name": "Hex", "type": "ghost", "power": 65, "accuracy": 100, "category": "special", "pp": 10, "description": "This relentless attack does massive damage to a target affected by status conditions."},
    "shadow_force": {"name": "Shadow Force", "type": "ghost", "power": 120, "accuracy": 100, "category": "physical", "pp": 5, "description": "The user disappears, then strikes the target on the next turn. This move hits even if the target protects itself."},

    # Dragon moves
    "dragon_rage": {"name": "Dragon Rage", "type": "dragon", "power": 0, "accuracy": 100, "category": "special", "pp": 10, "fixed_damage": 40, "description": "This attack hits the target with a shock wave of pure rage. This attack always inflicts 40 HP damage."},
    "dragon_breath": {"name": "Dragon Breath", "type": "dragon", "power": 60, "accuracy": 100, "category": "special", "pp": 20, "description": "The user exhales a mighty gust that inflicts damage. This may also leave the target with paralysis."},
    "dragon_claw": {"name": "Dragon Claw", "type": "dragon", "power": 80, "accuracy": 100, "category": "physical", "pp": 15, "description": "The user slashes the target with huge, sharp claws."},
    "dragon_pulse": {"name": "Dragon Pulse", "type": "dragon", "power": 85, "accuracy": 100, "category": "special", "pp": 10, "description": "The user opens its mouth and shoots out a ball of energy at the target."},
    "outrage": {"name": "Outrage", "type": "dragon", "power": 120, "accuracy": 100, "category": "physical", "pp": 10, "locked": True, "description": "The user rampages and attacks for two to three turns. The user then becomes confused."},
    "draco_meteor": {"name": "Draco Meteor", "type": "dragon", "power": 130, "accuracy": 90, "category": "special", "pp": 5, "effect": "lower_own_special", "description": "Comets are summoned down from the sky onto the target. The attack's recoil harshly lowers the user's Sp. Atk stat."},
    "dragon_dance": {"name": "Dragon Dance", "type": "dragon", "power": 0, "accuracy": None, "category": "status", "pp": 20, "effect": "boost_physical", "description": "The user vigorously performs a mystic, powerful dance that boosts its Attack and Speed stats."},

    # Dark moves
    "night_slash": {"name": "Night Slash", "type": "dark", "power": 70, "accuracy": 100, "category": "physical", "pp": 15, "high_crit": True, "description": "The user slashes the target the instant an opportunity arises. Critical hits land more easily."},
    "dark_pulse": {"name": "Dark Pulse", "type": "dark", "power": 80, "accuracy": 100, "category": "special", "pp": 15, "description": "The user releases a horrible aura imbued with dark thoughts. This may also make the target flinch."},
    "night_daze": {"name": "Night Daze", "type": "dark", "power": 85, "accuracy": 95, "category": "special", "pp": 10, "description": "The user lets loose a pitch-black shock wave at its target. This may also lower the target's accuracy."},
    "sucker_punch": {"name": "Sucker Punch", "type": "dark", "power": 70, "accuracy": 100, "category": "physical", "pp": 5, "priority": 1, "description": "This move enables the user to attack first. This move fails if the target is not readying an attack."},

    # Steel moves
    "iron_tail": {"name": "Iron Tail", "type": "steel", "power": 100, "accuracy": 75, "category": "physical", "pp": 15, "description": "The target is slammed with a steel-hard tail. This may also lower the target's Defense stat."},
    "flash_cannon": {"name": "Flash Cannon", "type": "steel", "power": 80, "accuracy": 100, "category": "special", "pp": 10, "description": "The user gathers all its light energy and releases it at once. This may also lower the target's Sp. Def stat."},
    "heavy_slam": {"name": "Heavy Slam", "type": "steel", "power": 0, "accuracy": 100, "category": "physical", "pp": 10, "weight_based": True, "description": "The user slams into the target with its heavy body. The more the user outweighs the target, the greater the move's power."},

    # Fairy moves
    "moonblast": {"name": "Moonblast", "type": "fairy", "power": 95, "accuracy": 100, "category": "special", "pp": 15, "description": "Borrowing the power of the moon, the user attacks the target. This may also lower the target's Sp. Atk stat."},
    "fairy_wind": {"name": "Fairy Wind", "type": "fairy", "power": 40, "accuracy": 100, "category": "special", "pp": 30, "description": "The user stirs up a fairy wind and strikes the target with it."},
    "dazzling_gleam": {"name": "Dazzling Gleam", "type": "fairy", "power": 80, "accuracy": 100, "category": "special", "pp": 10, "description": "The user damages opposing monsters by emitting a powerful flash."},

    # Legendary signature
    "lunar_dance": {"name": "Lunar Dance", "type": "psychic", "power": 0, "accuracy": None, "category": "status", "pp": 10, "sacrifice": True, "description": "The user faints. In return, the monster taking its place will have its status and HP fully restored."},
    "solar_charge": {"name": "Solar Charge", "type": "fire", "power": 140, "accuracy": 95, "category": "special", "pp": 5, "heal": 0.5, "description": "The user absorbs solar energy and releases a massive blast, healing itself with the absorbed energy."},
    "morning_sun": {"name": "Morning Sun", "type": "normal", "power": 0, "accuracy": None, "category": "status", "pp": 5, "heal": 0.67, "description": "The user restores its own HP. The amount of HP regained varies with the weather."},
    "ion_deluge": {"name": "Ion Deluge", "type": "electric", "power": 0, "accuracy": None, "category": "status", "pp": 25, "description": "The user disperses electrically charged particles, which changes Normal-type moves to Electric-type."},
}

def get_move_data(move_id):
    """Get move data by ID."""
    return MOVES.get(move_id, None)

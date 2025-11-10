"""
Game Configuration and Constants
"""

# Game Version
VERSION = "0.1.0"
GAME_NAME = "Void Dominion"

# Starting Values
STARTING_CREDITS = 50000
STARTING_LOCATION = "nexus_prime"
STARTING_VESSEL = "scout_standard_mk1"  # Standard Scout MK1 - basic starting ship

# Game Balance
BASE_SKILL_TRAIN_TIME = 300  # seconds for level 1
SKILL_TIME_MULTIPLIER = 1.5  # each level takes 1.5x longer
MARKET_FLUCTUATION_RANGE = 0.15  # 15% price variance
CONTRACT_COOLDOWN = 600  # 10 minutes between contracts

# Combat
COMBAT_TURN_DURATION = 10  # seconds per combat turn
BASE_WEAPON_DAMAGE = 100
BASE_SHIELD_CAPACITY = 500
BASE_ARMOR_RATING = 100

# Economy
TAX_RATE = 0.05  # 5% transaction tax
MANUFACTURING_TIME_BASE = 1800  # 30 minutes base manufacturing
MINING_CYCLE_TIME = 300  # 5 minutes per mining cycle

# Territory Control
SECTOR_CLAIM_COST = 1000000  # 1 million credits to claim
SECTOR_UPKEEP_COST = 50000  # per game day
TERRITORY_CONTROL_BONUS = 0.1  # 10% bonus in controlled territory

# File Paths
SAVE_FILE = "save_game.yaml"
DATA_DIR = "data"

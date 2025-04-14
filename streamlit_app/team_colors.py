"""
NBA Team Colors and Logos Module

This module provides dictionaries of NBA team colors and logo URLs for use in visualizations
and team displays throughout the dashboard.
"""

# NBA Team Primary and Secondary Colors
TEAM_COLORS = {
    'Atlanta Hawks': {'primary': '#E03A3E', 'secondary': '#C1D32F', 'tertiary': '#26282A'},
    'Boston Celtics': {'primary': '#007A33', 'secondary': '#BA9653', 'tertiary': '#FFFFFF'},
    'Brooklyn Nets': {'primary': '#000000', 'secondary': '#FFFFFF', 'tertiary': '#CD1041'},
    'Charlotte Hornets': {'primary': '#1D1160', 'secondary': '#00788C', 'tertiary': '#A1A1A4'},
    'Chicago Bulls': {'primary': '#CE1141', 'secondary': '#000000', 'tertiary': '#FFFFFF'},
    'Cleveland Cavaliers': {'primary': '#860038', 'secondary': '#041E42', 'tertiary': '#FDBB30'},
    'Dallas Mavericks': {'primary': '#00538C', 'secondary': '#002B5E', 'tertiary': '#B8C4CA'},
    'Denver Nuggets': {'primary': '#0E2240', 'secondary': '#FEC524', 'tertiary': '#8B2131'},
    'Detroit Pistons': {'primary': '#C8102E', 'secondary': '#1D42BA', 'tertiary': '#BEC0C2'},
    'Golden State Warriors': {'primary': '#1D428A', 'secondary': '#FFC72C', 'tertiary': '#26282A'},
    'Houston Rockets': {'primary': '#CE1141', 'secondary': '#000000', 'tertiary': '#C4CED4'},
    'Indiana Pacers': {'primary': '#002D62', 'secondary': '#FDBB30', 'tertiary': '#BEC0C2'},
    'Los Angeles Clippers': {'primary': '#C8102E', 'secondary': '#1D428A', 'tertiary': '#BEC0C2'},
    'Los Angeles Lakers': {'primary': '#552583', 'secondary': '#FDB927', 'tertiary': '#000000'},
    'Memphis Grizzlies': {'primary': '#5D76A9', 'secondary': '#12173F', 'tertiary': '#F5B112'},
    'Miami Heat': {'primary': '#98002E', 'secondary': '#F9A01B', 'tertiary': '#000000'},
    'Milwaukee Bucks': {'primary': '#00471B', 'secondary': '#EEE1C6', 'tertiary': '#0077C0'},
    'Minnesota Timberwolves': {'primary': '#0C2340', 'secondary': '#236192', 'tertiary': '#78BE20'},
    'New Orleans Pelicans': {'primary': '#0C2340', 'secondary': '#C8102E', 'tertiary': '#85714D'},
    'New York Knicks': {'primary': '#006BB6', 'secondary': '#F58426', 'tertiary': '#BEC0C2'},
    'Oklahoma City Thunder': {'primary': '#007AC1', 'secondary': '#EF3B24', 'tertiary': '#002D62'},
    'Orlando Magic': {'primary': '#0077C0', 'secondary': '#C4CED4', 'tertiary': '#000000'},
    'Philadelphia 76ers': {'primary': '#006BB6', 'secondary': '#ED174C', 'tertiary': '#002B5C'},
    'Phoenix Suns': {'primary': '#1D1160', 'secondary': '#E56020', 'tertiary': '#000000'},
    'Portland Trail Blazers': {'primary': '#E03A3E', 'secondary': '#000000', 'tertiary': '#FFFFFF'},
    'Sacramento Kings': {'primary': '#5A2D81', 'secondary': '#63727A', 'tertiary': '#000000'},
    'San Antonio Spurs': {'primary': '#C4CED4', 'secondary': '#000000', 'tertiary': '#FFFFFF'},
    'Toronto Raptors': {'primary': '#CE1141', 'secondary': '#000000', 'tertiary': '#A1A1A4'},
    'Utah Jazz': {'primary': '#002B5C', 'secondary': '#00471B', 'tertiary': '#F9A01B'},
    'Washington Wizards': {'primary': '#002B5C', 'secondary': '#E31837', 'tertiary': '#C4CED4'},
}

# NBA Team Logo URLs - Using official NBA CDN where possible
TEAM_LOGOS = {
    'Atlanta Hawks': 'https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg',
    'Boston Celtics': 'https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg',
    'Brooklyn Nets': 'https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg',
    'Charlotte Hornets': 'https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg',
    'Chicago Bulls': 'https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg',
    'Cleveland Cavaliers': 'https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg',
    'Dallas Mavericks': 'https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg',
    'Denver Nuggets': 'https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg',
    'Detroit Pistons': 'https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg',
    'Golden State Warriors': 'https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg',
    'Houston Rockets': 'https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg',
    'Indiana Pacers': 'https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg',
    'Los Angeles Clippers': 'https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg',
    'Los Angeles Lakers': 'https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg',
    'Memphis Grizzlies': 'https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg',
    'Miami Heat': 'https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg',
    'Milwaukee Bucks': 'https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg',
    'Minnesota Timberwolves': 'https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg',
    'New Orleans Pelicans': 'https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg',
    'New York Knicks': 'https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg',
    'Oklahoma City Thunder': 'https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg',
    'Orlando Magic': 'https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg',
    'Philadelphia 76ers': 'https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg',
    'Phoenix Suns': 'https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg',
    'Portland Trail Blazers': 'https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg',
    'Sacramento Kings': 'https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg',
    'San Antonio Spurs': 'https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg',
    'Toronto Raptors': 'https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg',
    'Utah Jazz': 'https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg',
    'Washington Wizards': 'https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg',
}

# NBA Team IDs mapping
TEAM_IDS = {
    1610612737: 'Atlanta Hawks',
    1610612738: 'Boston Celtics',
    1610612751: 'Brooklyn Nets',
    1610612766: 'Charlotte Hornets',
    1610612741: 'Chicago Bulls',
    1610612739: 'Cleveland Cavaliers',
    1610612742: 'Dallas Mavericks',
    1610612743: 'Denver Nuggets',
    1610612765: 'Detroit Pistons',
    1610612744: 'Golden State Warriors',
    1610612745: 'Houston Rockets',
    1610612754: 'Indiana Pacers',
    1610612746: 'Los Angeles Clippers',
    1610612747: 'Los Angeles Lakers',
    1610612763: 'Memphis Grizzlies',
    1610612748: 'Miami Heat',
    1610612749: 'Milwaukee Bucks',
    1610612750: 'Minnesota Timberwolves',
    1610612740: 'New Orleans Pelicans',
    1610612752: 'New York Knicks',
    1610612760: 'Oklahoma City Thunder',
    1610612753: 'Orlando Magic',
    1610612755: 'Philadelphia 76ers',
    1610612756: 'Phoenix Suns',
    1610612757: 'Portland Trail Blazers',
    1610612758: 'Sacramento Kings',
    1610612759: 'San Antonio Spurs',
    1610612761: 'Toronto Raptors',
    1610612762: 'Utah Jazz',
    1610612764: 'Washington Wizards',
}

def get_team_colors(team_name):
    """
    Get the color scheme for a specific team.
    
    Args:
        team_name (str): The full name of the NBA team
        
    Returns:
        dict: Dictionary containing primary, secondary, and tertiary colors
              If team not found, returns default NBA colors
    """
    return TEAM_COLORS.get(team_name, {'primary': '#17408B', 'secondary': '#C9082A', 'tertiary': '#FFFFFF'})

def get_team_logo(team_name):
    """
    Get the logo URL for a specific team.
    
    Args:
        team_name (str): The full name of the NBA team
        
    Returns:
        str: URL to the team logo
             If team not found, returns NBA logo
    """
    return TEAM_LOGOS.get(team_name, 'https://cdn.nba.com/logos/nba/nba-logoman-75.svg')

def get_team_name_from_id(team_id):
    """
    Get the team name from a team ID.
    
    Args:
        team_id (int): The NBA team ID
        
    Returns:
        str: Team full name or 'Unknown Team' if not found
    """
    return TEAM_IDS.get(team_id, 'Unknown Team') 
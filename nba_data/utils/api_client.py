import os
from typing import Dict, Any, List, Optional, Tuple
from balldontlie import BalldontlieAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NBAApiClient:
    """Client for interacting with the balldontlie API using the official package"""
    
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv('BALLDONTLIE_API_KEY')
        if not api_key:
            raise ValueError("BALLDONTLIE_API_KEY environment variable is required")
        
        self.api = BalldontlieAPI(api_key=api_key)
    
    def get_all_teams(self) -> List[Dict]:
        """Get all NBA teams"""
        response = self.api.nba.teams.list()
        
        # Handle ListResponse object - get the data attribute directly
        if hasattr(response, 'data'):
            # Convert NBATeam objects to dictionaries
            teams = []
            for team in response.data:
                team_dict = {
                    'id': team.id,
                    'abbreviation': team.abbreviation,
                    'city': team.city,
                    'conference': team.conference,
                    'division': team.division,
                    'full_name': team.full_name,
                    'name': team.name
                }
                teams.append(team_dict)
            return teams
        return []
    
    def get_players(self, per_page: int = 25, cursor: Optional[int] = None) -> Tuple[List[Dict], Optional[int]]:
        """
        Get paginated list of players
        
        Args:
            per_page: Number of players per page
            cursor: Cursor for pagination (new pagination style)
            
        Returns:
            Tuple containing (list of player dictionaries, next cursor)
        """
        params = {
            'per_page': per_page,
            'cursor': cursor
        }
            
        response = self.api.nba.players.list(**params)
        
        # Default return values
        players = []
        next_cursor = None
        
        # Handle ListResponse object - get the data attribute directly
        if hasattr(response, 'data'):
            # Convert NBAPlayer objects to dictionaries
            for player in response.data:
                # Extract team data if available
                team_data = None
                if hasattr(player, 'team') and player.team:
                    team_data = {
                        'id': player.team.id,
                        'abbreviation': player.team.abbreviation,
                        'city': player.team.city,
                        'conference': player.team.conference,
                        'division': player.team.division,
                        'full_name': player.team.full_name,
                        'name': player.team.name
                    }
                
                player_dict = {
                    'id': player.id,
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'position': getattr(player, 'position', ''),
                    'height': getattr(player, 'height', None),
                    'weight_pounds': getattr(player, 'weight_pounds', None),
                    'jersey_number': getattr(player, 'jersey_number', None),
                    'college': getattr(player, 'college', None),
                    'country': getattr(player, 'country', None),
                    'draft_year': getattr(player, 'draft_year', None),
                    'draft_round': getattr(player, 'draft_round', None),
                    'draft_number': getattr(player, 'draft_number', None),
                    'team': team_data
                }
                players.append(player_dict)
        
        # Extract next cursor if available
        if hasattr(response, 'meta') and hasattr(response.meta, 'next_cursor'):
            next_cursor = response.meta.next_cursor
            
        return players, next_cursor
    
    def get_games(self, **params) -> Tuple[List[Dict], Optional[int]]:
        """
        Get games with optional filters
        
        Args:
            **params: Parameters to filter games by (per_page, cursor, seasons, team_ids, etc.)
            
        Returns:
            Tuple containing (list of game dictionaries, next cursor)
        """
        response = self.api.nba.games.list(**params)
        
        # Default return values
        games = []
        next_cursor = None
        
        # Handle ListResponse object - get the data attribute directly
        if hasattr(response, 'data'):
            # Convert NBAGame objects to dictionaries
            for game in response.data:
                # Extract home team data
                home_team = None
                if hasattr(game, 'home_team') and game.home_team:
                    home_team = {
                        'id': game.home_team.id,
                        'abbreviation': game.home_team.abbreviation,
                        'city': game.home_team.city,
                        'conference': game.home_team.conference,
                        'division': game.home_team.division,
                        'full_name': game.home_team.full_name,
                        'name': game.home_team.name
                    }
                
                # Extract visitor team data
                visitor_team = None
                if hasattr(game, 'visitor_team') and game.visitor_team:
                    visitor_team = {
                        'id': game.visitor_team.id,
                        'abbreviation': game.visitor_team.abbreviation,
                        'city': game.visitor_team.city,
                        'conference': game.visitor_team.conference,
                        'division': game.visitor_team.division,
                        'full_name': game.visitor_team.full_name,
                        'name': game.visitor_team.name
                    }
                
                game_dict = {
                    'id': game.id,
                    'date': game.date,
                    'datetime': getattr(game, 'datetime', None),
                    'home_team': home_team,
                    'visitor_team': visitor_team,
                    'home_team_score': game.home_team_score,
                    'visitor_team_score': game.visitor_team_score,
                    'season': getattr(game, 'season', None),
                    'status': game.status,
                    'period': getattr(game, 'period', None),
                    'time': getattr(game, 'time', None),
                    'postseason': getattr(game, 'postseason', False)
                }
                
                games.append(game_dict)
        
        # Extract next cursor if available
        if hasattr(response, 'meta') and hasattr(response.meta, 'next_cursor'):
            next_cursor = response.meta.next_cursor
            
        return games, next_cursor
    
    def _process_response(self, response) -> Dict:
        """Process API response into a dictionary format"""
        result = {}
        
        # Extract data from response
        if hasattr(response, 'data'):
            result['data'] = response.data
        
        # Extract meta information if available
        if hasattr(response, 'meta'):
            result['meta'] = {}
            meta = response.meta
            
            # Copy common meta fields
            for field in ['total_pages', 'current_page', 'next_page', 'per_page', 'total_count', 'next_cursor']:
                if hasattr(meta, field):
                    result['meta'][field] = getattr(meta, field)
        
        return result

# Create a singleton instance
api_client = NBAApiClient()
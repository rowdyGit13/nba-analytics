from typing import List, Dict, Any, Union
from ..repositories.search_repository import SearchRepository
from nba_data.models import Player, Team # Import Game if game search is added

class SearchService:

    MAX_RESULTS = 5 # Max cards to display as per spec
    PLACEHOLDER_LOGO = 'https://via.placeholder.com/50' # Placeholder if logo not in db
    PLACEHOLDER_PHOTO = 'https://via.placeholder.com/100' # Placeholder if photo not in db

    @staticmethod
    def perform_search(search_term: str, search_type: str, season: int) -> List[Dict[str, Any]]:
        """Performs search based on type and formats results for the frontend."""
        results = []
        if not search_term or not season:
            return results

        try:
            season_int = int(season) # Ensure season is an integer
        except ValueError:
            print(f"Invalid season format: {season}")
            return [] # Or raise an error

        if search_type == 'player':
            players = SearchRepository.search_players(search_term, limit=SearchService.MAX_RESULTS)
            for player in players:
                results.append(SearchService._format_player_result(player))
        
        elif search_type == 'team':
            teams = SearchRepository.search_teams(search_term, limit=SearchService.MAX_RESULTS)
            for team in teams:
                stats = SearchRepository.get_team_stats(team, season_int)
                results.append(SearchService._format_team_result(team, stats))

        # elif search_type == 'game':
            # games = SearchRepository.search_games(search_term, season_int, limit=SearchService.MAX_RESULTS)
            # for game in games:
            #     results.append(SearchService._format_game_result(game))

        return results

    @staticmethod
    def _format_player_result(player: Player) -> Dict[str, Any]:
        """Formats player data for the template card."""
        return {
            'type': 'player',
            'name': f"{player.first_name} {player.last_name}",
            'photo': SearchService.PLACEHOLDER_PHOTO, # Use placeholder
            'height': player.height_display, 
            'position': player.position or 'N/A',
            'team_name': player.team.full_name if player.team else 'Free Agent',
            'team_logo': SearchService.PLACEHOLDER_LOGO, # Use placeholder
            # Add other relevant player fields if needed
        }

    @staticmethod
    def _format_team_result(team: Team, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Formats team data and stats for the template card."""
        return {
            'type': 'team',
            'name': team.full_name,
            'logo': SearchService.PLACEHOLDER_LOGO, # Use placeholder
            'ppg': stats.get('ppg', 0),
            'papg': stats.get('papg', 0),
            'record': stats.get('record', '0-0'),
            # Add other relevant team fields if needed
        }

    # @staticmethod
    # def _format_game_result(game: Game) -> Dict[str, Any]:
    #     """Formats game data for the template card."""
    #     # TODO: Implement game formatting
    #     return {
    #         'type': 'game',
    #         # ... add game details
    #     } 
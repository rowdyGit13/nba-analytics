from typing import List, Dict, Any
from ..repositories.visualization_repository import VisualizationRepository
from nba_data.models import Team
import json

class VisualizationService:

    DATASET_OPTIONS = {
        'ppg': 'Points Per Game vs Season',
        'papg': 'Points Allowed Per Game vs Season',
        'wins': 'Wins vs Season',
        'home_wins': 'Home Wins vs Season',
        'away_wins': 'Away Wins vs Season'
    }

    @staticmethod
    def get_all_teams_for_select() -> List[Dict[str, Any]]:
        """Gets all teams formatted for a dropdown select."""
        teams = VisualizationRepository.get_all_teams()
        return [{'id': team.id, 'name': team.full_name} for team in teams]

    @staticmethod
    def get_chart_data(team_id: int, dataset_key: str) -> str:
        """Fetches seasonal data and formats it for Chart.js."""
        if not team_id or dataset_key not in VisualizationService.DATASET_OPTIONS:
            return json.dumps({'labels': [], 'data': [], 'label': 'Select Team and Dataset'})
        
        try:
            team_id_int = int(team_id)
        except ValueError:
            print(f"Invalid team ID for chart data: {team_id}")
            return json.dumps({'labels': [], 'data': [], 'label': 'Invalid Team ID'})

        seasonal_stats = VisualizationRepository.get_team_seasonal_stats(team_id_int)
        
        labels = [str(stat['season']) for stat in seasonal_stats]
        data = [round(stat.get(dataset_key, 0), 1) for stat in seasonal_stats] # Round to 1 decimal
        label = f"{VisualizationService.DATASET_OPTIONS[dataset_key]} for Team ID {team_id_int}" # TODO: Get team name

        chart_data = {
            'labels': labels,
            'data': data,
            'label': label,
        }
        return json.dumps(chart_data) 
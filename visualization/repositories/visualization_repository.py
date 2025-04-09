from typing import List, Dict, Any
from django.db.models import Avg, Count, Q, Sum, F
from nba_data.models import Team, Game

class VisualizationRepository:

    @staticmethod
    def get_all_teams() -> List[Team]:
        """Fetches all teams for the dropdown selector."""
        try:
            return Team.objects.all().order_by('full_name')
        except Exception as e:
            print(f"Error fetching all teams: {e}")
            return []

    @staticmethod
    def get_team_seasonal_stats(team_id: int) -> List[Dict[str, Any]]:
        """Aggregates key stats for a given team, grouped by season."""
        seasonal_data = []
        try:
            # Get all seasons the team played games in
            seasons = Game.objects.filter(Q(home_team_id=team_id) | Q(visitor_team_id=team_id)) \
                                  .values_list('season', flat=True).distinct().order_by('season')

            for season in seasons:
                home_games = Game.objects.filter(home_team_id=team_id, season=season)
                away_games = Game.objects.filter(visitor_team_id=team_id, season=season)
                
                home_stats = home_games.aggregate(
                    total_points_scored=Sum('home_team_score'),
                    total_points_allowed=Sum('visitor_team_score'),
                    wins=Count('pk', filter=Q(home_team_score__gt=F('visitor_team_score')))
                )
                
                away_stats = away_games.aggregate(
                    total_points_scored=Sum('visitor_team_score'),
                    total_points_allowed=Sum('home_team_score'),
                    wins=Count('pk', filter=Q(visitor_team_score__gt=F('home_team_score')))
                )

                total_games_count = home_games.count() + away_games.count()
                if total_games_count > 0:
                    total_points_scored = (home_stats['total_points_scored'] or 0) + (away_stats['total_points_scored'] or 0)
                    total_points_allowed = (home_stats['total_points_allowed'] or 0) + (away_stats['total_points_allowed'] or 0)
                    total_wins = (home_stats['wins'] or 0) + (away_stats['wins'] or 0)
                    home_wins = home_stats['wins'] or 0
                    away_wins = away_stats['wins'] or 0
                    
                    ppg = total_points_scored / total_games_count
                    papg = total_points_allowed / total_games_count
                    
                    seasonal_data.append({
                        'season': season,
                        'ppg': ppg,
                        'papg': papg,
                        'wins': total_wins,
                        'home_wins': home_wins,
                        'away_wins': away_wins
                    })
        
        except Exception as e:
            print(f"Error fetching seasonal stats for team {team_id}: {e}")
            # Handle error appropriately, maybe return partial data or empty list

        return seasonal_data 
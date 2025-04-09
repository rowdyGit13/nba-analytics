from typing import List, Optional, Dict, Any
from django.db.models import Q, Avg, Count, Sum, F
from nba_data.models import Player, Team, Game

class SearchRepository:

    @staticmethod
    def search_players(name_query: str, limit: int = 10) -> List[Player]:
        """Searches for players by first or last name."""
        try:
            # Simple search: combine first and last names and check if query is contained
            # More complex search could involve splitting query and checking first/last names separately
            return Player.objects.filter(
                Q(first_name__icontains=name_query) | Q(last_name__icontains=name_query)
            ).select_related('team')[:limit] # Limit results for performance
        except Exception as e:
            print(f"Error searching players: {e}")
            # Consider logging the error
            return []

    @staticmethod
    def search_teams(name_query: str, limit: int = 10) -> List[Team]:
        """Searches for teams by full name, name, city, or abbreviation."""
        try:
            return Team.objects.filter(
                Q(full_name__icontains=name_query) |
                Q(name__icontains=name_query) |
                Q(city__icontains=name_query) |
                Q(abbreviation__iexact=name_query) # Exact match for abbreviation
            )[:limit]
        except Exception as e:
            print(f"Error searching teams: {e}")
            return []

    @staticmethod
    def get_team_stats(team: Team, season: int) -> Dict[str, Any]:
        """Calculates PPG, PAPG, and record for a team in a given season."""
        stats = {
            'ppg': 0,
            'papg': 0,
            'wins': 0,
            'losses': 0,
            'record': '0-0'
        }
        try:
            home_games = Game.objects.filter(home_team=team, season=season)
            away_games = Game.objects.filter(visitor_team=team, season=season)
            
            home_stats = home_games.aggregate(
                total_points_scored=Sum('home_team_score'),
                total_points_allowed=Sum('visitor_team_score'),
                wins=Count('pk', filter=Q(home_team_score__gt=F('visitor_team_score'))),
                losses=Count('pk', filter=Q(home_team_score__lt=F('visitor_team_score')))
            )
            
            away_stats = away_games.aggregate(
                total_points_scored=Sum('visitor_team_score'),
                total_points_allowed=Sum('home_team_score'),
                wins=Count('pk', filter=Q(visitor_team_score__gt=F('home_team_score'))),
                losses=Count('pk', filter=Q(visitor_team_score__lt=F('home_team_score')))
            )

            total_games = home_games.count() + away_games.count()
            if total_games > 0:
                total_points_scored = (home_stats['total_points_scored'] or 0) + (away_stats['total_points_scored'] or 0)
                total_points_allowed = (home_stats['total_points_allowed'] or 0) + (away_stats['total_points_allowed'] or 0)
                total_wins = (home_stats['wins'] or 0) + (away_stats['wins'] or 0)
                total_losses = (home_stats['losses'] or 0) + (away_stats['losses'] or 0)
                
                stats['ppg'] = total_points_scored / total_games
                stats['papg'] = total_points_allowed / total_games
                stats['wins'] = total_wins
                stats['losses'] = total_losses
                stats['record'] = f"{total_wins}-{total_losses}"
                
        except Exception as e:
            print(f"Error calculating team stats for {team.full_name}, season {season}: {e}")
            # Return default stats on error
        
        return stats

    # TODO: Implement search_games if needed
    # @staticmethod
    # def search_games(query: str, season: int, limit: int = 10) -> List[Game]:
    #     pass 
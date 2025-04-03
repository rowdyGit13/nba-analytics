from django.core.management.base import BaseCommand
from nba_data.models import Game, Team
from nba_data.utils.api_client import api_client
import logging
from datetime import datetime
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import NBA games from the API'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, required=True, 
                            help='Season to import (e.g., 2023 for 2023-2024 season)')
        parser.add_argument('--max-pages', type=int, default=25, 
                            help='Maximum number of pages to import')

    def handle(self, *args, **options):
        season = options['season']
        max_pages = options['max_pages']
        self.stdout.write(f'Importing NBA games for {season}-{season+1} season (up to {max_pages} pages)...')
        
        try:
            page_count = 0
            next_cursor = None
            
            while page_count < max_pages:
                page_count += 1
                self.stdout.write(f'Fetching page {page_count} of maximum {max_pages}...')
                
                # Get games from API
                params = {
                    'per_page': 25,
                    'seasons': [season]
                }
                
                if next_cursor:
                    params['cursor'] = next_cursor
                
                games_data, next_cursor = api_client.get_games(**params)
                
                if not games_data:
                    self.stdout.write('No more games found.')
                    break
                
                self.stdout.write(f'Processing {len(games_data)} games...')
                
                # Process each game
                for game_data in games_data:
                    # Get the related teams
                    try:
                        home_team = Team.objects.get(team_id=game_data['home_team']['id'])
                        visitor_team = Team.objects.get(team_id=game_data['visitor_team']['id'])
                    except Team.DoesNotExist as e:
                        self.stdout.write(self.style.WARNING(
                            f"Team not found: {str(e)}. Run import_teams first."
                        ))
                        continue
                    
                    # Parse the date and datetime
                    game_date = datetime.strptime(game_data['date'][:10], '%Y-%m-%d').date()
                    game_datetime = None
                    if game_data.get('datetime'):
                        try:
                            game_datetime = make_aware(datetime.strptime(game_data['datetime'], '%Y-%m-%d %H:%M:%S%z'))
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Could not parse datetime: {game_data['datetime']}"))
                    
                    # Update or create game
                    game, created = Game.objects.update_or_create(
                        game_id=game_data['id'],
                        defaults={
                            'date': game_date,
                            'datetime': game_datetime,
                            'home_team': home_team,
                            'visitor_team': visitor_team,
                            'home_team_score': game_data['home_team_score'],
                            'visitor_team_score': game_data['visitor_team_score'],
                            'season': season,
                            'status': game_data['status'],
                            'period': game_data.get('period'),
                            'time': game_data.get('time'),
                            'postseason': game_data.get('postseason', False),
                        }
                    )
                    
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'{action} game: {visitor_team.abbreviation} @ {home_team.abbreviation} ({game_date})')
                
                # Check if we have a next cursor
                if not next_cursor:
                    self.stdout.write('No more pages available.')
                    break
            
            self.stdout.write(self.style.SUCCESS('Successfully imported games'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing games: {str(e)}'))
            logger.error(f'Error importing games: {str(e)}', exc_info=True)
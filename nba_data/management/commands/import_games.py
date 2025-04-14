from django.core.management.base import BaseCommand
from nba_data.models import Game, Team
from nba_data.utils.api_client import api_client
import logging
from datetime import datetime
from django.utils.timezone import make_aware
import time
import re

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import NBA games from the API'

    def add_arguments(self, parser):
        parser.add_argument('--seasons', type=str, nargs='+', required=True, 
                            help='Seasons to import. Use individual years (e.g., 2022 2023) or ranges (e.g., 2022-2024)')
        parser.add_argument('--max-pages', type=int, default=100, 
                            help='Maximum number of pages to import per season')
        parser.add_argument('--start-cursor', type=int, default=None,
                            help='API cursor to start fetching from (for resuming imports - only applies to first season)')
    
    def parse_seasons(self, season_args):
        """Parse season arguments which can be individual years or ranges."""
        seasons = []
        
        for arg in season_args:
            # Check if it's a range (e.g., 2022-2024)
            range_match = re.match(r'^(\d{4})-(\d{4})$', arg)
            if range_match:
                start_year = int(range_match.group(1))
                end_year = int(range_match.group(2))
                if start_year <= end_year:
                    seasons.extend(range(start_year, end_year + 1))
                else:
                    self.stdout.write(self.style.WARNING(f"Invalid range: {arg}. Start year must be <= end year."))
            else:
                # Try parsing as a single year
                try:
                    seasons.append(int(arg))
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid season format: {arg}"))
        
        # Remove duplicates and sort
        seasons = sorted(list(set(seasons)))
        
        if not seasons:
            self.stdout.write(self.style.ERROR("No valid seasons specified."))
        
        return seasons

    def handle(self, *args, **options):
        season_args = options['seasons']
        max_pages = options['max_pages']
        start_cursor = options['start_cursor']
        
        # Parse seasons from arguments
        seasons = self.parse_seasons(season_args)
        
        if not seasons:
            self.stdout.write(self.style.ERROR("No valid seasons to import. Exiting."))
            return
        
        self.stdout.write(f'Importing NBA games for seasons: {", ".join(str(s) for s in seasons)}')
        total_games_processed = 0
        
        for season in seasons:
            self.stdout.write(self.style.SUCCESS(f'\nProcessing season: {season}-{season+1}'))
            games_processed = self.import_season(season, max_pages, start_cursor)
            total_games_processed += games_processed
            
            # Only use start_cursor for the first season
            start_cursor = None
            
        self.stdout.write(self.style.SUCCESS(f'\nAll imports completed. Total games processed: {total_games_processed}'))
    
    def import_season(self, season, max_pages, start_cursor):
        """Import games for a specific season"""
        self.stdout.write(f'Importing NBA games for {season}-{season+1} season (up to {max_pages} pages)...')
        if start_cursor:
            self.stdout.write(f'Starting from cursor: {start_cursor}')
        
        page_count = 0
        next_cursor = start_cursor
        games_processed_in_session = 0
        max_retries = 5
        current_retries = 0

        while page_count < max_pages:
            page_count += 1
            self.stdout.write(f'Fetching page {page_count} of maximum {max_pages} (Cursor: {next_cursor})...')
            
            try:
                # Get games from API
                params = {
                    'per_page': 25,
                    'seasons': [season]
                }
                
                if next_cursor:
                    params['cursor'] = next_cursor
                
                games_data, current_cursor_result = api_client.get_games(**params)
                
                # Reset retries on successful call
                current_retries = 0

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
                            dt_str = game_data['datetime']
                            if dt_str.endswith('Z'):
                                game_datetime = make_aware(datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
                            else:
                                game_datetime = make_aware(datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ'))
                        except ValueError as dt_err:
                            self.stdout.write(self.style.WARNING(f"Could not parse datetime: {game_data.get('datetime')} - Error: {dt_err}"))
                    
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
                            'season': season_str,
                            'status': game_data['status'],
                            'period': game_data.get('period'),
                            'time': game_data.get('time'),
                            'postseason': game_data.get('postseason', False),
                        }
                    )
                    
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'{action} game: {visitor_team.abbreviation} @ {home_team.abbreviation} ({game_date})')
                    games_processed_in_session += 1
                
                # Update next_cursor ONLY after successful processing of the page
                next_cursor = current_cursor_result

                # Check if we have a next cursor
                if not next_cursor:
                    self.stdout.write('No more pages available.')
                    break

            except Exception as e:
                if "Too Many Requests" in str(e):
                    if current_retries < max_retries:
                        current_retries += 1
                        wait_time = 60 * current_retries
                        self.stdout.write(self.style.WARNING(
                            f"Rate limit hit. Retrying page {page_count} in {wait_time} seconds... (Attempt {current_retries}/{max_retries})"
                        ))
                        time.sleep(wait_time)
                        page_count -= 1
                        continue
                    else:
                        self.stdout.write(self.style.ERROR(
                            f"Max retries reached for rate limit on page {page_count}. Stopping."
                        ))
                        self.stdout.write(f"To resume later, use: --start-cursor {next_cursor} --seasons {season}")
                        logger.error(f'Rate limit max retries reached: {str(e)}', exc_info=True)
                        break
                else:
                    self.stdout.write(self.style.ERROR(f'Error importing games on page {page_count}: {str(e)}'))
                    self.stdout.write(f"Error occurred. Last successful cursor was: {next_cursor}")
                    self.stdout.write(f"Consider resuming with: --start-cursor {next_cursor} --seasons {season}")
                    logger.error(f'Error importing games: {str(e)}', exc_info=True)
                    break

        if page_count >= max_pages:
            self.stdout.write(self.style.WARNING(f'Reached max pages ({max_pages}) for season {season}-{season+1}.'))
            if next_cursor:
                self.stdout.write(f"To continue fetching this season, run again with: --start-cursor {next_cursor} --seasons {season}")

        self.stdout.write(self.style.SUCCESS(f'Finished season {season}-{season+1}. Processed {games_processed_in_session} games.'))
        if next_cursor:
            self.stdout.write(f"Last API cursor processed was: {next_cursor}")
            
        return games_processed_in_session
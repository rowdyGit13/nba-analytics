from django.core.management.base import BaseCommand
from nba_data.models import Team, Player
from nba_data.utils.api_client import api_client
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

def parse_height(height_str: str) -> tuple[int | None, int | None, int | None]:
    """
    Parse height string (e.g. '6-2') into feet, inches, and total inches
    Returns tuple of (feet, inches, total_inches)
    """
    if not height_str or '-' not in height_str:
        return None, None, None
    
    try:
        feet_str, inches_str = height_str.split('-')
        feet = int(feet_str)
        inches = int(inches_str)
        total_inches = (feet * 12) + inches
        return feet, inches, total_inches
    except (ValueError, IndexError):
        return None, None, None

class Command(BaseCommand):
    help = 'Import NBA players from the API'
    
    def add_arguments(self, parser):
        parser.add_argument('--max-pages', type=int, default=20, 
                            help='Maximum number of pages to import')

    def handle(self, *args, **options):
        max_pages = options.get('max_pages', 20)
        self.stdout.write(f'Importing NBA players (up to {max_pages} pages)...')
        
        try:
            page_count = 0
            next_cursor = None
            
            while page_count < max_pages:
                page_count += 1
                self.stdout.write(f'Fetching page {page_count} of maximum {max_pages}...')
                
                # Get players from API
                players_data, next_cursor = api_client.get_players(per_page=25, cursor=next_cursor)
                
                if not players_data:
                    self.stdout.write('No more players found.')
                    break
                
                self.stdout.write(f'Processing {len(players_data)} players...')
                
                # Process each player
                for player_data in players_data:
                    # Get or create the player's team
                    team = None
                    if player_data.get('team') and player_data['team'].get('id'):
                        try:
                            team = Team.objects.get(team_id=player_data['team']['id'])
                        except Team.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f"Team with ID {player_data['team']['id']} not found. Run import_teams first."
                            ))
                    
                    # Parse height
                    height_feet, height_inches, height_total = parse_height(player_data.get('height'))
                    
                    # Update or create player
                    player, created = Player.objects.update_or_create(
                        player_id=player_data['id'],
                        defaults={
                            'first_name': player_data['first_name'],
                            'last_name': player_data['last_name'],
                            'position': player_data.get('position', ''),
                            'height_feet': height_feet,
                            'height_inches': height_inches,
                            'height_total_inches': height_total,
                            'weight_pounds': player_data.get('weight_pounds'),
                            'team': team,
                        }
                    )
                    
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'{action} player: {player.first_name} {player.last_name}')
                
                # Check if we have a next cursor
                if not next_cursor:
                    self.stdout.write('No more pages available.')
                    break
            
            self.stdout.write(self.style.SUCCESS('Successfully imported players'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing players: {str(e)}'))
            logger.error(f'Error importing players: {str(e)}', exc_info=True)
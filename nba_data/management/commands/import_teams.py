from django.core.management.base import BaseCommand
from nba_data.models import Team
from nba_data.utils.api_client import api_client
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import all NBA teams from the API'

    def handle(self, *args, **options):
        self.stdout.write('Importing NBA teams...')
        
        # Get teams from API
        try:
            teams_data = api_client.get_all_teams()
            
            if not teams_data:
                self.stdout.write(self.style.WARNING('No teams found in the API response.'))
                return
            
            self.stdout.write(f'Found {len(teams_data)} teams')
            
            # Process each team
            for team_data in teams_data:
                team, created = Team.objects.update_or_create(
                    team_id=team_data['id'],
                    defaults={
                        'abbreviation': team_data['abbreviation'],
                        'city': team_data['city'],
                        'conference': team_data['conference'],
                        'division': team_data['division'],
                        'full_name': team_data['full_name'],
                        'name': team_data['name'],
                    }
                )
                
                action = 'Created' if created else 'Updated'
                self.stdout.write(f'{action} team: {team.full_name}')
            
            self.stdout.write(self.style.SUCCESS('Successfully imported teams'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing teams: {str(e)}'))
            logger.error(f'Error importing teams: {str(e)}', exc_info=True)
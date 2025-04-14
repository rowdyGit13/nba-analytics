from django.core.management.base import BaseCommand
from nba_data.analytics import dataframes, data_prep, stats
import pandas as pd
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process NBA data for analysis'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, 
                           help='Season to process - provide start year only (e.g., 2022 for 2022-2023 season)')
        parser.add_argument('--export', action='store_true', help='Export processed data to CSV files')
        parser.add_argument('--export-dir', type=str, default='processed_data',
                            help='Directory to export data to (relative to current directory)')

    def handle(self, *args, **options):
        season = options.get('season')
        export = options.get('export', False)
        export_dir = options.get('export_dir')
        
        # Convert season to YYYY-YYYY format if provided
        season_str = None
        if season:
            season_str = f"{season}-{season+1}"
            self.stdout.write(f'Processing NBA data for season {season_str}...')
        else:
            self.stdout.write('Processing NBA data for all seasons...')
        
        # Create export directory if needed
        if export and not os.path.exists(export_dir):
            os.makedirs(export_dir)
            self.stdout.write(f'Created export directory: {export_dir}')
        
        try:
            # Step 1: Load data from database into pandas DataFrames
            self.stdout.write('Loading teams data...')
            teams_df = dataframes.get_teams_dataframe()
            if teams_df.empty:
                self.stdout.write(self.style.WARNING('No teams found. Run import_teams first.'))
                return
            
            self.stdout.write('Loading players data...')
            players_df = dataframes.get_players_dataframe()
            if players_df.empty:
                self.stdout.write(self.style.WARNING('No players found. Run import_players first.'))
                return
            
            self.stdout.write('Loading games data...')
            games_df = dataframes.get_games_dataframe()
            if games_df.empty:
                self.stdout.write(self.style.WARNING('No games found. Run import_games first.'))
                return
            
            # Filter by season if specified
            if season_str:
                self.stdout.write(f'Filtering data for season {season_str}...')
                if 'season' in games_df.columns:
                    games_df = games_df[games_df['season'] == season_str]
            
            # Step 2: Clean and transform data
            self.stdout.write('Cleaning and transforming player data...')
            cleaned_players_df = data_prep.clean_player_data(players_df)
            
            self.stdout.write('Cleaning and transforming teams data...')
            cleaned_teams_df = data_prep.clean_teams_data(teams_df)
            
            self.stdout.write('Cleaning and transforming games data...')
            cleaned_games_df = data_prep.clean_games_data(games_df)
            
            
            # Step 3: Calculate team statistics

            self.stdout.write('Preparing game data...')
            prepared_games_df = data_prep.enhance_game_data(cleaned_games_df)
            
        
            self.stdout.write('Calculating team statistics...')
            team_stats_df = data_prep.prepare_home_vs_away(prepared_games_df)
            
            if not team_stats_df.empty:
                self.stdout.write('Calculating team performance metrics...')
                team_metrics_df = stats.calculate_team_performance_metrics(team_stats_df)
                
                self.stdout.write('Calculating team rankings...')
                team_rankings_df = stats.calculate_team_rankings(team_metrics_df)
            else:
                team_metrics_df = pd.DataFrame()
                team_rankings_df = pd.DataFrame()
                self.stdout.write(self.style.WARNING(
                    'Could not calculate team statistics. Check that game data is complete.'
                ))
                
            # Step 4: Export processed data if requested
            if export:
                self.stdout.write('Exporting processed data...')
                
                # Define export mappings (DataFrame, filename)
                export_items = [
                    (cleaned_players_df, 'players.csv'),
                    (prepared_games_df, 'games.csv'),
                    (team_stats_df, 'team_stats.csv'),
                    (team_metrics_df, 'team_metrics.csv'),
                    (team_rankings_df, 'team_rankings.csv'),
                    (cleaned_teams_df, 'teams.csv')
                ]
                
                # Export each dataframe
                for df, filename in export_items:
                    if not df.empty:
                        season_suffix = f'_{season_str}' if season_str else ''
                        output_path = os.path.join(export_dir, f'{filename.split(".")[0]}{season_suffix}.csv')
                        df.to_csv(output_path, index=False)
                        self.stdout.write(f'  Exported {output_path}')
                
            
            self.stdout.write(self.style.SUCCESS('Successfully processed NBA data!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing data: {str(e)}'))
            logger.error(f'Error processing data: {str(e)}', exc_info=True) 
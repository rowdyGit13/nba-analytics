import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

# Use our custom data loader with fallback capability
from streamlit_app.data_loader import get_teams_dataframe, get_players_dataframe, get_games_dataframe

# App setup
st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to get seasons
def get_seasons():
    games_df = get_games_dataframe()
    if not games_df.empty:
        return sorted(games_df['season'].unique().tolist(), reverse=True)
    return []

# Sidebar navigation
st.sidebar.title("NBA Analytics Dashboard")
pages = ["Home", "Search", "Data Visualization"]
choice = st.sidebar.radio("Navigation", pages)

# Home page
if choice == "Home":
    st.title("Welcome to the NBA Analytics Dashboard")
    st.markdown("""
    This dashboard provides insights and visualizations of NBA data. You can:
    
    - Search for specific players or teams
    - View team statistics and performance metrics
    - Explore data visualizations of team performance across seasons
    
    Use the sidebar to navigate between pages.
    """)
    
    # Display a welcome image
    st.image("https://cdn.nba.com/manage/2021/08/NBA-75th-anniversary-diamond-logo.jpg", width=600)

# Search page
elif choice == "Search":
    st.title("Player & Team Search")
    
    # Get DataFrames
    players_df = get_players_dataframe()
    teams_df = get_teams_dataframe()
    games_df = get_games_dataframe()
    
    # Get list of seasons
    seasons = get_seasons()
    
    # Search tabs
    tab1, tab2 = st.tabs(["Player Search", "Team Search"])
    
    # Player Search Tab
    with tab1:
        st.subheader("Player Search")
        
        # Player search inputs
        player_name = st.text_input("Enter player name")
        selected_season = st.selectbox("Select Season", seasons if seasons else ["No data available"])
        
        if st.button("Search Player"):
            if player_name and not players_df.empty:
                # Filter players by name
                filtered_players = players_df[
                    players_df['full_name'].str.contains(player_name, case=False)
                ]
                
                if not filtered_players.empty:
                    # Display player cards (up to 5)
                    for _, player in filtered_players.head(5).iterrows():
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            # Display a placeholder NBA logo or player image if available
                            st.image("https://cdn.nba.com/logos/nba/nba-logoman-75.svg", width=100)
                        
                        with col2:
                            st.subheader(player['full_name'])
                            st.write(f"**Position:** {player['position'] if pd.notna(player['position']) else 'N/A'}")
                            st.write(f"**Height:** {player['height_feet']}-{player['height_inches'] if pd.notna(player['height_feet']) else 'N/A'}")
                            st.write(f"**Team:** {player['team_name'] if pd.notna(player['team_name']) else 'N/A'}")
                            if pd.notna(player['team_id']):
                                st.write(f"**Team Conference:** {player['team_conference']}")
                                st.write(f"**Team Division:** {player['team_division']}")
                else:
                    st.warning(f"No players found matching '{player_name}'")
    
    # Team Search Tab
    with tab2:
        st.subheader("Team Search")
        
        # Team search inputs
        if not teams_df.empty:
            team_list = sorted(teams_df['full_name'].unique().tolist())
            selected_team = st.selectbox("Select Team", team_list)
            selected_season = st.selectbox("Select Season", seasons if seasons else ["No data available"], key="team_season")
            
            if st.button("Search Team"):
                if selected_team and selected_season != "No data available":
                    team_id = teams_df[teams_df['full_name'] == selected_team]['team_id'].iloc[0]
                    
                    # Calculate team stats for the selected season
                    home_games = games_df[(games_df['home_team_id'] == team_id) & (games_df['season'] == selected_season)]
                    away_games = games_df[(games_df['visitor_team_id'] == team_id) & (games_df['season'] == selected_season)]
                    
                    if not home_games.empty or not away_games.empty:
                        # Calculate wins and losses
                        home_wins = len(home_games[home_games['home_team_score'] > home_games['visitor_team_score']])
                        home_losses = len(home_games) - home_wins
                        
                        away_wins = len(away_games[away_games['visitor_team_score'] > away_games['home_team_score']])
                        away_losses = len(away_games) - away_wins
                        
                        total_wins = home_wins + away_wins
                        total_losses = home_losses + away_losses
                        
                        # Calculate points per game and points allowed
                        home_points_scored = home_games['home_team_score'].mean() if len(home_games) > 0 else 0
                        home_points_allowed = home_games['visitor_team_score'].mean() if len(home_games) > 0 else 0
                        
                        away_points_scored = away_games['visitor_team_score'].mean() if len(away_games) > 0 else 0
                        away_points_allowed = away_games['home_team_score'].mean() if len(away_games) > 0 else 0
                        
                        games_played = len(home_games) + len(away_games)
                        ppg = (home_games['home_team_score'].sum() + away_games['visitor_team_score'].sum()) / games_played if games_played > 0 else 0
                        papg = (home_games['visitor_team_score'].sum() + away_games['home_team_score'].sum()) / games_played if games_played > 0 else 0
                        
                        # Display team card
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            # Display team logo (placeholder)
                            st.image("https://cdn.nba.com/logos/nba/nba-logoman-75.svg", width=150)
                        
                        with col2:
                            st.subheader(f"{selected_team} ({selected_season})")
                            st.write(f"**Record:** {total_wins}-{total_losses}")
                            st.write(f"**Points Per Game:** {ppg:.1f}")
                            st.write(f"**Points Allowed Per Game:** {papg:.1f}")
                            st.write(f"**Home Record:** {home_wins}-{home_losses}")
                            st.write(f"**Away Record:** {away_wins}-{away_losses}")
                    else:
                        st.warning(f"No game data available for {selected_team} in the {selected_season} season")
        else:
            st.warning("No team data available")

# Data Visualization page
elif choice == "Data Visualization":
    st.title("Team Data Visualization")
    
    # Get DataFrames
    teams_df = get_teams_dataframe()
    games_df = get_games_dataframe()
    
    if not teams_df.empty and not games_df.empty:
        # Team selection
        team_list = sorted(teams_df['full_name'].unique().tolist())
        selected_team = st.selectbox("Select Team", team_list)
        
        if selected_team:
            team_id = teams_df[teams_df['full_name'] == selected_team]['team_id'].iloc[0]
            
            # Get all seasons for this team
            home_games = games_df[games_df['home_team_id'] == team_id]
            away_games = games_df[games_df['visitor_team_id'] == team_id]
            all_seasons = sorted(pd.concat([home_games['season'], away_games['season']]).unique().tolist())
            
            if all_seasons:
                # Visualization type selection
                viz_type = st.selectbox(
                    "Select Visualization", 
                    ["Points Per Game vs Season", 
                     "Points Allowed Per Game vs Season", 
                     "Wins vs Season",
                     "Home Wins vs Season",
                     "Away Wins vs Season"]
                )
                
                # Calculate statistics for each season
                season_stats = []
                for season in all_seasons:
                    season_home_games = home_games[home_games['season'] == season]
                    season_away_games = away_games[away_games['season'] == season]
                    
                    # Calculate wins
                    home_wins = len(season_home_games[season_home_games['home_team_score'] > season_home_games['visitor_team_score']])
                    away_wins = len(season_away_games[season_away_games['visitor_team_score'] > season_away_games['home_team_score']])
                    total_wins = home_wins + away_wins
                    
                    # Calculate points
                    games_played = len(season_home_games) + len(season_away_games)
                    ppg = (season_home_games['home_team_score'].sum() + season_away_games['visitor_team_score'].sum()) / games_played if games_played > 0 else 0
                    papg = (season_home_games['visitor_team_score'].sum() + season_away_games['home_team_score'].sum()) / games_played if games_played > 0 else 0
                    
                    season_stats.append({
                        'season': season,
                        'ppg': ppg,
                        'papg': papg,
                        'wins': total_wins,
                        'home_wins': home_wins,
                        'away_wins': away_wins
                    })
                
                # Create DataFrame with stats
                stats_df = pd.DataFrame(season_stats)
                
                # Create visualization based on selection
                if not stats_df.empty:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    if viz_type == "Points Per Game vs Season":
                        ax.bar(stats_df['season'].astype(str), stats_df['ppg'], color='blue')
                        ax.set_ylabel('Points Per Game')
                        ax.set_title(f'{selected_team} - Points Per Game by Season')
                    
                    elif viz_type == "Points Allowed Per Game vs Season":
                        ax.bar(stats_df['season'].astype(str), stats_df['papg'], color='red')
                        ax.set_ylabel('Points Allowed Per Game')
                        ax.set_title(f'{selected_team} - Points Allowed Per Game by Season')
                    
                    elif viz_type == "Wins vs Season":
                        ax.bar(stats_df['season'].astype(str), stats_df['wins'], color='green')
                        ax.set_ylabel('Wins')
                        ax.set_title(f'{selected_team} - Wins by Season')
                    
                    elif viz_type == "Home Wins vs Season":
                        ax.bar(stats_df['season'].astype(str), stats_df['home_wins'], color='purple')
                        ax.set_ylabel('Home Wins')
                        ax.set_title(f'{selected_team} - Home Wins by Season')
                    
                    elif viz_type == "Away Wins vs Season":
                        ax.bar(stats_df['season'].astype(str), stats_df['away_wins'], color='orange')
                        ax.set_ylabel('Away Wins')
                        ax.set_title(f'{selected_team} - Away Wins by Season')
                    
                    ax.set_xlabel('Season')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    # Display the plot
                    st.pyplot(fig)
                    
                    # Display the data table
                    st.subheader("Data Table")
                    st.dataframe(stats_df)
            else:
                st.warning(f"No game data available for {selected_team}")
    else:
        st.warning("No team or game data available") 
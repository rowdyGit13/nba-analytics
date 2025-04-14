"""
Demo application to showcase the team colors and chart utilities.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

# Import our custom modules
from streamlit_app.team_colors import get_team_colors, get_team_logo, TEAM_COLORS, TEAM_LOGOS
from streamlit_app.chart_utils import (
    style_dataframe, 
    create_team_bar_chart, 
    create_team_line_chart,
    create_shot_chart,
    create_player_comparison_radar,
    create_bubble_chart
)

# Set page config
st.set_page_config(
    page_title="NBA Analytics Dashboard - Demo",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("NBA Analytics Dashboard - Demo")
st.markdown("This is a demonstration of the team colors and chart utilities for the NBA Analytics Dashboard.")

# Sidebar with team selection
st.sidebar.title("Team Selection")
selected_team = st.sidebar.selectbox(
    "Select a team",
    sorted(TEAM_COLORS.keys()),
    index=0
)

# Get team colors and logo
team_colors = get_team_colors(selected_team)
team_logo = get_team_logo(selected_team)

# Display team colors and logo
st.sidebar.subheader("Team Colors")
st.sidebar.markdown(f"**Primary:** {team_colors['primary']}")
st.sidebar.markdown(f"**Secondary:** {team_colors['secondary']}")
st.sidebar.markdown(f"**Tertiary:** {team_colors['tertiary']}")
st.sidebar.image(team_logo, width=150)

# Main content area
st.header(f"Visualization Demo for {selected_team}")

# Create tabs for different chart types
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Team Stats", 
    "Player Comparison", 
    "Shot Chart", 
    "League Comparison",
    "Styled Tables"
])

# Tab 1: Team Stats
with tab1:
    st.subheader("Team Performance Over Season")
    
    # Generate sample team stats data
    seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
    ppg = np.random.uniform(95, 120, 5).tolist()
    opp_ppg = np.random.uniform(95, 120, 5).tolist()
    
    # Create a DataFrame
    team_stats_df = pd.DataFrame({
        "Season": seasons,
        "PPG": ppg,
        "OPP_PPG": opp_ppg,
        "NET_RATING": [ppg[i] - opp_ppg[i] for i in range(5)]
    })
    
    # Create bar chart
    bar_chart = create_team_bar_chart(
        df=team_stats_df,
        x_col="Season",
        y_col="PPG",
        team_name=selected_team,
        title=f"{selected_team} Points Per Game"
    )
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Create line chart
    line_chart = create_team_line_chart(
        df=team_stats_df,
        x_col="Season",
        y_col="NET_RATING",
        team_name=selected_team,
        title=f"{selected_team} Net Rating"
    )
    st.altair_chart(line_chart, use_container_width=True)

# Tab 2: Player Comparison
with tab2:
    st.subheader("Player Comparison")
    
    # Sample player stats
    player1 = {
        "PTS": 25.3,
        "REB": 5.7,
        "AST": 7.9,
        "STL": 1.5,
        "BLK": 0.6,
        "FG%": 0.48,
        "3P%": 0.38
    }
    
    player2 = {
        "PTS": 20.6,
        "REB": 10.1,
        "AST": 3.2,
        "STL": 0.9,
        "BLK": 1.7,
        "FG%": 0.52,
        "3P%": 0.33
    }
    
    # Create player comparison radar chart
    radar_chart = create_player_comparison_radar(
        player1_stats=player1,
        player2_stats=player2,
        player1_name="Player A",
        player2_name="Player B"
    )
    st.pyplot(radar_chart)

# Tab 3: Shot Chart
with tab3:
    st.subheader("Shot Chart")
    
    # Generate sample shot data
    n_shots = 200
    made_shots = np.random.randint(0, 2, n_shots)
    
    # Create shot locations randomly
    x_coords = np.random.uniform(-250, 250, n_shots)
    y_coords = np.random.uniform(-50, 400, n_shots)
    
    # Create shot DataFrame
    shots_df = pd.DataFrame({
        "LOC_X": x_coords,
        "LOC_Y": y_coords,
        "SHOT_MADE_FLAG": made_shots
    })
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        made_only = st.checkbox("Show Made Shots Only", value=False)
    
    # Create shot chart
    shot_chart = create_shot_chart(
        shots_df=shots_df,
        team_name=selected_team,
        made_only=made_only,
        title=f"{selected_team} Shot Chart (Demo Data)"
    )
    st.pyplot(shot_chart)

# Tab 4: League Comparison
with tab4:
    st.subheader("League Comparison")
    
    # Generate sample league data for top teams
    teams = list(TEAM_COLORS.keys())[:10]
    ppg = np.random.uniform(100, 120, 10)
    opp_ppg = np.random.uniform(100, 120, 10)
    win_pct = np.random.uniform(0.4, 0.7, 10)
    
    # Create league comparison DataFrame
    league_df = pd.DataFrame({
        "Team": teams,
        "PPG": ppg,
        "OPP_PPG": opp_ppg,
        "WIN_PCT": win_pct,
        "NET_RTG": ppg - opp_ppg
    })
    
    # Create bubble chart
    bubble_chart = create_bubble_chart(
        df=league_df,
        x_col="PPG",
        y_col="OPP_PPG",
        size_col="WIN_PCT",
        team_col="Team",
        title="Team Offensive vs Defensive Rating"
    )
    st.altair_chart(bubble_chart, use_container_width=True)

# Tab 5: Styled Tables
with tab5:
    st.subheader("Styled Tables")
    
    # Create sample player stats
    players = ["Player A", "Player B", "Player C", "Player D", "Player E"]
    stats = {
        "Player": players,
        "PPG": np.random.uniform(10, 30, 5),
        "RPG": np.random.uniform(3, 12, 5),
        "APG": np.random.uniform(2, 10, 5),
        "FG_PCT": np.random.uniform(0.4, 0.6, 5),
        "3PT_PCT": np.random.uniform(0.3, 0.45, 5),
        "FT_PCT": np.random.uniform(0.7, 0.95, 5),
    }
    
    player_stats_df = pd.DataFrame(stats)
    
    # Display styled dataframe
    st.dataframe(
        style_dataframe(player_stats_df, selected_team),
        use_container_width=True
    )
    
    # Team stats table
    st.subheader("Team Stats")
    team_full_stats = pd.DataFrame({
        "Stat": ["Points Per Game", "Rebounds Per Game", "Assists Per Game", 
                "Steals Per Game", "Blocks Per Game", "Turnovers Per Game",
                "FG Percentage", "3PT Percentage", "FT Percentage"],
        "Value": np.random.uniform(80, 120, 9),
        "League Rank": np.random.randint(1, 31, 9),
        "League Average": np.random.uniform(75, 115, 9)
    })
    
    st.dataframe(
        style_dataframe(team_full_stats, selected_team),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("Demo created for NBA Analytics Dashboard") 
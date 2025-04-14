"""
Chart Utility Functions for NBA Analytics Dashboard

This module provides functions for creating and styling charts and tables
for the NBA Analytics Dashboard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import streamlit as st
from typing import List, Dict, Any, Optional, Union, Tuple

# Import team colors
try:
    from team_colors import get_team_colors, get_team_logo
except ImportError:
    try:
        from streamlit_app.team_colors import get_team_colors, get_team_logo
    except ImportError:
        # Last resort fallback
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from streamlit_app.team_colors import get_team_colors, get_team_logo

# Set up the styling
plt.style.use('ggplot')
sns.set(style="whitegrid")

def style_dataframe(df: pd.DataFrame, team_name: Optional[str] = None) -> pd.DataFrame:
    """
    Apply styling to a dataframe based on team colors if provided.
    
    Args:
        df (pd.DataFrame): DataFrame to style
        team_name (str, optional): NBA team name to use for styling
        
    Returns:
        pd.DataFrame: Styled DataFrame
    """
    # Get team colors if team_name is provided, otherwise use default NBA colors
    colors = get_team_colors(team_name) if team_name else {'primary': '#17408B', 'secondary': '#C9082A', 'tertiary': '#FFFFFF'}
    
    # Create a styled dataframe
    styled_df = df.style.set_properties(**{
        'background-color': colors['tertiary'],
        'color': '#333333',
        'border-color': colors['secondary'],
        'border': '1px solid'
    })
    
    # Style the header
    styled_df = styled_df.set_table_styles([{
        'selector': 'th',
        'props': [
            ('background-color', colors['primary']),
            ('color', colors['tertiary']),
            ('font-weight', 'bold'),
            ('text-align', 'center'),
            ('border', f'1px solid {colors["secondary"]}')
        ]
    }])
    
    # Add hover effect and other details
    styled_df = styled_df.set_table_styles([
        {'selector': 'tr:hover', 'props': [('background-color', f'{colors["secondary"]}25')]},
        {'selector': 'td', 'props': [('text-align', 'center'), ('padding', '8px')]},
    ], overwrite=False)
    
    # Format numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        if 'pct' in col.lower() or 'percentage' in col.lower():
            styled_df = styled_df.format({col: '{:.1%}'})
        elif 'ratio' in col.lower():
            styled_df = styled_df.format({col: '{:.2f}'})
        else:
            styled_df = styled_df.format({col: '{:.1f}'})
    
    return styled_df

def create_team_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, team_name: str, title: str) -> alt.Chart:
    """
    Create a bar chart for team data with team colors.
    
    Args:
        df (pd.DataFrame): DataFrame with the data
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        team_name (str): Team name for colors
        title (str): Chart title
        
    Returns:
        alt.Chart: Altair chart object
    """
    # Get team colors
    colors = get_team_colors(team_name)
    
    # Create the chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
        y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
        color=alt.value(colors['primary']),
        tooltip=[x_col, y_col]
    ).properties(
        title=title,
        width=600,
        height=400
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='start',
        color=colors['primary']
    ).configure_axis(
        grid=True,
        gridColor='#EEEEEE',
        labelFontSize=12,
        titleFontSize=14
    )
    
    return chart

def create_team_line_chart(df: pd.DataFrame, x_col: str, y_col: str, team_name: str, title: str) -> alt.Chart:
    """
    Create a line chart for team data with team colors.
    
    Args:
        df (pd.DataFrame): DataFrame with the data
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        team_name (str): Team name for colors
        title (str): Chart title
        
    Returns:
        alt.Chart: Altair chart object
    """
    # Get team colors
    colors = get_team_colors(team_name)
    
    # Create the chart
    chart = alt.Chart(df).mark_line(
        point=True,
        strokeWidth=3,
        opacity=0.8
    ).encode(
        x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
        y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
        color=alt.value(colors['primary']),
        tooltip=[x_col, y_col]
    ).properties(
        title=title,
        width=600,
        height=400
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='start',
        color=colors['primary']
    ).configure_axis(
        grid=True,
        gridColor='#EEEEEE',
        labelFontSize=12,
        titleFontSize=14
    )
    
    return chart

def create_shot_chart(shots_df: pd.DataFrame, team_name: Optional[str] = None, 
                      made_only: bool = False, title: str = "Shot Chart") -> plt.Figure:
    """
    Create a shot chart visualization using team colors.
    
    Args:
        shots_df (pd.DataFrame): DataFrame with shot data (must have columns: 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG')
        team_name (str, optional): Team name for colors
        made_only (bool): Whether to show only made shots
        title (str): Chart title
        
    Returns:
        plt.Figure: Matplotlib figure object
    """
    # Get team colors
    colors = get_team_colors(team_name) if team_name else {'primary': '#17408B', 'secondary': '#C9082A', 'tertiary': '#FFFFFF'}
    
    # Filter shots if needed
    if made_only:
        shots_df = shots_df[shots_df['SHOT_MADE_FLAG'] == 1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 11))
    
    # Draw court
    draw_court(ax, color=colors['primary'])
    
    # Plot shots
    made_shots = shots_df[shots_df['SHOT_MADE_FLAG'] == 1]
    missed_shots = shots_df[shots_df['SHOT_MADE_FLAG'] == 0]
    
    # Plot made shots
    ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'], 
              c=colors['primary'], marker='o', s=30, alpha=0.7, 
              label='Made Shot')
    
    # Plot missed shots if not filtered
    if not made_only:
        ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'], 
                  c=colors['secondary'], marker='x', s=30, alpha=0.7,
                  label='Missed Shot')
    
    # Set title, limits, and legend
    ax.set_title(title, fontsize=18, color=colors['primary'])
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 470)
    ax.legend(loc='upper right')
    
    return fig

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    """
    Draw a basketball court on the given axis with the specified color.
    
    Args:
        ax (matplotlib.axes.Axes): The axis to draw on
        color (str): The color of the court lines
        lw (float): Line width
        outer_lines (bool): Whether to draw outer court boundaries
        
    Returns:
        matplotlib.axes.Axes: The axis with the court drawn
    """
    if ax is None:
        ax = plt.gca()
    
    # Create the basketball hoop
    hoop = plt.Circle((0, 0), 7.5, facecolor='none', edgecolor=color, linewidth=lw)
    
    # Create backboard
    backboard = plt.Rectangle((-30, -7.5), 60, 0, linewidth=lw, edgecolor=color)
    
    # The paint
    outer_box = plt.Rectangle((-80, -47.5), 160, 190, linewidth=lw, facecolor='none', edgecolor=color)
    inner_box = plt.Rectangle((-60, -47.5), 120, 190, linewidth=lw, facecolor='none', edgecolor=color)
    
    # Free throw top arc
    top_free_throw = plt.Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, facecolor='none', edgecolor=color)
    
    # Free throw bottom arc
    bottom_free_throw = plt.Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, facecolor='none', edgecolor=color, linestyle='dashed')
    
    # Restricted zone
    restricted = plt.Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, facecolor='none', edgecolor=color)
    
    # Three point line
    corner_three_a = plt.Rectangle((-220, -47.5), 0, 140, linewidth=lw, facecolor='none', edgecolor=color)
    corner_three_b = plt.Rectangle((220, -47.5), 0, 140, linewidth=lw, facecolor='none', edgecolor=color)
    three_arc = plt.Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, facecolor='none', edgecolor=color)
    
    # Center Court
    center_outer_arc = plt.Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, facecolor='none', edgecolor=color)
    center_inner_arc = plt.Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, facecolor='none', edgecolor=color)
    
    # Add the court elements to the plot
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, 
                     bottom_free_throw, restricted, corner_three_a, 
                     corner_three_b, three_arc, center_outer_arc, 
                     center_inner_arc]
    
    for element in court_elements:
        ax.add_patch(element)
    
    # Add outer lines if specified
    if outer_lines:
        outer_court = plt.Rectangle((-250, -47.5), 500, 470, linewidth=lw, facecolor='none', edgecolor=color)
        ax.add_patch(outer_court)
    
    # Remove axis ticks and labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 470)
    
    return ax

def create_player_comparison_radar(player1_stats: Dict[str, float], player2_stats: Dict[str, float], 
                                  player1_name: str, player2_name: str) -> plt.Figure:
    """
    Create a radar chart comparing two players.
    
    Args:
        player1_stats (Dict[str, float]): Dictionary of stats for player 1
        player2_stats (Dict[str, float]): Dictionary of stats for player 2
        player1_name (str): Name of player 1
        player2_name (str): Name of player 2
        
    Returns:
        plt.Figure: Matplotlib figure object
    """
    # Get categories (stat names) and create a figure
    categories = list(player1_stats.keys())
    N = len(categories)
    
    # Create angle for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Create a figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Add player 1 stats
    values1 = list(player1_stats.values())
    values1 += values1[:1]  # Close the loop
    ax.plot(angles, values1, linewidth=2, linestyle='solid', label=player1_name, color='#1D428A')
    ax.fill(angles, values1, alpha=0.1, color='#1D428A')
    
    # Add player 2 stats
    values2 = list(player2_stats.values())
    values2 += values2[:1]  # Close the loop
    ax.plot(angles, values2, linewidth=2, linestyle='solid', label=player2_name, color='#CE1141')
    ax.fill(angles, values2, alpha=0.1, color='#CE1141')
    
    # Set category labels
    plt.xticks(angles[:-1], categories, fontsize=12)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    return fig

def create_bubble_chart(df: pd.DataFrame, x_col: str, y_col: str, size_col: str, 
                       team_col: str, title: str) -> alt.Chart:
    """
    Create a bubble chart with team colors.
    
    Args:
        df (pd.DataFrame): DataFrame with the data
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        size_col (str): Column for bubble size
        team_col (str): Column with team names
        title (str): Chart title
        
    Returns:
        alt.Chart: Altair chart object
    """
    # Create a copy of the dataframe and add color information
    plot_df = df.copy()
    
    # Create the chart
    chart = alt.Chart(plot_df).mark_circle(opacity=0.7).encode(
        x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
        y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
        size=alt.Size(size_col, title=size_col.replace('_', ' ').title()),
        color=alt.Color(team_col, title='Team'),
        tooltip=[team_col, x_col, y_col, size_col]
    ).properties(
        title=title,
        width=700,
        height=500
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='start',
        color='black'
    )
    
    return chart 
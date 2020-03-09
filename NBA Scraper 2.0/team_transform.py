#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:48:32 2020

@author: ahelgeso
"""

def team_transform(df):
    
    import pandas as pd
    import numpy as np
    
    '''
    1. create an empty running dataframe for everything
    2. start a for loop for each team
    3. create a team index of the current year dataframe where only 
        active team is in the dataframe
    4. create an empty running dataframe for the current team
    5. define the necessary columns for the running dataframe
    6. loop through the team-indexed df based on if the team
        appears in the 'home_team' or 'away_team' columns
    7. add the team running dataframe to the everything 
        running dataframe
    8. reset index and return
    '''
    
    all_teams = pd.DataFrame()
    
    TEAM_ABBREVS = {
    'Cleveland Cavaliers': 'CLE',
    'Boston Celtics':'BOS',
    'Washington Wizards':'WAS',
    'Charlotte Hornets':'CHO',
    'Minnesota Timberwolves':'MIN',
    'Dallas Mavericks':'DAL',
    'Milwaukee Bucks':'MIL',
    'Philadelphia 76ers':'PHI',
    'Phoenix Suns':'PHO',
    'Los Angeles Lakers':'LAL',
    'Utah Jazz':'UTA',
    'Sacramento Kings':'SAC',
    'New York Knicks':'NYK',
    'New Orleans Pelicans':'NOP',
    'Detroit Pistons':'DET',
    'Atlanta Hawks':'ATL',
    'Chicago Bulls':'CHI',
    'Miami Heat':'MIA',
    'Memphis Grizzlies':'MEM',
    'Golden State Warriors':'GSW',
    'Denver Nuggets':'DEN',
    'Brooklyn Nets':'BRK',
    'Los Angeles Clippers':'LAC',
    'Portland Trail Blazers':'POR',
    'Indiana Pacers':'IND',
    'San Antonio Spurs':'SAS',
    'Houston Rockets':'HOU',
    'Oklahoma City Thunder':'OKC',
    'Toronto Raptors':'TOR',
    'Orlando Magic':'ORL'
    }
    
    TEAMS = TEAM_ABBREVS.values()
    
    for team in TEAMS:
        
        # Grab the df only when the team of interest is playing
        rundf = df[np.logical_or(df['home_team']==team, df['away_team']==team)].copy()
        
        # Define team column
        rundf['team'] = team
        
        # Define home and away indicies
        idx_team_home = rundf[rundf['home_team']==team].index
        idx_team_away = rundf[rundf['away_team']==team].index
        
        # Define opponent column and home game column based on 
        # home / away indices
        rundf.loc[idx_team_home, 'opponent'] = rundf.loc[idx_team_home, 'away_team']
        rundf.loc[idx_team_away, 'opponent'] = rundf.loc[idx_team_away, 'home_team']
        rundf.loc[idx_team_home, 'home_game'] = 1
        rundf.loc[idx_team_away, 'home_game'] = 0
        
        ### Setting team quarter scores when team is home and away ###
        
        rundf.loc[idx_team_home, 'team_q1'] = rundf.loc[idx_team_home, 'home_q1']
        rundf.loc[idx_team_away, 'team_q1'] = rundf.loc[idx_team_away, 'away_q1']
        
        rundf.loc[idx_team_home, 'team_q2'] = rundf.loc[idx_team_home, 'home_q2']
        rundf.loc[idx_team_away, 'team_q2'] = rundf.loc[idx_team_away, 'away_q2']
        
        rundf.loc[idx_team_home, 'team_q3'] = rundf.loc[idx_team_home, 'home_q3']
        rundf.loc[idx_team_away, 'team_q4'] = rundf.loc[idx_team_away, 'away_q4']
        
        rundf.loc[idx_team_home, 'team_OT'] = rundf.loc[idx_team_home, 'home_OT']
        rundf.loc[idx_team_away, 'team_OT'] = rundf.loc[idx_team_away, 'away_OT']
        
        rundf.loc[idx_team_home, 'team_final'] = rundf.loc[idx_team_home, 'home_final']
        rundf.loc[idx_team_away, 'team_final'] = rundf.loc[idx_team_away, 'away_final']
        
        ### Setting opponent quarter scores when team is home and away ###
        
        rundf.loc[idx_team_home, 'opponent_q1'] = rundf.loc[idx_team_home, 'away_q1']
        rundf.loc[idx_team_away, 'opponent_q1'] = rundf.loc[idx_team_away, 'home_q1']

        rundf.loc[idx_team_home, 'opponent_q2'] = rundf.loc[idx_team_home, 'away_q2']
        rundf.loc[idx_team_away, 'opponent_q2'] = rundf.loc[idx_team_away, 'home_q2']

        rundf.loc[idx_team_home, 'opponent_q3'] = rundf.loc[idx_team_home, 'away_q3']
        rundf.loc[idx_team_away, 'opponent_q3'] = rundf.loc[idx_team_away, 'home_q3']

        rundf.loc[idx_team_home, 'opponent_q4'] = rundf.loc[idx_team_home, 'away_q4']
        rundf.loc[idx_team_away, 'opponent_q4'] = rundf.loc[idx_team_away, 'home_q4']

        rundf.loc[idx_team_home, 'opponent_OT'] = rundf.loc[idx_team_home, 'away_OT']
        rundf.loc[idx_team_away, 'opponent_OT'] = rundf.loc[idx_team_away, 'home_OT']

        rundf.loc[idx_team_home, 'opponent_final'] = rundf.loc[idx_team_home, 'away_final']
        rundf.loc[idx_team_away, 'opponent_final'] = rundf.loc[idx_team_away, 'home_final']

        cols_to_drop = ['away_q1',
                         'away_q2',
                         'away_q3',
                         'away_q4',
                         'away_OT',
                         'away_final',
                         'home_q1',
                         'home_q2',
                         'home_q3',
                         'home_q4',
                         'home_OT',
                         'home_final']
        
        rundf.drop(cols_to_drop, axis=1, inplace=True)
        all_teams.append(rundf)
        
    return all_teams








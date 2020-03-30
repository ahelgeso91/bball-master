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
    
    TEAMS = list(TEAM_ABBREVS.values())
    
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
        rundf.loc[idx_team_away, 'team_q3'] = rundf.loc[idx_team_away, 'away_q3']

        rundf.loc[idx_team_home, 'team_q4'] = rundf.loc[idx_team_home, 'home_q4']
        rundf.loc[idx_team_away, 'team_q4'] = rundf.loc[idx_team_away, 'away_q4']
        
        rundf.loc[idx_team_home, 'team_OT'] = rundf.loc[idx_team_home, 'home_OT']
        rundf.loc[idx_team_away, 'team_OT'] = rundf.loc[idx_team_away, 'away_OT']
        
        rundf.loc[idx_team_home, 'team_final'] = rundf.loc[idx_team_home, 'home_final']
        rundf.loc[idx_team_away, 'team_final'] = rundf.loc[idx_team_away, 'away_final']
        
        rundf.loc[idx_team_home, 'team_pace'] = rundf.loc[idx_team_home, 'home_pace']
        rundf.loc[idx_team_away, 'team_pace'] = rundf.loc[idx_team_away, 'away_pace']
        
        rundf.loc[idx_team_home, 'team_efg'] = rundf.loc[idx_team_home, 'home_efg']*100.0
        rundf.loc[idx_team_away, 'team_efg'] = rundf.loc[idx_team_away, 'away_efg']*100.0
        
        rundf.loc[idx_team_home, 'team_tov'] = rundf.loc[idx_team_home, 'home_tov']
        rundf.loc[idx_team_away, 'team_tov'] = rundf.loc[idx_team_away, 'away_tov']
        
        rundf.loc[idx_team_home, 'team_orb'] = rundf.loc[idx_team_home, 'home_orb']
        rundf.loc[idx_team_away, 'team_orb'] = rundf.loc[idx_team_away, 'away_orb']
        
        rundf.loc[idx_team_home, 'team_ftr'] = rundf.loc[idx_team_home, 'home_ftr']*100.0
        rundf.loc[idx_team_away, 'team_ftr'] = rundf.loc[idx_team_away, 'away_ftr']*100.0
        
        rundf.loc[idx_team_home, 'team_ortg'] = rundf.loc[idx_team_home, 'home_ortg']
        rundf.loc[idx_team_away, 'team_ortg'] = rundf.loc[idx_team_away, 'away_ortg']
        
        rundf.loc[idx_team_home, 'team_drtg'] = rundf.loc[idx_team_home, 'home_drtg']
        rundf.loc[idx_team_away, 'team_drtg'] = rundf.loc[idx_team_away, 'away_drtg']
        
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
        
        rundf.loc[idx_team_home, 'opponent_pace'] = rundf.loc[idx_team_home, 'away_pace']
        rundf.loc[idx_team_away, 'opponent_pace'] = rundf.loc[idx_team_away, 'home_pace']
        
        rundf.loc[idx_team_home, 'opponent_efg'] = rundf.loc[idx_team_home, 'away_efg']*100.0
        rundf.loc[idx_team_away, 'opponent_efg'] = rundf.loc[idx_team_away, 'home_efg']*100.0
        
        rundf.loc[idx_team_home, 'opponent_tov'] = rundf.loc[idx_team_home, 'away_tov']
        rundf.loc[idx_team_away, 'opponent_tov'] = rundf.loc[idx_team_away, 'home_tov']
        
        rundf.loc[idx_team_home, 'opponent_orb'] = rundf.loc[idx_team_home, 'away_orb']
        rundf.loc[idx_team_away, 'opponent_orb'] = rundf.loc[idx_team_away, 'home_orb']
        
        rundf.loc[idx_team_home, 'opponent_ftr'] = rundf.loc[idx_team_home, 'away_ftr']*100.0
        rundf.loc[idx_team_away, 'opponent_ftr'] = rundf.loc[idx_team_away, 'home_ftr']*100.0
        
        rundf.loc[idx_team_home, 'opponent_ortg'] = rundf.loc[idx_team_home, 'away_ortg']
        rundf.loc[idx_team_away, 'opponent_ortg'] = rundf.loc[idx_team_away, 'home_ortg']
        
        rundf.loc[idx_team_home, 'opponent_drtg'] = rundf.loc[idx_team_home, 'away_drtg']
        rundf.loc[idx_team_away, 'opponent_drtg'] = rundf.loc[idx_team_away, 'home_drtg']

        rundf['date'] = pd.to_datetime(rundf['date'])

        rundf.sort_values(by = 'date', inplace=True)
        
        rundf['rest'] = rundf['date'].diff().dt.days - 1
        
        rundf['b2b'] = rundf['rest'].apply(lambda x: 1 if x==0 else 0)
        rundf['q1_margin'] = rundf['team_q1'] - rundf['opponent_q1']
        rundf['h1_margin'] = (rundf['team_q1'] + rundf['team_q2']) - (rundf['opponent_q1'] + rundf['opponent_q2'])
        rundf['margin'] = rundf['team_final'] - rundf['opponent_final']
        
        rundf['seven_game_pace'] = rundf['team_pace'].rolling(7).mean().shift(1)
        rundf['seven_game_efg'] = rundf['team_efg'].rolling(7).mean().shift(1)
        rundf['seven_game_tov'] = rundf['team_tov'].rolling(7).mean().shift(1)
        rundf['seven_game_orb'] = rundf['team_orb'].rolling(7).mean().shift(1)
        rundf['seven_game_ftr'] = rundf['team_ftr'].rolling(7).mean().shift(1)
        rundf['seven_game_ortg'] = rundf['team_ortg'].rolling(7).mean().shift(1)
        rundf['seven_game_drtg'] = rundf['team_drtg'].rolling(7).mean().shift(1)
        
        cols_to_drop = ['away_team', 
                        'away_q1', 'away_q2', 
                        'away_q3', 'away_q4', 
                        'away_OT', 'away_final', 
                        'home_team', 'home_q1', 
                        'home_q2', 'home_q3', 
                        'home_q4', 'home_OT',
                        'home_final', 
                        'away_pace', 
                        'away_efg', 'away_tov',
                        'away_orb', 'away_ftr',
                        'away_ortg', 'away_drtg',
                        'home_pace', 'home_efg',
                        'home_tov', 'home_orb',
                        'home_ftr', 'home_ortg', 
                        'home_drtg']
        
        rundf.drop(cols_to_drop, axis=1, inplace=True)
        all_teams = all_teams.append(rundf)
        
    return all_teams.reset_index(drop=True)

def opponent_align(df):
    import pandas as pd
    import numpy as np
    
    opponent_seven_game_efg = []
    opponent_seven_game_tov = []
    opponent_seven_game_orb = []
    opponent_seven_game_ftr = []
    opponent_seven_game_pace = []
    opponent_seven_game_ortg = []
    opponent_seven_game_drtg = []
    opponent_rest = []
    opponent_b2b= []
    
    for i in range(len(df)):
        team = df['team'].iloc[i]
        date = df['date'].iloc[i]
        correspond_row = df[np.logical_and(df['date']==date, df['opponent']==team)]
        
        opponent_seven_game_efg.append(correspond_row['seven_game_efg'].iloc[0])
        opponent_seven_game_tov.append(correspond_row['seven_game_tov'].iloc[0])
        opponent_seven_game_orb.append(correspond_row['seven_game_orb'].iloc[0])
        opponent_seven_game_ftr.append(correspond_row['seven_game_ftr'].iloc[0])
        opponent_seven_game_pace.append(correspond_row['seven_game_pace'].iloc[0])
        opponent_seven_game_ortg.append(correspond_row['seven_game_ortg'].iloc[0])
        opponent_seven_game_drtg.append(correspond_row['seven_game_drtg'].iloc[0])
        opponent_rest.append(correspond_row['rest'].iloc[0])
        opponent_b2b.append(correspond_row['b2b'].iloc[0])
        
    dct = {
        'opponent_seven_game_efg':opponent_seven_game_efg,
        'opponent_seven_game_tov':opponent_seven_game_tov,
        'opponent_seven_game_orb':opponent_seven_game_ortg,
        'opponent_seven_game_ftr':opponent_seven_game_ftr,
        'opponent_seven_game_pace':opponent_seven_game_pace,
        'opponent_seven_game_ortg':opponent_seven_game_ortg,
        'opponent_seven_game_drtg':opponent_seven_game_drtg,
        'opponent_rest':opponent_rest,
        'opponent_b2b':opponent_b2b
        }
    
    return pd.concat([df, pd.DataFrame(dct)], axis=1)


# def line_align(df):
#     for i in range(len(df)):
#         team = df['team'].iloc[i]
#         date = df['date'].iloc[i]
#         correspond_row = nba20_lines[np.logical_and(nba20_lines['team']==team, nba20_lines['date']==date)]
#         if correspond_row['line'].empty:
#             pass
#         else:
#             df.loc[i, 'line'] = correspond_row['line'].iloc[0]
#     return df



if __name__ == '__main__':
    import tkinter as tk
    from tkinter import filedialog
    import pandas as pd
    
    #Dialog window to select correct file
    root=tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    df = pd.read_csv(file_path)
    df = team_transform(df)
    df = opponent_align(df)






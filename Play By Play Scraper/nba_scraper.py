# -*- coding: utf-8 -*-
"""

"""

def get_results(year, teams=[]):
    '''Takes in a year (int >=2015) and a list of teams (one team still needs to be in list
    form) and returns a pandas dataframe including:
        game date
        home team
        away team
        home and away results by quarter
        final score
        
        Required imports: 
            from datetime import datetime
            from datetime import timedelta
            from dateutil.relativedelta import relativedelta
            import requests, bs4
            import pandas as pd
            import sys
        '''
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import pandas as pd

    team_abbrevs = {
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
    
    # team will be a list
    # year will be an int
    
    # If no team is input, scrape for all teams
    # Need to have a switch for if scraping current season or not
    # First: Generate list of Game Log URLs
    
    if teams == []:
        teams = team_abbrevs.values()
    
    df = pd.DataFrame()
    
    for team in teams:
        running_df = pd.DataFrame()
        
        try:
            print(f'\nGathering URLs for {team}')
            game_links = get_urls(year, team)
        except:
            print(f'Error with game links for {team}')
        
        try:
            print('Getting game dates')
            game_dates = get_dates(game_links)
        except:
            print(f'Error with game dates for {team}')
            
        try:
            print('Calculating rest days')
            rest = calc_rest_days(game_dates)
        except:
            print(f'Error with rest days')
            
        if year == (datetime.today()+relativedelta(months=+2)).year:
            new_links = current_season_switch(rest,game_links)
            game_links = new_links
        print(f'Games Played: {len(game_links)}')
        
        try:
            print(f'Gathering line scores for {team}...')
            game_box_scores = get_line_scores(game_links)
        except:
            print(f'Error gathering line scores for {team}')

        running_df = pd.concat([rest, game_box_scores], axis = 1, ignore_index = True)
        df = df.append(running_df)
        
    columns = ['date','rest_days','away_team','away_q1','away_q2','away_q3','away_q4','away_OT','away_final',
              'home_team','home_q1','home_q2','home_q3','home_q4','home_OT','home_final']
    
    df.columns = columns
    return df


def get_urls(year, team):
    
    import requests, bs4
    
    # Team is a string, year is an int
    # Need a switch for current season
    
    # First page to start looking for games

    team_page = f'https://www.basketball-reference.com/teams/{team}/{year}_games.html'
    res = requests.get(team_page)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get just regular season games
    reg_season = soup.find('table',{'id':'games'})
    
    # Initialize list
    links = []
    
    # Compile URLs and add to list
    for entry in reg_season.find_all(attrs={'data-stat':'box_score_text'}):
        for link in entry.find_all('a'):
            links.append(link.get('href'))
    
    return links

def get_dates(links):
    
    from datetime import datetime
    from datetime import timedelta
    import pandas as pd
    
    dates = []
    for link in links:
            
        date = datetime.strptime(link[11:19], '%Y%m%d')
        dates.append(date)
            

    dates_db = pd.DataFrame({'date':dates})
    dates_db = dates_db[dates_db<(datetime.today()+timedelta(days=-1))].dropna()
    return dates_db

def current_season_switch(dates, links):
    links = links[0:len(dates)]
    return links

def calc_rest_days(dates_db):
    
    import pandas as pd
    from datetime import datetime
    from datetime import timedelta
    
    rest = [10]
    
    for i, date in enumerate(dates_db['date'].iloc[1:]):
        rest_day = int((date - dates_db['date'].iloc[i]).days)
        rest.append(rest_day)
        
    return pd.concat([dates_db, pd.DataFrame({'rest_days':rest})], axis = 1,
                      ignore_index = True)

def get_line_scores(urls):
    import pandas as pd
    import sys
    import requests, bs4
    import re
    
    # List of urls
    # This will be called immediately after the team URLs were scraped
    # Only will collect one OT period score just bc that will get out of hand
    # Box score output should always be the same structure:
        # Away Team
        # Away Q1
        # Away Q2
        # Away Q3
        # Away Q4
        # Away OT (IF OT)
        # Away Final
        # Home Team
        # Home Q1
        # Home Q2
        # Home Q3
        # Home Q4
        # Home OT (IF OT)
        # Home Final
    
    away = []
    away_q1 = []
    away_q2 = []
    away_q3 = []
    away_q4 = []
    away_OT = []
    away_final = []
    home = []
    home_q1 = []
    home_q2 = []
    home_q3 = []
    home_q4 = []
    home_OT = []
    home_final = []
    
    all_lists = [away, away_q1, away_q2, away_q3, away_q4, away_OT, away_final,
               home, home_q1, home_q2, home_q3, home_q4, home_OT, home_final]
    
    for i, url in enumerate(urls):
        sys.stdout.write(f'\rGame Number: {i+1}')
        sys.stdout.flush()
        current_game = f'https://www.basketball-reference.com{url}'
        res = requests.get(current_game, 'html_parser')
        res.raise_for_status()
        soup = bs4.BeautifulSoup(re.sub("<!--|-->", "", res.text), 'lxml')

        line_score = soup.find('table',{'id':'line_score'})
        df = pd.read_html(str(line_score),flavor='bs4')[0]

        if 'OT' in df['Scoring'].columns:
            away.append(df['Unnamed: 0_level_0']['Unnamed: 0_level_1'].iloc[0])
            home.append(df['Unnamed: 0_level_0']['Unnamed: 0_level_1'].iloc[1])
            away_q1.append(df['Scoring']['1'].iloc[0])
            away_q2.append(df['Scoring']['2'].iloc[0])
            away_q3.append(df['Scoring']['3'].iloc[0])
            away_q4.append(df['Scoring']['4'].iloc[0])
            away_OT.append(df['Scoring']['OT'].iloc[0])
            away_final.append(df['Scoring']['T'].iloc[0])
            home_q1.append(df['Scoring']['1'].iloc[1])
            home_q2.append(df['Scoring']['2'].iloc[1])
            home_q3.append(df['Scoring']['3'].iloc[1])
            home_q4.append(df['Scoring']['4'].iloc[1])
            home_OT.append(df['Scoring']['OT'].iloc[1])
            home_final.append(df['Scoring']['T'].iloc[1])

        else:
            away.append(df['Unnamed: 0_level_0']['Unnamed: 0_level_1'].iloc[0])
            home.append(df['Unnamed: 0_level_0']['Unnamed: 0_level_1'].iloc[1])
            away_q1.append(df['Scoring']['1'].iloc[0])
            away_q2.append(df['Scoring']['2'].iloc[0])
            away_q3.append(df['Scoring']['3'].iloc[0])
            away_q4.append(df['Scoring']['4'].iloc[0])
            away_OT.append(0)
            away_final.append(df['Scoring']['T'].iloc[0])
            home_q1.append(df['Scoring']['1'].iloc[1])
            home_q2.append(df['Scoring']['2'].iloc[1])
            home_q3.append(df['Scoring']['3'].iloc[1])
            home_q4.append(df['Scoring']['4'].iloc[1])
            home_OT.append(0)
            home_final.append(df['Scoring']['T'].iloc[1])



    line_score_dict = {
        'away_team':away,
        'away_q1':away_q1,
        'away_q2':away_q2,
        'away_q3':away_q3,
        'away_q4':away_q4,
        'away_OT':away_OT,
        'away_final':away_final,
        'home_team':home,
        'home_q1':home_q1,
        'home_q2':home_q2,
        'home_q3':home_q3,
        'home_q4':home_q4,
        'home_OT':home_OT,
        'home_final':home_final
    }
    
    
    return pd.DataFrame(line_score_dict)
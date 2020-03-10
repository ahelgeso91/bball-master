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
    # First: Generate list of Game Log URLs
    
    if teams == []:
        teams = team_abbrevs.values()
    
    df = pd.DataFrame()
    league_links = []
    
    for team in teams:
        
        try:
            print(f'Gathering URLs for {team}')
            game_links = get_urls(year, team)
            league_links.extend(game_links)
        except:
            print(f'Error with game links for {team}')
    
    # This line deletes duplicates from the list (PHI plays BOS 
    # and BOS plays PHI would be scraped twice)
    league_links = list(set(league_links))
    
    # Extract dates from the common link structure
    try:
        print('Getting game dates')
        game_dates = get_dates(league_links)
    except:
        print(f'Error with game dates function')
    
    # If this is the first time building the current season,
    # only scrape up until today's date
        
    if year == (datetime.today()+relativedelta(months=+2)).year:
        new_links = current_season_switch(game_dates,league_links)
        league_links = new_links
        

    print(f'Total Games To Scrape: {len(league_links)}')
    # Now we go get the line scores with the link list
    try:
        print(f'Gathering line scores...')
        game_box_scores = get_line_scores(league_links)
    except:
        print(f'Error gathering line scores')
    
    # We concat the dates and the line scores data, then label
    # the columns and return the data
        
    df = pd.concat([game_dates.reset_index(drop=True), game_box_scores],
                    axis = 1, ignore_index = True)

    columns = ['date','away_team','away_q1','away_q2','away_q3','away_q4','away_OT','away_final',
              'home_team','home_q1','home_q2','home_q3','home_q4','home_OT','home_final']
    
    df.columns = columns
    return df


def get_urls(year, team):
    
    '''Takes in year as an integer and team as a 3-character string, which is their
    abbreviation per basketball-reference.com.
    '''
    import requests, bs4
    
    # Team is a string, year is an int
    # Need a switch for current season
    
    # Find all the games the team played:

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

def get_dates(links, last_date_scraped = None):
    
    '''Returns pandas dataframe of dates that a team plays games, or of 
    dates needed to scrape if passing in a last date scraped, to indicate
    an in season update.'''
    
    from datetime import datetime
    from datetime import timedelta
    import pandas as pd
    
    ### Get all dates right off the bat
    dates = []
    for link in links:
            
        date = datetime.strptime(link[11:19], '%Y%m%d')
        dates.append(date)
    
    ### If this is an in season update, figure out the range of dates you
    ### still need scraped. Then, take the intersection of days since last 
    ### update and the dates available. Finally, filter out today.
        
    if last_date_scraped:
        delta = datetime.today() - last_date_scraped
        days = []
        for i in range(delta.days + 1):
            day = last_date_scraped + timedelta(days=i)
            days.append(day)
        dates_to_scrape = list(set(dates).intersection(set(days)))
        dates_db = pd.DataFrame({'date':dates_to_scrape})
        dates_db = dates_db[dates_db<(datetime.today()+timedelta(days=-1))].dropna()
        return dates_db
    
    ### If this is a fresh scrape, just return all dates to scrape.
    
    else:
        dates_db = pd.DataFrame({'date':dates})
        dates_db = dates_db[dates_db<(datetime.today()+timedelta(days=-1))].dropna()
        return dates_db

def current_season_switch(dates, links):
    ''' For the first time scraping the current season'''
    
#    dates['date'] = dates['date'].dt.strftime('%Y%m%d'+str(0))
    new_links = [links[i] for i in list(dates.index)]
    
    return new_links
    

# def calc_rest_days(dates_db):
    
#     import pandas as pd
#     from datetime import datetime
#     from datetime import timedelta
    
#     rest = [10]
    
#     for i, date in enumerate(dates_db['date'].iloc[1:]):
#         rest_day = int((date - dates_db['date'].iloc[i]).days)
#         rest.append(rest_day)
        
#     return pd.concat([dates_db, pd.DataFrame({'rest_days':rest})], axis = 1,
#                       ignore_index = True)

def get_line_scores(urls):
    ''' Returns pandas dataframe of home team, away team, and quarterly
    scoring splits.'''
    
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


    for i, url in enumerate(urls):
        sys.stdout.write(f"\rGame Number {i+1}")
        sys.stdout.flush()
        current_game = f'https://www.basketball-reference.com{url}'
        res = requests.get(current_game)
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
        'home_final':home_final,
    }
    
    
    return pd.DataFrame(line_score_dict)

def in_season_update(year = None):
    
    ''' Takes in and updates a csv file in the working directory of format:
        {year}_line_scores.csv
        '''
    
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
    
    import pandas as pd
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import tkinter as tk
    from tkinter import filedialog
    
    if not year:
        year = str((datetime.today()+relativedelta(months=+2)).year)
    
    #Dialog window to select correct file
    root=tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    
    # Read in and organize file by dates
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # The last entry in the dates column is last time we updated
    # the data
    last_date_scraped = df['date'].iloc[-1]

    # For each team, get the URLS, get the dates to scrape 
    # (between last time scraped and the current day)
    # and then extract only the correct URLs from the list using
    # the known needed dates
    
    for team in TEAMS:
        urls = get_urls(year, team)
        dates_to_scrape = get_dates(urls, last_date_scraped)
        date_search = dates_to_scrape['date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'+str(0)))
        
        urls_to_scrape = []
        
        for date in date_search:
            if date in ''.join(urls):
                
                for url in urls:
                    if date in url:
                        urls_to_scrape.append(url)
                        break
                    else:
                        pass
            
        # We have the URLs now, so we can get the line scores
        # like normal. Then we make sure we drop duplicates, 
        # and return the dataframe. The user should manually save.
                    
        line_scores = get_line_scores(urls_to_scrape)
        line_scores = pd.concat([dates_to_scrape, line_scores], axis=1)
        df = pd.concat([df, line_scores]).reset_index(drop=True)
        df.sort_values(by='date', inplace=True)
        df.drop_duplicates(inplace=True)
        df.dropna(inplace = True)
#        df.to_csv(f'{year}_line_scores.csv', index=False)
    return df

def get_four_fac(urls):
    
    import pandas as pd
    import sys
    import requests, bs4
    import re
    
    home_pace = []
    home_efg = []
    home_tov = []
    home_orb = []
    home_ftr = []
    home_ortg = []
    home_drtg = []
    
    away_pace = []
    away_efg = []
    away_tov = []
    away_orb = []
    away_ftr = []
    away_ortg = []
    away_drtg = []
    
    for i, url in enumerate(urls):
        sys.stdout.write(f"\rGame Number {i+1}")
        sys.stdout.flush()
        current_game = f'https://www.basketball-reference.com{url}'
        res = requests.get(current_game)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(re.sub("<!--|-->", "", res.text), 'lxml')
        four_fac = soup.find('table', {'id':'four_factors'})
        four_fac_df = pd.read_html(str(four_fac),flavor='bs4')[0]
        
        home_pace.append(four_fac_df['Unnamed: 1_level_0']['Pace'].iloc[1])
        home_efg.append(four_fac_df['Four Factors']['eFG%'].iloc[1])
        home_tov.append(four_fac_df['Four Factors']['TOV%'].iloc[1])
        home_orb.append(four_fac_df['Four Factors']['ORB%'].iloc[1])
        home_ftr.append(four_fac_df['Four Factors']['FT/FGA'].iloc[1])
        home_ortg.append(four_fac_df['Unnamed: 6_level_0']['ORtg'].iloc[1])
        home_drtg.append(four_fac_df['Unnamed: 6_level_0']['ORtg'].iloc[0])
    
        away_pace.append(four_fac_df['Unnamed: 1_level_0']['Pace'].iloc[0])
        away_efg.append(four_fac_df['Four Factors']['eFG%'].iloc[0])
        away_tov.append(four_fac_df['Four Factors']['TOV%'].iloc[0])
        away_orb.append(four_fac_df['Four Factors']['ORB%'].iloc[0])
        away_ftr.append(four_fac_df['Four Factors']['FT/FGA'].iloc[0])
        away_ortg.append(four_fac_df['Unnamed: 6_level_0']['ORtg'].iloc[0])
        away_drtg.append(four_fac_df['Unnamed: 6_level_0']['ORtg'].iloc[1])
    
    four_facs = {
        'away_pace': away_pace,
        'away_efg': away_efg,
        'away_tov': away_tov,
        'away_orb': away_orb,
        'away_ftr': away_ftr,
        'away_ortg': away_ortg,
        'away_drtg': away_drtg,
    
        'home_pace': home_pace,
        'home_efg': home_efg,
        'home_tov': home_tov,
        'home_orb': home_orb,
        'home_ftr': home_ftr,
        'home_ortg': home_ortg,
        'home_drtg': home_drtg
        }
    
    return pd.DataFrame(four_facs)
        
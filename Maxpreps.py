def get_first_google_result(s):
    '''
    Gets first google result and returns as beautiful soup object
    Input: string
    Output: beautiful soup object for website
    '''
    query = '+'.join(s.split())     
    url = f"https://www.google.com/search?q={query}"
    soup = set_up_soup(url)
    first_result = soup.find('div', class_='yuRUbf')
    
    if first_result:
        return set_up_soup(first_result.a['href'])
    else:
        return None
    


def find_pos_on_maxpreps(name, soup, pos):

    try:
        jersey_pos = soup.find_all('div', class_ = 'jersey-pos')
        sports = soup.find_all('div', class_ = 'sport-name')
        li = list(zip(sports, jersey_pos))
        sports_x_pos = [pos[1] for i, pos in enumerate(li) if 'Football' in str(li[i][0])][0]
        sports_x_pos = sports_x_pos.text.split('• ')[-1]
        sports_x_pos = np.array(sports_x_pos.split(', ')).flatten()
        return sports_x_pos
    except IndexError:
        return np.array([[input_position_from_on3(pos)]])
    

def input_position_from_on3(pos):
    '''
    Differentiates between On3 position and Maxpreps positions
    Input: On3 position
    Output: corresponding maxpreps position (ex. qb should match with qb)
    '''
    maxpreps_positions = ['QB', 'RB', 'WR', 'TE', 'T', 'G', 'C', 'DE', 'CB', 'FS', 'SS', 'DT', 'MLB', 'OLB']
    on3_positions = ['qb', 'rb', 'wr', 'te', 'ot', 'iol', 'xx', 'edge', 'cb', 's', 'xxx', 'dl', 'lb', 'xx', 'ath']

    return [maxpreps_positions[on3_positions.index(pos)]]
   

def assign_pos(jersey_pos, num, poss_positions):
    '''
    Assigns player to position in dataframe
    Inputs: array of positions, number position, offense or defense
    Outputs: position to add
    '''
    counter = 0
    for item in jersey_pos:
        if item in poss_positions:
            counter+=1
            if counter == num:
                return item
    
    return "--"

def get_mp_confName(soup):
    '''
    Gets a player's athletic conference name, useful for finding all-conference data
    Input: Soup object
    Output: Conference name of player
    '''
    team_link = soup.find('a', class_ = 'sc-333a63d7-0 eWSjMq school')['href'] 
    team_link_rankings = team_link + '/football/22-23/standings/'
    soup_team = set_up_soup(team_link_rankings).find("h2", class_ = 'sc-f584fccb-0 hTQrEh heading_125_bold')
    
    return soup_team.text if soup_team else 'Not Found'

def get_team_captain(soup):
    '''
    Finds whether a player is a team captain or not
    Input: maxpreps website beautiful soup object
    Output: team captain
    '''
    try: 
        teamdata = soup.find('div', class_ = 'teamdata')
        sport_arr = soup.find_all('div', class_ = 'sport')
        football = [sport_arr[i] for i, sport in enumerate(sport_arr) if 'Football' in str(sport_arr[i])]
        if 'Captain' in str(football[0]):
            return 1

        return 0
    except IndexError:
        print('Couldn\'t find team captain for player above')
        return 'IndexError'

    return 0

def get_team_rating(soup):
    '''
    Gets a player's team rating from maxpreps
    Input: soup object of the website
    Output: Rating
    '''
    team_link = soup.find('a', class_ = 'sc-333a63d7-0 eWSjMq school')['href'] 
    team_link_rankings = team_link + '/football/22-23/rankings/'
    soup_team = set_up_soup(team_link_rankings)

    trs = soup_team.find_all("tr")
    for tr in trs:
        if team_link + "football/22-23/schedule/" in str(tr):
            return tr.find_all("td")[-1].text
    
    return 'Not_found'

def get_mp_potg(soup):
    '''
    Gets how many times a player has won player of the game, from 2022 and in total
    Input: soup object of the website
    Output: (How many times player won in 2022, Total number of career times player won potg)
    '''
    links = soup.find_all('li', class_ = '')
    soup_potg = ''
    found_soup = 0
    for link in links:
        if "awards" in str(link):
            soup_potg = set_up_soup(link.a['href'])
            found_soup = 1
            break
    
    if found_soup == 0:
        return 0, 0
            
    buttons = soup_potg.find_all('button')
    potg_2022 = 0
    potg_before = 0
    for button in buttons:
        if "Player of the Game" in str(button):
            if "2022" in str(button):
                potg_2022+=1
            if "2021" in str(button) or "2020" in str(button) or "2019" in str(button):
                potg_before+=1
    return potg_2022, potg_before + potg_2022

def set_up_soup(link):
    '''
    Sets up a beatuiful soup object for a website
    Input: Link for parseable website
    Output: Soup object ready for parsing
    '''
    session = requests.Session()
    retry = Retry(connect=4, backoff_factor=2.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }  # headers to approve user agent

    response = session.get(link, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

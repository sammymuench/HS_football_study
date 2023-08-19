def get_player_ratings_and_school(url):
    '''
    Gets player ratings + school name
    Input: url
    Output: dataframe with all info from that on3 webpage
    '''
    
    response = requests.get(url) 
        #requests.get returns a requests.response object. 
        #This sends an HTTP get request. The server responds with the desired info
    
    soup = BeautifulSoup(response.text, 'html.parser')
        #reuturns beautiful soup object to scrape data
        #response.text: tells computer to scrape the HTML content
        #html.parser: parser library that BeautifulSoup uses to parse HTML
    
    players = soup.find_all('li', class_ = "IndustryComparisonList_industryComparisonItemContainer__QNFjk")
        #finds all div elements with the CSS class "player card"
        #find_all method returns a ResultSet object (iterable like a list)
        #each element in the ResultSet object is a Tag object to further search

    data = []
    curr_player = 0
    
    for player in players:
        data.append(create_player(player, curr_player))
        curr_player+=1
        
    df = pd.DataFrame(data)
    return df


def create_player(player, i):
    '''
    Creates a player for the dataframe
    Input beautiful soup object with player, index of current player
    Output: dict with player's information
    '''
    
    new_obs = {}

    on3_a = player.find('a', class_= 
                          f"MuiTypography-root MuiLink-root MuiLink-underlineNone MuiBox-root jss{27 + i * 4} IndustryComparisonFourServicesItem_serviceItemContainer__Vxx5H IndustryComparisonConditionalLink_conditionalLink__C6QoW MuiTypography-colorPrimary")
    ESPN_a = player.find('a', class_= 
                          f"MuiTypography-root MuiLink-root MuiLink-underlineNone MuiBox-root jss{29 + i * 4} IndustryComparisonFourServicesItem_serviceItemContainer__Vxx5H IndustryComparisonConditionalLink_conditionalLink__C6QoW MuiTypography-colorPrimary")
    sports247_a = player.find('a', class_= 
                          f"MuiTypography-root MuiLink-root MuiLink-underlineNone MuiBox-root jss{28 + i * 4} IndustryComparisonFourServicesItem_serviceItemContainer__Vxx5H IndustryComparisonConditionalLink_conditionalLink__C6QoW MuiTypography-colorPrimary")
    rivals_a = player.find('a', class_= 
                          f"MuiTypography-root MuiLink-root MuiLink-underlineNone MuiBox-root jss{30 + i * 4} IndustryComparisonFourServicesItem_serviceItemContainer__Vxx5H IndustryComparisonConditionalLink_conditionalLink__C6QoW MuiTypography-colorPrimary")

    new_obs["Player_Name"] = player.find('a', class_='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-h5 MuiTypography-colorPrimary').text
    new_obs["On3_rating"] = notRivals_rating_assign(on3_a)
    new_obs["ESPN_rating"] = notRivals_rating_assign(ESPN_a)
    new_obs["Rivals_rating"] = rivals_rating_assign(rivals_a)
    new_obs["247_rating"] = notRivals_rating_assign(sports247_a)
    new_obs["On3SchN"], new_obs["On3SchLoc"] = get_school_name(player)
    
    return new_obs
        


def notRivals_rating_assign(soupObj):
    '''
    Assign rating from on3 website
    Input: beautiful soup object that may contain rating
    Output: rating
    '''
    if soupObj is None or soupObj.find('span', class_ = "StarRating_overallRating__MTh52 StarRating_gray__xYvHF") is None:
        return 40.9

    return soupObj.find('span', class_ = "StarRating_overallRating__MTh52 StarRating_gray__xYvHF").text


def rivals_rating_assign(soupObj):
    '''
    Assign rating from on3 website
    Input: beautiful soup object that may contain rating
    Output: rating
    '''
    if soupObj is None or soupObj.find('span', class_ = "StarRating_overallRating__MTh52 StarRating_gray__xYvHF") is None:
        return 2.7

    return soupObj.find('span', class_ = "StarRating_overallRating__MTh52 StarRating_gray__xYvHF").text


def get_school_name(player):
    '''
    Gets the player's ON3 school name, will be important to get other data later
    input: Beautiful soup object for an On3 web page with the player
    output: School name + city
    '''
    school_name = player.find('p', class_='MuiTypography-root IndustryComparisonPlayerItem_hometownContainer__Qvs_0 IndustryComparisonPlayerItem_mobile__ROVeH MuiTypography-body1 MuiTypography-colorTextPrimary')
    school_name = school_name.find('span')
    school_city = player.find('span', class_='IndustryComparisonPlayerItem_homeTown__8IcYx')
    if school_name is not None and school_city is not None:
        return (school_name.text, " (" + school_city.text + ")")
    else:
        return None

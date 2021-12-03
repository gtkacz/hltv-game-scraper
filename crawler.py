import re, sys, time, requests
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm
from bs4 import BeautifulSoup

def tag_cleanup(html):
    html = str(html)
    cleanr = re.compile('<.*?>')
    string = (re.sub(cleanr, '', html))
    string = string.strip()
    return string

def main():
    url = r'https://www.hltv.org/matches/2353153/nip-vs-vitality-iem-winter-2021'
    #url = r'https://www.hltv.org/matches/2353151/g2-vs-liquid-iem-winter-2021'
        
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    
    date_event_table = soup.find_all('div', class_ = 'timeAndEvent')[0]
    date = tag_cleanup(date_event_table.find_all('div', class_ = 'date')[0])
    event = tag_cleanup((date_event_table.find_all('div', class_ = 'event')[0]).find_all('a')[0])
    
    info_table = soup.find_all('div', class_ = ['padding', 'preformatted-text'])[0]
    match_info = tag_cleanup(info_table).split('\n')
    match_info = list(filter(None, match_info))
    
    vetos = []
    
    for veto_table in soup.find_all('div', class_ = 'padding'):
        for veto in veto_table.find_all('div', class_ = ''):
            vetos.append(tag_cleanup(veto)[3:])
    
    maps = {}
    
    for map_table in soup.find_all('div', class_ = 'mapholder'):
        map_name = tag_cleanup(map_table.find('div', class_ = 'mapname'))
        
        for t in map_table.find_all('div', class_ = ['results', 'played']):
            for l in t.find_all('div', class_ = 'results-left'):
                l_team = tag_cleanup(l.find('div', class_ = 'results-teamname'))
                l_result = tag_cleanup(l.find('div', class_ = 'results-team-score'))
                
            for c in t.find_all('div', class_ = 'results-center'):
                try:
                    x = c.find_all('div', class_ = 'results-center-half-score')[0]
                    ct_b = x.find_all('span', class_ = 'ct')
                    t_b = x.find_all('span', class_ = 't')
                    
                    ct_l = tag_cleanup(ct_b[0])
                    ct_r = tag_cleanup(ct_b[1])
                    t_l = tag_cleanup(t_b[1])
                    t_r = tag_cleanup(t_b[0])
                except:
                    pass
            
            for r in t.find_all('span', class_ = 'results-right'):
                r_team = tag_cleanup(r.find('div', class_ = 'results-teamname'))
                r_result = tag_cleanup(r.find('div', class_ = 'results-team-score'))
            
        if l_result != '-':
            maps[map_name] = {l_team: f'{l_result} — CT: {ct_l} T: {t_l}', r_team: f'{r_result} — CT: {ct_r} T: {t_r}'}
        else:
            maps[map_name] = {l_team: l_result, r_team: r_result}
            
    stats = {}
    
    for stats_table in soup.find_all('div', class_ = 'stats-content'):
        teams = stats_table.find_all('table', class_ = ['table', 'totalstats'])
        team_l = teams[0]
        team_r = teams[3] #############configurar pra mapas
        
        names_l = team_l.find_all('td', class_ = 'players')
        kd_l = team_l.find_all('td', class_ = 'kd')
        plus_minus_l = team_l.find_all('td', class_ = 'plus-minus')
        adr_l = team_l.find_all('td', class_ = 'adr')
        kast_l = team_l.find_all('td', class_ = 'kast')
        rating_l = team_l.find_all('td', class_ = 'rating')
        
        names_r = team_r.find_all('td', class_ = 'players')
        print(tag_cleanup(team_r))
        kd_r = team_r.find_all('td', class_ = 'kd')
        plus_minus_r = team_r.find_all('td', class_ = 'plus-minus')
        adr_r = team_r.find_all('td', class_ = 'adr')
        kast_r = team_r.find_all('td', class_ = 'kast')
        rating_r = team_r.find_all('td', class_ = 'rating')
        
        for i in range(1, 5):
            stats[tag_cleanup(names_l[i]).split()[-1]] = {
                'KD': tag_cleanup(kd_l[i]),
                '+/-': tag_cleanup(plus_minus_l[i]),
                'ADR': tag_cleanup(adr_l[i]),
                'KAST': tag_cleanup(kast_l[i]),
                'Rating': tag_cleanup(rating_l[i])
                }

            stats[tag_cleanup(names_r[i]).split()[-1]] = {
                'K-D': tag_cleanup(kd_r[i]),
                '+/-': tag_cleanup(plus_minus_r[i]),
                'ADR': tag_cleanup(adr_r[i]),
                'KAST': tag_cleanup(kast_r[i]),
                'Rating': tag_cleanup(rating_r[i])
                }
        
    print(repr(date), repr(event), '\n')
    
    for i in match_info:
        print(i)
    print('\n')
    
    for i in vetos:
        print(i)
    print('\n')
        
    for x, y in maps.items():
        print(x, y)
    print('\n')
        
    for x, y in stats.items():
        print(x, y)


if __name__ == '__main__':
    main()
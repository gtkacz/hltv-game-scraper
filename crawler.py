import re, sys, time, requests
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

def tag_cleanup(html):
    html = str(html)
    cleanr = re.compile('<.*?>')
    string = (re.sub(cleanr, '', html))
    string = string.strip()
    return string

def main():
    #url = r'https://www.hltv.org/matches/2353153/nip-vs-vitality-iem-winter-2021'
    url = r'https://www.hltv.org/matches/2353151/g2-vs-liquid-iem-winter-2021'
        
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    
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
            
            for r in t.find_all('span', class_ = 'results-right'):
                r_team = tag_cleanup(r.find('div', class_ = 'results-teamname'))
                r_result = tag_cleanup(r.find('div', class_ = 'results-team-score'))
            
        maps[map_name] = {l_team: l_result, r_team: r_result}
        
    for i in match_info:
        print(i)
    print('\n')
    
    for i in vetos:
        print(i)
    print('\n')
        
    for x, y in maps.items():
        print(x, y)


if __name__ == '__main__':
    main()
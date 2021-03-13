

#IMPORT EVERYTHING:
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from itertools import zip_longest
import requests
import time
import csv

#---------------------------------------------#

#OBJECTIVE 1: Scrape RT Top 100 list for titles and partial links

rt_url = "https://www.rottentomatoes.com/top/bestofrt/"

#-- Make ~the soup~
webpage = requests.get(rt_url)
soup = BeautifulSoup(webpage.text, 'html.parser')


#-- Make an empty list for titles
movie_titles = []


#-- Make an empty list for links
movie_links = []


#-- Find the table
rt_table = soup.find('table', class_='table')


#-- Find the titles
rt_rows = rt_table.find_all('a', class_='unstyled articleLink')


#-- Function for titles
def get_titles_from_rt(url):

    for cells in rt_rows:
        movie_title = cells.text.strip()
        movie_titles.append(movie_title)

    return(movie_titles)


#-- Function for partial links
def get_links_from_rt(url):
    for links in rt_rows:
        movie_href = links.attrs['href']
        movie_links.append(movie_href)

    return(movie_links)


#-- Call the function
rt_movie_titles = get_titles_from_rt(rt_url)

rt_movie_links = get_links_from_rt(rt_url)

#Test it:
#print(rt_movie_titles)
#print(rt_movie_links)

#---------------------------------------------#

#OBJECTIVE 2: Scrape TM scores

#-- Fill in your own path to installed chromedriver
driver = webdriver.Chrome('/Users/dirname/dirname/dirname//chromedriver')

#-- Make an empty list for Tomatometer scores
tm_scores = []


#-- Scrape Tomatometer Scores

def scrape_tm_scores(movie_partials):

    for urls in movie_partials:

        driver.get('https://www.rottentomatoes.com' + urls)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        time.sleep(5)

        mainColumn = soup.find(id='mainColumn')

        scoreboard = mainColumn.find('score-board')

        tm_attr = scoreboard.attrs['tomatometerscore']
        tm_scores.append(tm_attr)

    return(tm_scores)



#-- Call the function:

tomatometer_scores = scrape_tm_scores(rt_movie_links)



#---------------------------------------------#

#OBJECTIVE 3: Box Office Mojo- Scrape WW box office earnings


#-- Make an empty list for worldwide box office earnings
boxoffice_earnings = []


def scrape_wwbo(titles):

    for eachtitle in titles:

        #-- Making exceptions for titles from RT that are different on the BOM site
        if eachtitle == 'Portrait of a Lady on Fire (Portrait de la jeune fille en feu) (2020)':
            eachtitle = 'Portrait of a Lady on Fire (2020)'
        elif eachtitle == 'A Night at the Opera (1935)':
            boxoffice_earnings.append('N/A')
            continue
        elif eachtitle == 'La Grande illusion (Grand Illusion) (1938)':
            eachtitle = 'La Grande illusion'
        elif eachtitle == 'The Adventures of Robin Hood (1938)':
            boxoffice_earnings.append('N/A')
            continue
        elif eachtitle == '1917 (2020)':
            eachtitle = '1917'
        elif eachtitle == 'The Battle of Algiers (La Battaglia di Algeri) (1967)':
            eachtitle = 'The Battle of Algiers'
        elif eachtitle == 'Seven Samurai (Shichinin no Samurai) (1956)':
            eachtitle = 'Seven Samurai'

        #-- Load the webpage
        driver.get('https://www.boxofficemojo.com/')
        search_box = driver.find_element_by_name('q')
        #-- Search each title
        search_box.send_keys(str(eachtitle))
        search_box.submit()
        #-- Pause
        time.sleep(3)

        #-- Click first search result
        driver.find_element_by_css_selector('.a-size-medium.a-link-normal.a-text-bold').click()

        #-- Make more soup
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        time.sleep(1)

        try:
            #-- Find the WW box office element
            mojo_performance_sum = soup.find('div', class_='a-section a-spacing-none mojo-performance-summary-table')

            money_span = mojo_performance_sum.find_all('span', class_='a-size-medium a-text-bold')

            ww_elem = money_span[2].find('span', class_='money')

            ww_bo = ww_elem.get_text()

            #-- Add to list
            boxoffice_earnings.append(ww_bo)

        except:
            #-- If no BO earnings listed
            boxoffice_earnings.append('N/A')

    return(boxoffice_earnings)



#-- Call the function
ww_boxoffice = scrape_wwbo(rt_movie_titles)


#---------------------------------------------#

#OBJECTIVE 4: Scrape Audience scores

#-- Make an empty list for Audience scores
aud_scores = []


#-- Scrape Audience Scores

def scrape_aud_scores(partialurls):

    for locallinks in partialurls:

        driver.get('https://www.rottentomatoes.com' + locallinks)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        time.sleep(5)

        mainColumn = soup.find(id='mainColumn')

        scoreboard = mainColumn.find('score-board')

        aud_attr = scoreboard.attrs['audiencescore']
        aud_scores.append(aud_attr)

    return(aud_scores)



#-- Call the function
audience_scores = scrape_aud_scores(rt_movie_links)


#---------------------------------------------#

#OBJECTIVE 5: Box Office Mojo- Scrape Production Budgets

#Make an empty list for production budgets
prod_budgets = []

def scrape_movie_budget(movietitles):

    for title in movietitles:

        #-- Making exceptions for titles from RT that are different on the BOM site
        if title == 'Portrait of a Lady on Fire (Portrait de la jeune fille en feu) (2020)':
            title = 'Portrait of a Lady on Fire (2020)'
        elif title == 'A Night at the Opera (1935)':
            prod_budgets.append('N/A')
            continue
        elif title == 'La Grande illusion (Grand Illusion) (1938)':
            title = 'La Grande illusion'
        elif title == 'The Adventures of Robin Hood (1938)':
            prod_budgets.append('N/A')
            continue
        elif title == '1917 (2020)':
            title = '1917'
        elif title == 'The Battle of Algiers (La Battaglia di Algeri) (1967)':
            title = 'The Battle of Algiers'
        elif title == 'Seven Samurai (Shichinin no Samurai) (1956)':
            title = 'Seven Samurai'

        #-- Load the webpage
        driver.get('https://www.boxofficemojo.com/')
        search_box = driver.find_element_by_name('q')
        #-- Search each title
        search_box.send_keys(str(title))
        search_box.submit()
        #-- Pause
        time.sleep(3)

        #-- Click first search result
        driver.find_element_by_css_selector('.a-size-medium.a-link-normal.a-text-bold').click()

        #-- Make more soup
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        time.sleep(1)

        try:
            #-- Find the budget element
            mojo_summary_table = soup.find('div', class_='a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile')

            table_rows = mojo_summary_table.find_all('div', class_='a-section a-spacing-none')

            budget_span = table_rows[2].find('span', class_='money')

            budget = budget_span.get_text()

            #-- Add to list
            prod_budgets.append(budget)

        except:
            #-- If no budget listed
            prod_budgets.append('N/A')


    return(prod_budgets)


#-- Call the function
production_budget = scrape_movie_budget(rt_movie_titles)


#---------------------------------------------#

#-- QUIT DRIVER FOR WHOLE CODE
driver.quit()

#---------------------------------------------#

#OBJECTIVE 4: Write data to a CSV

def write_csv():

    #-- Create and open a new file
    output_file = open('scraping_proj_output.csv', 'w')

    #-- Python CSV writer object
    csv_writer = csv.writer(output_file)

    #-- Determine order of columns
    lists = [rt_movie_titles, tomatometer_scores, audience_scores, ww_boxoffice, production_budget]

    export_data = zip_longest(*lists, fillvalue = '')

    #-- Column headings
    csv_writer.writerow(['Movie Title and Release Year', 'Tomatometer Score', 'Audience Score', 'Worldwide Box Office Earnings', 'Production Budget for Film'])

    #-- Write data to CSV
    csv_writer.writerow(export_data)

    output_file.close()


write_csv()

print('done :)')

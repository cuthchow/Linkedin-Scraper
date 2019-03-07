from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
from bs4 import BeautifulSoup

#Open browser and linkedin

#Number of profiles to scrape 
people = int(input())

#Open browser
driver = webdriver.Safari()
driver.get('http://www.linkedin.com')


#Function to login from homepage
def login():
    username = 'USERNAME'
    password = 'PASSWORD!'

    userbox = driver.find_element_by_id('login-email')
    passbox = driver.find_element_by_id('login-password')

    userbox.send_keys(username)
    passbox.send_keys(password)
    passbox.send_keys(Keys.RETURN)

    sleep(2)

login()

#Starting spot

#for X number of times:
    #Go to link of person
    #Extract jobs and save to csv
    #Find next link, Go to next page, and repeat step 2

#Link of first profile
starting_link = ''

driver.get('https://www.linkedin.com' + starting_link)
visited_links = [starting_link]
sleep(2)

csvfile = open('Jobs.csv', 'a')
writer = csv.writer(csvfile)
writer.writerow([])
writer.writerow(('name', 'Job 1', 'Job 2', 'Job 3', 'Job 4', 'Job 5', 'Job 6'))

def proceed_to_next(html):
    '''
    find and open the first recommended person link
    Make sure the same person isn't visited twice.
    '''
    try:
        for x in range(0,5):
            nextlink = html.find_all('a', class_ = 'pv-browsemap-section__member ember-view')[x].attrs['href']
            if nextlink not in visited_links:
                visited_links.append(nextlink)
                link = f'http://www.linkedin.com{nextlink}'
                driver.get(link)
                break
    except:
        driver.back()
        sleep(3)
        driver.execute_script("window.scrollTo(150, 400)")
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for x in range(0,5):
            nextlink = soup.find_all('a', class_ = 'pv-browsemap-section__member ember-view')[x].attrs['href']
            if nextlink not in visited_links:
                visited_links.append(nextlink)
                link = f'http://www.linkedin.com{nextlink}'
                driver.get(link)
                break

def extract_jobs():
    '''
    Extracts the job history of the current user profile
    Writes the jobs to a csv file 
    Saves link of the user to avoid effort duplication 
    '''
    sleep(4)
    driver.execute_script("window.scrollTo(150, 650)")
    sleep(3)

    #Get page and parse
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #Find name, all job titles and job locations, find all, convert bs object to list.
    name = soup.select('.pv-top-card-section__name')[0].get_text().strip()
    jobtitle = list(soup.find_all('h3', class_ = 't-16 t-black t-bold'))
    joblocation = list(soup.find_all('span', class_ = 'pv-entity__secondary-title'))

    #Create a list of all jobs. First item in list is name.
    alljobs = []
    alljobs.append(name)

    #Print each job combined, add to all jobs list
    print(f'{name} worked at:')
    for each in range(0,len(jobtitle)):
        job = f'{str(jobtitle[each].text)} at {str(joblocation[each].text)}'
        print(job)
        alljobs.append(job)

    #Write the alljobs list as a row in the csv file
    writer.writerow(alljobs)

    proceed_to_next(soup)

def snoopdogg(x):
    for each in range(x):
        extract_jobs()
    csvfile.close()

#Run Function 
snoopdogg(people)


#Pending Fixes
    #Jobs where there is a missing location or job title
    #How to deal with column only appearing once.
    #explicit waits

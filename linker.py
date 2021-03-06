import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs


# > Get the 'Copy Link' from LinkedIn job posting in /Jobs
# > Retrieve the first href from the page.content to get link to job posting

# Returns corresponding job id from job URL
def get_job_id(url):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)['currentJobId'][0]


def get_linked():
    URL = ''
    URL = input('Paste a LinkedIn Job URL.')  # Link to linkedin job posting

    # If user inputs non-direct link, check if it contains the jobID and build a valid URL
    if 'currentJobId' in URL:
        print('Indirect URL found : parsing job id..')
        job_id = get_job_id(URL)
        URL = f'https://www.linkedin.com/jobs/view/{job_id}'
        print(f'New URL : {URL}')


    # Make request to page
    page = requests.get(URL)

    # Set up beautiful soup object
    soup = BeautifulSoup(page.content, 'html.parser')

    # Ensure user is entering linkedin url
    try:
        result = soup.find(id="main-content")
        #print(result.prettify())
    except AttributeError:
        print('Invalid URL: use valid LinkedIn URL.')
        return

    # Get parent element containing company name and location
    company_and_location = result.find('div', class_='sub-nav-cta__sub-text-container')

    # Retrieve company name and location from parent element
    company = company_and_location.find('a', class_='sub-nav-cta__optional-url')
    location = company_and_location.select('span')[0].get_text(strip=True)

    # Get parent element for job title
    job_title_parent = result.find('h3', class_='sub-nav-cta__header')
    job_title = job_title_parent.text

    # Get parent element for Seniority Level
#    level_parent = result.find('ul', class_='job-criteria__list')
#    level = level_parent.select('span')[0].get_text(strip=True)

    # Create array from retreived values
    job_dict = {'job_title':job_title,'company':company.text,'location':location,'job_url':URL,'level':'Entry Level'}
    return job_dict

import requests
import bs4
from bs4 import BeautifulSoup
import os

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'}
 
def getUrl(url):
  r = requests.get(url, headers=headers)
  r.encoding = r.apparent_encoding
  r.raise_for_status()
  return r.text

def get_page(URL = 'https://www.imdb.com/search/keyword/', page = 1, page_str = 'page='):
  '''
  URL: str - the string of URL deleting the explicit page number
  page: int - the page number
  page_str: str - the key word to test validity avoiding corner case

  Output: str - the targeted url of specific page
  '''
  # Change the page number of target url
  if page_str not in URL:
    print('Cannot find the targeted page keyword, please change another')
    return
  start_index = URL.find(page_str)
  end_index = start_index + len(page_str)
  URL = list(URL)
  URL.insert(end_index + 1, str(page))
  return ''.join(URL)

def get_max_page(URL, left_key_word = 'of', right_key_word = 'titles'):
  '''
  Objective: Getting the possible maximum page of current list
  URL: str - the string of URL of any page list
  left & right keywords: relating starting and ending index

  Output: int - the maximum page of current rank list
  '''
  html = getUrl(URL)
  bf = BeautifulSoup(html, 'html.parser')
  div_content = str(bf.find('div', attrs = {'class': 'desc'}))
  start_index = div_content.find(left_key_word)
  end_index = div_content.find(right_key_word)

  try:
    str_page =  div_content[start_index:end_index].split(' ')[1]
  except:
    str_page = '0'
  if ',' in str_page:
    left, right = str_page.split(',')
    return (int(left)*1000 + int(right)) // 50 + 1
  return int(str_page) // 50 + 1

def get_all_list_page(URL, page_str = 'page', left_key_word = 'of', right_key_word = 'titles'):
  '''
  URL: str - the string of URL deleting the explicit page number
  page_str: str - the key word to test validity avoiding corner case
  left & right keywords: relating starting and ending index

  Output: List[str] - the URL's array of all or Top 10,000 films page list
  '''
  first_page_url = get_page(URL, 1, page_str)
  max_page = get_max_page(first_page_url, left_key_word, right_key_word)
  
  if max_page > 200:
    print(f'The size of film list is over the allowable maximum, current url is {URL[-11:]}')
  
  size = min(max_page, 200)
  res = [] # The variable caching urls
  for page_i in range(size):
    res.append(get_page(URL, page_i + 1, page_str))
  
  return res

def get_all_film_url(page_url):
  '''
  page_url: List[str] - the url list of featured film pages
  
  Output: List[str] - the backend tag for url list of film url on one page
  '''
  html = getUrl(page_url)
  bf = BeautifulSoup(html, 'html.parser')
  temp = bf.find_all('h3', attrs = {'class':'lister-item-header'})
  linkList = []
  for list in temp:
    tempList=list.find('a', attrs = {'class':''})
    link = tempList.get('href')
    linkList.append(link)
  return linkList

# Get the full URL of film
def readable_film_url(back_tag = '', front_tag = 'https://www.imdb.com'):
  return front_tag + back_tag

def get_film_info(film_url):
  '''
  film_url: str - the URL of specific film   
  Output: dict {key-value pairs} - including related info about specific film
  '''
  try:
    r = requests.get(film_url)
    bf = BeautifulSoup(r.text, 'lxml')
    bf_info = bf.find('section', {'class': 'ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-7643a8e3-1 glXLDh'})
  except:
    print(f'request cannot get in {film_url}')
    return {
      'film_name': None,'synopsis': None,'genre_list': None,'publish_year': None,'MPAA': None,
      'Duration_minute': None,'Rating': None,'Rating_popularity': None,'Popularity': None,
      'Director': None,'Writer': None,'Stars': None,'Awards': None,'Release_date': None,
      'Country_of_origin': None,'Language': None,'Filming_locations': None,'Production_companies': None,
      'Budget': None,'Gross_US_Canada': None,'Opening_weekend': None,'Gross_worldwide': None,
      'Runtime': None,'Color': None,'Sound_mix': None,'Aspect_ratio': None,'film_url': film_url
  }

  # Get Film Name
  try:
    name_part = bf_info.find('div', attrs = {'class': 'sc-80d4314-1 fbQftq'}).find('h1')
    film_name = name_part.get_text()
  except:
    film_name = None
    print(f'No film name and current url is {film_url}')
  
  # Get Story Line of Film
  try:
    story_part = bf_info.find('div', attrs = {'class': 'sc-16ede01-7 hrgVKw', 'data-testid': 'plot'})
    story_line = story_part.find('span', {'data-testid': 'plot-xl'}).get_text()
  except:
    story_line = None
    print(f'No synopsis and current url is {film_url}')

  # Get genre tags of film
  try:
    genre_part = bf_info.find('div', attrs = {'class': 'ipc-chip-list--baseAlt ipc-chip-list sc-16ede01-5 ggbGKe', 'data-testid': 'genres'})
    genre_part = genre_part.find_all('a')
    genre_list = []
    for genre in genre_part:
      genre_list.append(genre.get_text())
  except:
    genre_list = None

  # Categorical bar
  category_part = bf_info.find('div', {'class':'sc-80d4314-2 iJtmbR'}).find_all('li')
  # Publish_year
  try:
    publish_year = category_part[0].find('span').get_text() # Publishing year
  except:
    publish_year = None
    print(f'No publish year and current url is {film_url}')
  # MPAA
  try:
    MPAA = category_part[1].find('span').get_text()# MPAA
  except:
    MPAA = None
  # Duration
  try:
    Duration_str = category_part[2].get_text() # Duration
  except:
    try:
      Duration_str = category_part[1].get_text()
    except:
      Duration_str = None

  try:
    Rating = bf_info.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score', 'class': 'sc-7ab21ed2-2 kYEdvH'}).find('span').get_text()
    # Number of users rated the film
    Rating_popularity = bf_info.find('div', {'class': 'sc-7ab21ed2-3 dPVcnq'}).get_text()
  except:
    Rating = None
    Rating_popularity = None

  try:
    Popularity = bf.find('div', {"data-testid":"hero-rating-bar__popularity__score", 
                                 "class":"sc-edc76a2-1 gopMqI"}).get_text() # Popularity
  except:
    Popularity = None
  
  try:
    creator_part = bf.find_all('div', {'class': 'ipc-metadata-list-item__content-container'})
    # Director
    director_part = creator_part[0].find_all('a')
    director_list = []
    for director in director_part:
      director_list.append(director.get_text())
    # Writer
    writer_part = creator_part[1].find_all('a')
    writer_list = []
    for writer in writer_part:
      writer_list.append(writer.get_text())

    # Stars
    stars_part = creator_part[2].find_all('a')
    stars_list = []
    for stars in stars_part:
      stars_list.append(stars.get_text())
  except:
    director_list, writer_list, stars_list = [], [], []
    print(f'No creator part and current url is {film_url}')

  # Awards
  try:
    Awards = bf.find('section', {'cel_widget_id': 'StaticFeature_Awards', 'class': 'ipc-page-section ipc-page-section--base celwidget'})
    Awards = Awards.find('li', {'data-testid': 'award_information'}).find('label', {'class': 'ipc-metadata-list-item__list-content-item'}).get_text()
  except:
    Awards = None

  # Reviews_info
  Reviews_info = bf_info.find('ul', {'class': 'ipc-inline-list sc-124be030-0 ddUaJu baseAlt',
                                     'data-testid': 'reviewContent-all-reviews'})
  Reviews_info = Reviews_info.find_all('li')
  # User reviews
  try:
    User_reviews = Reviews_info[0].find('span', {'class': 'score'}).get_text()
  except:
    User_reviews = None
  # Critic reviews
  try:
    Critic_reviews = Reviews_info[1].find('span', {'class': 'score'}).get_text()
  except:
    Critic_reviews = None
  # Metascore
  try:
    Metascore = Reviews_info[2].find('span', {'class': 'score'}).get_text()
  except:
    Metascore = None


  # For Info Details
  try:
    details = bf.find('section',{'data-testid':'Details', 'class': 'ipc-page-section ipc-page-section--base celwidget'})
  except:
    details = None
    print(f'No details for {film_url}')
  # Release Date
  try:
    Release_date = details.find('li', {'role':'presentation', 'data-testid': 'title-details-releasedate'}).\
                   find('div').get_text()
  except:
    Release_date = None
  # Country of origin
  try:
    Country_of_origin = []
    tmp_list = details.find('li', {'role':'presentation', 'data-testid': 'title-details-origin'}).\
               find('div').find_all('li')
    for tmp in tmp_list:
      Country_of_origin.append(tmp.get_text())
  except:
    Country_of_origin = []
  # Language
  try:
    Language = []
    tmp_list = details.find('li', {'role':'presentation', 'data-testid': 'title-details-languages'}).\
               find('div').find_all('li')
    for tmp in tmp_list:
      Language.append(tmp.get_text())
  except:
    Language = []
  # Filming locations
  try:
    Filming_locations = details.find('li', {'role':'presentation', 'data-testid': 'title-details-filminglocations'}).\
                        find('div').get_text()
  except:
    Filming_locations = None
  # Production companies
  try:
    Production_companies = []
    tmp_list = details.find('li', {'role':'presentation', 'data-testid': 'title-details-companies'}).\
               find('div').find_all('li')
    for tmp in tmp_list:
      Production_companies.append(tmp.get_text())
  except:
    Production_companies = []
  
  # Box office
  try:
    box_office = bf.find('section',{'data-testid':'BoxOffice', 'class': 'ipc-page-section ipc-page-section--base celwidget'})
    box_office = box_office.find('div', {'data-testid':'title-boxoffice-section'})
  except:
    box_office = None
  # Budget
  try:
    Budget = box_office.find('li', {'data-testid': 'title-boxoffice-budget'}).find('div').find('span').get_text()
  except:
    Budget = None
  # Gross US & Canada
  try:
    Gross_US_Canada = box_office.find('li', {'data-testid': 'title-boxoffice-grossdomestic'}).find('div').find('span').get_text()
  except:
    Gross_US_Canada = None
  # Opening weekend US & Canada
  try:
    Opening_weekend = box_office.find('li', {'data-testid': 'title-boxoffice-openingweekenddomestic'}).find('div').find('span').get_text()
  except:
    Opening_weekend = None
  # Gross worldwide
  try:
    Gross_worldwide = box_office.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).find('div').find('span').get_text()
  except:
    Gross_worldwide = None

  # Technical Specs
  try:
    Technical_specs = bf.find('section',{'data-testid':'TechSpecs', 'class': 'ipc-page-section ipc-page-section--base celwidget'})
    Technical_specs = Technical_specs.find('div', {'data-testid':'title-techspecs-section'})
  except:
    Technical_specs = None
    print(f'No Technical Specs for {film_url}')
  # Runtime
  try:
    Runtime = Technical_specs.find('li', {'data-testid': 'title-techspec_runtime'}).find('div').get_text()
  except:
    Runtime = None
  # Color
  try:
    Color = Technical_specs.find('li', {'data-testid': 'title-techspec_color'}).find('div').get_text()
  except:
    Color = None
  # Sound mix
  try:
    Sound_mix = []
    Sound_mix_list = Technical_specs.find('li', {'data-testid': 'title-techspec_soundmix'}).find('div').find_all('li')
    for sound in Sound_mix_list:
      Sound_mix.append(sound.get_text())
  except:
    Sound_mix = []
  # Aspect ratio
  try:
    Aspect_ratio = Technical_specs.find('li', {'data-testid': 'title-techspec_aspectratio'}).find('div').get_text()
  except:
    Aspect_ratio = None

  return {
      'film_name': film_name,
      'synopsis': story_line,
      'genre_list': genre_list,
      'publish_year': publish_year,
      'MPAA': MPAA,
      'Duration_minute': Duration_str,
      'Rating': Rating,
      'Rating_popularity': Rating_popularity,
      'Popularity': Popularity,
      'Director': director_list,
      'Writer': writer_list,
      'Stars': stars_list,
      'Awards': Awards,
      'User_reviews': User_reviews,
      'Critic_reviews': Critic_reviews,
      'Metascore': Metascore,
      'Release_date': Release_date,
      'Country_of_origin': Country_of_origin,
      'Language': Language,
      'Filming_locations': Filming_locations,
      'Production_companies': Production_companies,
      'Budget': Budget,
      'Gross_US_Canada': Gross_US_Canada,
      'Opening_weekend': Opening_weekend,
      'Gross_worldwide': Gross_worldwide,
      'Runtime': Runtime,
      'Color': Color,
      'Sound_mix': Sound_mix,
      'Aspect_ratio': Aspect_ratio,
      'film_url': film_url
  }

def scrap_film_url_list(start_year = 1992, end_year = 2022):
  '''
  Filter_rules: (sample size: 112,464)
  - Featured Film
  - IMDB RATING From 3 to 10
  - At least 10000 votes

  URL: https://www.imdb.com/search/keyword/?ref_=kw_ref_yr&mode=detail&page=&title_type=movie&user_rating=3.0%2C&num_votes=10000%2C&sort=moviemeter,asc&release_date=2022%2C2022

  start_year & end_year: int - the year starting or ending recording films
  Output: List[str] - the validate url list of films published between start_year and end_year
  '''
  page_url_list = []
  # Get the url of page by year
  for target_year in range(start_year, end_year + 1):
    URL = f'https://www.imdb.com/search/keyword/?ref_=kw_ref_yr&mode=detail&page=&title_type=movie&user_rating=3.0%2C&num_votes=10000%2C&sort=moviemeter,asc&release_date={target_year}%2C{target_year}'
    try:
      page_url_list.extend(get_all_list_page(URL))
    except:
      print(URL)
  print('Already get url of page by year')
  print('# of unique pages: ', len(page_url_list))

  # Parse the tag of film
  film_url_list = []
  for page_url in page_url_list: # url of one page
    page_film_tag = get_all_film_url(page_url) # The list of film url tag in one page
    for film_tag in page_film_tag: # One film tag in one page
      film_url = readable_film_url(back_tag = film_tag, front_tag = 'https://www.imdb.com') # Transfer to url
      film_url_list.append(film_url)
  print('# of unique movies: ', len(set(film_url_list)))
  return film_url_list

import pandas as pd
def scrap_film_info_by_url(film_url_list):
  '''
  Output: DataFrame with film information
  '''
  film_info_df = pd.DataFrame()
  for film_url in film_url_list:
    film_info = get_film_info(film_url)
    film_info_df = film_info_df.append(film_info, ignore_index=True)
  return film_info_df
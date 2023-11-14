from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import json

HEADERS = {'User-Agent': UserAgent().chrome}
baseUrl = 'https://old.reddit.com'

class RedditEntry:
  def __init__(self, body, score, likes, dislikes, author, date):
    self.body = body
    self.score = score
    self.likes = likes
    self.dislikes = dislikes
    self.author = author
    self.date = date

class RedditPost:
  def __init__(self, title, post, comments):
    self.title = title
    self.post = post
    self.comments = comments

def get_soup(url):
  r = requests.get(url, headers=HEADERS)
  return BeautifulSoup(r.text, 'lxml')

def safe_get_text(value):
  try:
    value = value.text
  except:
    value = value
  return value

def safe_get_points(value):
  try:
    value = value.split(' ', 1)[0]
  except:
    value = value
  return value

def parse_post(soup):
  # extract main post information
  title = safe_get_text(soup.find('p', {'class': 'title'}))
  body = safe_get_text(soup.find('div', {'class': 'expando'}))

  post_metadata = soup.find('div', {'class': 'sitetable'})
  score = safe_get_text(post_metadata.find('div', {'class': 'score unvoted'}))
  likes = safe_get_text(post_metadata.find('div', {'class': 'score likes'}))
  dislikes = safe_get_text(post_metadata.find('div', {'class': 'score dislikes'}))
  author = safe_get_text(post_metadata.find('a', {'class': 'author'}))
  date = post_metadata.find('time', {'title': True})['title']
  postEntry = RedditEntry(body, score, likes, dislikes, author, date)

  # extract all comments and add to an array
  comments = list()
  for entry in soup.findAll('div', {'class': 'entry'}):
    body = entry.find('div', {'class': 'usertext-body'})
    if body == None:
      continue
    body = safe_get_text(body.find('p'))

    post_metadata = entry.find('p', {'class': 'tagline'})
    score = safe_get_points(safe_get_text(post_metadata.find('span', {'class': 'score unvoted'})))
    likes = safe_get_points(safe_get_text(post_metadata.find('span', {'class': 'score likes'})))
    dislikes = safe_get_points(safe_get_text(post_metadata.find('span', {'class': 'score dislikes'})))
    author = safe_get_text(post_metadata.find('a', {'class': 'author'}))
    date = post_metadata.find('time', {'title': True})['title']

    comment = RedditEntry(body, score, likes, dislikes, author, date)
    comments.append(comment.__dict__)

  return RedditPost(title, postEntry.__dict__, comments)

def parse_search(soup):
  links = list()
  post_section = soup.find('header', {'class': 'search-result-group-header'}).parent
  for link in post_section.findAll('a', {'class': 'search-title', 'href': True}):
    links.append(link['href'])

  return links

def get_post_info(url):
  print('Fetching data from ' + url)
  soup = get_soup(url)
  post = parse_post(soup)
  post.url = url
  return post

def get_post_links(url):
  soup = get_soup(url)
  links = parse_search(soup)
  return links

def dump_data(posts, filename):
  print('\nDumping data in file ' + filename)
  with open(filename, 'w') as fh:
    fh.write(json.dumps(posts))

  return filename

def run(term, subreddit):
  queryPath = ''
  if subreddit == None:
    queryPath = '/search?q=' + term
  else:
    queryPath = '/r/' + subreddit + '/search?q=' + term + '&restrict_sr=on'

  urls = get_post_links(baseUrl + queryPath)
  posts = list()
  for url in urls:
    posts.append(get_post_info(url + '?limit=500').__dict__)

  dump_data(posts, 'test_reddit.json')

run('fifa+world+cup', None)
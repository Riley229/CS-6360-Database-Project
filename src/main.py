from scrapers.reddit_scraper import search_reddit
import json

def dump_data(posts, filename):
  print('\nDumping data in file ' + filename)
  with open(filename, 'w') as fh:
    fh.write(json.dumps(posts))

  return filename


# a sample test for the reddit web scraper
reddit_data = search_reddit('cute elephant photos', None)
dump_data(reddit_data, 'reddit-test.json')
import sys
import requests
from bs4 import BeautifulSoup

# constants
NOT_AVAILABLE = "not available"

# check arguments
if len(sys.argv) < 2:
    print("Please provide the url of a webresource, e.g. http://www.github.com")
    sys.exit(1)

# fetch url
url_to_check = sys.argv[1]
request_result = requests.get(url_to_check)

# get all included resources
html = request_result.text
soup = BeautifulSoup(html, 'html.parser')
# css files
links = soup.find_all('link')
for link in links:
    # TODO load everything with preload or stylesheet rel
    print('it is a link : ' + str(link.get('href')) + ' rel: ' +  str(link.get('rel')))

# read cache control and etag header
if 'cache-control' in request_result.headers:
    cache_control = request_result.headers['cache-control']
else:
    cache_control = NOT_AVAILABLE
if 'etag' in request_result.headers:
    etag = request_result.headers['etag']
else:
    etag = NOT_AVAILABLE

print("Cache statistics for resource " + url_to_check)
print("Cache control: " + cache_control)
print("Etag: " + etag)

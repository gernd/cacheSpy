import sys
import requests
from bs4 import BeautifulSoup

# constants
NOT_AVAILABLE = "not available"

# methods

def get_cache_properties(web_resource_url):
    """Gets the cache properties of the given URL

    web_resource_url: The URL from which the resource should be fetched
    Returns: a tuple consisting holding the cache-control header and the etag
    """
    print('Fetching cache props for: ' + str(web_resource_url))

    # perform actual request
    request_result = requests.get(web_resource_url)

    # read cache control and etag header from response
    if 'cache-control' in request_result.headers:
        cache_control = request_result.headers['cache-control']
    else:
        cache_control = NOT_AVAILABLE
    if 'etag' in request_result.headers:
        etag = request_result.headers['etag']
    else:
        etag = NOT_AVAILABLE

    return (cache_control, etag)


# check arguments
if len(sys.argv) < 2:
    print("Please provide the url of a webresource, e.g. http://www.github.com")
    sys.exit(1)

# fetch url of root webresource
url_to_check = sys.argv[1]
request_result = requests.get(url_to_check)

# get all included resources
html = request_result.text
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('link')
for link in links:
    # we need the rel attribute for checking the resource
    if not link.get('rel'):
        continue
    rel_val = link.get('rel')[0]

    # at the moment we only consider stylesheets and preloaded resources
    if not rel_val in ('stylesheet', 'preload'):
        continue

    # get cache properties for resource
    url = link.get('href')
    cache_props = get_cache_properties(url)

    print("Cache statistics for resource " + url)
    print("Cache control: " + cache_props[0])
    print("Etag: " + cache_props[1])

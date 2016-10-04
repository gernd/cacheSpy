import sys
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# constants
NOT_AVAILABLE = "not available"

# methods
def extract_cache_properties(request_result):
    """Extracts cache properties from a request result

    request_result: Result of the request for extracting the cache properties
    Returns: a tuple consisting holding the cache-control header and the etag
    """
    if 'cache-control' in request_result.headers:
        cache_control = request_result.headers['cache-control']
    else:
        cache_control = NOT_AVAILABLE
    if 'etag' in request_result.headers:
        etag = request_result.headers['etag']
    else:
        etag = NOT_AVAILABLE

    return (cache_control, etag)

def get_cache_properties(web_resource_url):
    """Gets the cache properties of the given URL

    web_resource_url: The URL from which the resource should be fetched
    Returns: a tuple consisting holding the cache-control header and the etag
    """
    print('Fetching cache props for: ' + str(web_resource_url))

    # perform actual request
    request_result = requests.get(web_resource_url)

    cache_properties = extract_cache_properties(request_result)
    return cache_properties

# check arguments
if len(sys.argv) < 2:
    print("Please provide the url of a webresource, e.g. http://www.github.com")
    sys.exit(1)

# aggregated cache information 
cache_information_items = []

# fetch root webresource
url_to_check = sys.argv[1]
request_result = requests.get(url_to_check)

# print cache properties of "main" url
cache_props = extract_cache_properties(request_result)
cache_information = (url_to_check,) + cache_props 
cache_information_items.append(cache_information)

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
    cache_information = (url,) + cache_props 
    cache_information_items.append(cache_information)

# print all cache properties
t = PrettyTable(['Summary'])
print(t)
t = PrettyTable(['URL', 'Cache-Control', 'Etag'])
for cache_information in cache_information_items:
    t.add_row([cache_information[0],cache_information[1],cache_information[2]])

print(t)

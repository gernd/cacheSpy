import sys
import requests

# check arguments
if len(sys.argv) < 2:
    print("Please provide the url of a webresource, e.g. http://www.github.com")
    sys.exit(1)

# fetch url
url_to_check = sys.argv[1]
request_result = requests.get(url_to_check)

# read cache control and etag header
if 'cache-control' in request_result.headers:
    cache_control = request_result.headers['cache-control']
else:
    cache_control = "not available"
if 'etag' in request_result.headers:
    etag = request_result.headers['etag']
else:
    etag = "not available"

print("Cache statistics for resource " + url_to_check)
print("Cache control: " + cache_control)
print("Etag: " + etag)


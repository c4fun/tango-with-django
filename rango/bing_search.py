__author__ = 'laurichard'
import json
import urllib.request
import urllib.parse
from rango.keys import BING_API_KEY



def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/v1/'
    source = 'Web'

    # Specify how many results we wish to return per page
    results_per_page = 10
    offset = 0

    # Warp quotes around our query terms as required by the Bing API
    query = "'{0}'".format(search_terms)
    query = urllib.request.quote(query)

    # Constructs the latter part of our request's URL
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query
    )

    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''

    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # Create our results list which we'll populate
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        # Connect to the server and read the response generated.
        response = urllib.request.urlopen(search_url).read()

        # Convert the bytes to a str. Because "The JSON object must be str, not 'bytes'"
        str_response = response.decode('utf-8')

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(str_response)

        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']
            })
    except urllib.request.URLError as e:
        # Catch a URLError exception - something went wrong when connecting
        print("Error when querying the Bing API: "+e)

    return results

def main():
    search_terms = input("Input the word you want to search>> ")
    results = run_query(search_terms)
    print("Rank"+' '+'Title'+50*' '+'URL')
    rank = 0
    for result in results:
        rank += 1
        print(str(rank).ljust(5), end=' ')
        print(result['title'].ljust(50), end=' ')
        print(result['link'])

if __name__ == '__main__':
    main()
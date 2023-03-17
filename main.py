import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs
from jsbeautifier import beautify
import cssutils

# Define the website URL
url = "https://www.kryptokrona.org/en"

# Parse the website URL to get the domain name
domain_name = urlparse(url).netloc

## create regular user agent id, not a python bot
# initialize a session
session = requests.Session()
# set the User-agent as a regular browser
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"


# Create a directory to store the downloaded files
directory = f"{domain_name}_files"
if not os.path.exists(directory):
    os.makedirs(directory)

# Download the HTML file and save it
html = session.get(url).content
html_text = session.get(url).text
soup = bs(html, "html.parser")


# get script files
cont = 0
for script in soup.find_all("script"):
    if script.attrs.get("src"):
        script_url = urljoin(url, script.attrs.get("src"))
        # put file in the javascript folder.
        # get the file in javascript
        js = requests.get(script_url)
        fname = os.path.basename(urlparse(script_url).path)
        print(f"writing file {fname}")
        with open(f"{directory}/{fname}", "wb") as f:
            f.write(js.content)
        cont += 1

# write css files
css_files = []
count = 1
for css_tag in soup.find_all("link"):
    if css_tag.attrs.get("href") and css_tag.attrs.get("rel")==['stylesheet']:
        try:
            css_url = urljoin(url, css_tag.attrs.get("href"))
            ## get the css files
            css = requests.get(css_url)
            # change the name of the href tag
            fname = os.path.basename(urlparse(css_url).path)
            css_tag["href"] = fname
            print(f"writing file {fname}")
            # write the file
            with open(f"{directory}/{fname}","wb") as f:
                f.write(css.content)
                count += 1
        except:
            print('there was an error')

print(f'writing file index.html')
with open(f"{directory}/index.html", "w") as f:
    f.write(soup.prettify())

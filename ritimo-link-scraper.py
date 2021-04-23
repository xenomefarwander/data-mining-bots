import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Retrive url - Uncomment the next six lines to retrieve from URL


def makePageRequest(counter):
	urlNum = 20 * counter
	url = "https://www.ritimo.org/Repertoire-des-associations?mots%5B%5D=434&debut_acteurs={}#pagination_acteurs".format(urlNum)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}
	pageRequest = urllib.request.Request(url, headers=headers)
	return url

# Ignore SSL errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


counter = 0
listUL = [] 
# Cycles through each webpage and grabs all the lists matching css element "ul" (under which we find the list of site titles)
while counter < 6 :
	pageRequest = makePageRequest(counter)
	with urllib.request.urlopen(pageRequest) as contents: #Uncomment this line to retrive URL (use in conjunction with retrieve url)
		soup = BeautifulSoup(contents, 'html.parser')
		relevantLists = soup.find_all("ul", class_="liste-items liste-articles")
		listUL.append(relevantLists)			
	counter += 1

# Cycles through the ompiles the hrefs into formated links
output_counter = 0
for element in listUL:
	for line in element:
		content = str(line).strip()
		content = content.replace("\n", "")
		payLoad = re.findall('a href="(\S+)"', content)
		for entry in payLoad:
			payLoad = str(entry)
			print("https://www.ritimo.org/"+payLoad)
			output_counter +=1

print(f"\nTotal output: {output_counter}")




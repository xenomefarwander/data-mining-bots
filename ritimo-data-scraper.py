"""  Data miner for French site ritimo.org - 
Primary bug is that the dictionary values print with a '\n' character between them even when
line has been stripped and I cannot find a way to eliminate it.  It's easily fixed in a text
editor after export by searching and replacing any line returns + '\n' characters with just 
the '\n' character before exporting to excel or database"""

#  Structures the data output into rows that print in succession

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

def makePageRequest(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}
	pageRequest = urllib.request.Request(url, headers=headers)
	return url

def createDict(set_name, elements):
	#Takes <h2>s as set_name, i.e. keys, and <li>s as elements, i.e. values, and returns a dictionary
	dictKeys = []
	dictValues = []
	newDict = {}
	i = 0
	for item in set_name[0:4]:
		dictKeys.append(item.get_text())
	for item in elements:
		s = item.get_text()
		s = s.strip()
		s = s.replace(';', ',')
		s = s.replace('\n', '\\n')
		dictValues.append(s)
	while i < 4:
		try:
			newDict[dictKeys[i]] = dictValues[i]
			i += 1
		except:
			break
	return newDict


# Reads in file and stores each line as element in list
# filename = "output_links.txt"
# readURL = []
# with open(filename, 'r') as f:
# 	for line in f:
# 		if (line == "\n"):
# 			break
# 		else:
# 			line = line.rstrip()
# 			readURL.append(line)


# Print out first line with columns
print("Name; Address; Description; Home Country; Types of Actions; Actions in France; " \
		"Actions Outside France")

#Create loop... open page, scrape data, save data, close page
# for page in readURL:
#Opens page and scrapes for data 
pageRequest = makePageRequest("https://www.ritimo.org/Centre-de-Ressources-sur-le-Commerce-Equitable")
# Open url with urllib and pass into BS
with urllib.request.urlopen(pageRequest) as contents:
	soup = BeautifulSoup(contents, 'html.parser')

	# Get the organization's name
	org_name = soup.h1.get_text()
	org_name = org_name.replace(';', ',')

	# Get the organization's address (and clean up data formatting)
	rawAddress = soup.find(class_="adresse").get_text() # Contains Street address, Tel number, email, website (split)
	rawAddressList = rawAddress.split("\n")
	cleanAddressList = []
	for line in rawAddressList:
		line = line.strip()
		if re.search('^\S+', line):
			cleanAddressList.append(line)
	address = str(", ".join(cleanAddressList))
	address = address.replace(';', ',')
	
	# Get the organization's description
	description = soup.find(class_="texte").get_text()
	description = description.strip()
	description = description.replace(';', ',')
	description = description.replace('\n', '\\n')
	
	# Get the headers for the "set" names (grabs all but beyond h2_all[3] we can discard as not relevant headers)
	h2_all = soup.find_all("h2")
	# Get the "mots acteurs", which are the "elements" in our "sets"
	motsActeurs_all = soup.find_all("ul", class_="liste-mots-acteur")
	# Create a dictionary that takes the "set" name as the key and the "elements" as the value 
	myDict = createDict(h2_all, motsActeurs_all)
	
	print(org_name+"; "+address+"; "+description+"; ", end='')
	try:
		print(myDict["Pays d'intervention"], end='; ')
	except:
		print("N/A", end='; ')
	try:
		print(myDict["Types d'action"], end='; ')
	except:
		print("N/A", end='; ')
	try:
		print(myDict["Domaines d'intervention en France"], end='; ')
	except:
		print("N/A", end='; ')
	try:
		printList = myDict["Domaines d'intervention à l'étranger"]
		for item in printList:
			print(item, end='')
	except:
		print("N/A")
	print('\n', end='')




		



from electiondata import *

url = 'http://www.archives.gov/federal-register/electoral-college/2012/popular-vote.html'
filenameCSV = 'electionCollection.csv'
filenameJSON = 'electionCollection.json'
eclt = ElectionCollection(url)
eclt.collectToFile(filenameCSV)
eclt.collectToFile(filenameJSON)

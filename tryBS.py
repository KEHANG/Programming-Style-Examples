from electiondata import *

url = 'http://www.archives.gov/federal-register/electoral-college/2012/popular-vote.html'
filenameCSV = 'electionColletion.csv'
filenameJSON = 'electionColletion.json'
eclt = ElectionColletion(url)
eclt.collectToFile(filenameCSV)
eclt.collectToFile(filenameJSON)

from BeautifulSoup import *
import requests

class ElectionResults:
  
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        self.file = open(self.filename, 'r')
        self.all_lines = self.file.readlines()

    def states(self):
        all_names = []
        for line in self.all_lines:
            columns = line.split(',')
            all_names.append(columns[1])
        return all_names[1:]

    def state_count(self):
        return len(self.states())

    def addCandidates(self):
        self.candidates = []
        firstLine = self.all_lines[0].split(',')
        firstCandidate = (firstLine[3].split(' '))[0]
        secondCandidate = (firstLine[5].split(' '))[0]
        self.candidates.append(firstCandidate)
        self.candidates.append(secondCandidate)


    def addTotalVotes(self):
        self.totalVotes = {}
        firstTotVts = 0
        secondTotVts = 0

        for line in self.all_lines[1:]:
            firstTotVts += int((line.split(','))[3])
            secondTotVts += int((line.split(','))[5])

        firstCandidate = self.candidates[0]
        secondCandidate = self.candidates[1]

        self.totalVotes[firstCandidate] = firstTotVts
        self.totalVotes[secondCandidate] = secondTotVts

class ElectionCollection(object):
    def __init__(self, url):
        self.url = url

    def collectToFile(self, filename):
        fileExt = filename.split('.')[-1]
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content)

        tableOut = soup.find('table')
        table = tableOut.find('table')
        rows = table.findAll('tr')

        firstRow = rows[0]
        colHeads_raw = firstRow.findAll('th')
        colHeads = [head.text.replace('&nbsp;',' ').strip() for head in colHeads_raw]


        file = open(filename, 'w')
        if fileExt.lower() == 'csv':
            # write column heads
            for colHead in colHeads[:-1]:
                file.write(colHead + ',')
            file.write(colHeads[-1] + '\n')

            # write table body rows
            for row in rows[1:-1]:
                # write each row head
                rowHead = row.find('th')
                file.write(rowHead.text + ',')
                # write row cells
                rowCells = row.findAll('td')
                for cell in rowCells[:-1]:
                    file.write(cell.text + ',')
                file.write(rowCells[-1].text + '\n')
        elif fileExt.lower() == 'json':
            file.write('[')
            # write rows from second to last second
            for row in rows[1:-1]:
                file.write(' {\n')
                rowHead = row.find('th')
                file.write('\t"' + colHeads[0] + '": ' + '"' + rowHead.text + '",\n')

                rowCells_raw = row.findAll('td')
                rowCells_changeDash = [cell.text.replace('-','0') for cell in rowCells_raw]
                rowCells = [cell.replace('*','') for cell in rowCells_changeDash]

                for i in range(len(rowCells)-1):
                    file.write('\t"' + colHeads[i+1] + '": ' + rowCells[i] + ',\n')
                file.write('\t"' + colHeads[-1] + '": ' + rowCells[-1] + '\n')
                file.write(' },\n')

            # write final row
            row = rows[-1]
            file.write(' {\n')
            rowHead = row.find('th')
            file.write('\t"' + colHeads[0] + '": ' + '"' + rowHead.text + '",\n')

            rowCells_raw = row.findAll('td')
            rowCells_changeDash = [cell.text.replace('-','0') for cell in rowCells_raw]
            rowCells = [cell.replace('*','') for cell in rowCells_changeDash]

            for i in range(len(rowCells)-1):
                file.write('\t"' + colHeads[i+1] + '": ' + rowCells[i] + ',\n')
            file.write('\t"' + colHeads[-1] + '": ' + rowCells[-1] + '\n')
            file.write(' } ]')

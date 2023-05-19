import pandas as pd
import datetime

# Leitura do arquivo XLSX
workbook = pd.read_excel('./database/base_1.xlsx')
data = workbook.to_dict(orient='records')

# Formatação da data para o formato desejado
for row in data:
    row['date'] = row['date'].strftime('%Y-%m-%d')

# Cálculo do total de atendimentos
def getTotalOccurrences(data):
    return len(data)

totalOccurrences = getTotalOccurrences(data)

# Cálculo do total de dias analisados
def getTotalDays(data):
    uniqueDates = set(row['date'] for row in data)
    return len(uniqueDates)

totalDays = getTotalDays(data)

# Coleta tratada de datas
def getAllDates(data):
    count = {}
    for row in data:
        date = row['date']
        if date in count:
            count[date] += 1
        else:
            count[date] = 1
    return count

alldates = getAllDates(data)

# Cálculo da média mensal de atendimentos
def getMonthlyAverage(data):
    countsByMonth = {}
    for row in data:
        date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        month = date.strftime('%Y-%m')
        if month not in countsByMonth:
            countsByMonth[month] = 0
        countsByMonth[month] += 1

    monthlyAverages = {}
    for month, count in countsByMonth.items():
        daysInMonth = (datetime.datetime.strptime(month, '%Y-%m').replace(day=1) + datetime.timedelta(days=32)).day - 1
        average = count / daysInMonth
        monthlyAverages[month] = '{:.2f}'.format(average)

    return monthlyAverages

monthlyAverages = getMonthlyAverage(data)

# Retorna a média do total de meses em análise
def getTotalMonthlyAverage(monthlyAverages):
    totalAverage = sum(float(avg) for avg in monthlyAverages.values())
    totalMonths = len(monthlyAverages)
    totalMonthlyAverage = totalAverage / totalMonths
    return round(totalMonthlyAverage, 2)

totalMonthlyAverage = getTotalMonthlyAverage(monthlyAverages)

# Cálculo da média diária de atendimentos
def getDailyAverage(data):
    totalOccurrences = getTotalOccurrences(data)
    totalDays = getTotalDays(data)
    dailyAverage = totalOccurrences / totalDays
    return round(dailyAverage, 2)

dailyAverage = getDailyAverage(data)

# Ordenação crescente das datas
def sortDates(getAllDates):
    sortedDates = sorted(getAllDates.keys(), key=lambda date: datetime.datetime.strptime(date, '%Y-%m-%d'))
    sortedObj = {date: getAllDates[date] for date in sortedDates}
    return sortedObj

sortedDates = sortDates(alldates)

# Coleta ordenada dos Estados presentes no banco
def getCountryStates(data):
    uniqueCountryStates = list(set(row['country_state'] for row in data))
    return uniqueCountryStates

uniqueCountryStates = getCountryStates(data)

# Coleta ordenada das bases presentes no banco
def getUniquebase(data):
    baseReturn = list(set(row['base'] for row in data))
    return baseReturn

polo = getUniquebase(data)

# Verifica a quantidade de bases por Estado
def countBasesByState(data):
    stateBases = {}
    for row in data:
        state = row['country_state']
        base = row['base']
        if state not in stateBases:
            stateBases[state] = []
        stateBases[state].append(base)
    stateBaseCount = {state: len(bases) for state, bases in stateBases.items()}
    return stateBaseCount

stateCounts = countBasesByState(data)

# Retorno do número de ocorrências por Base
def countBases(data):
    count = {}
    for row in data:
        base = row['base']
        if base in count:
            count[base] += 1
        else:
            count[base] = 1
    return count

baseCount = countBases(data)

# Pesquisa de atendimentos com base na Data
def getOccurrenceByDate(data, date):
    filteredData = [row for row in data if row['date'] == date]
    statesCount = countBasesByState(filteredData)
    basesCount = countBases(filteredData)

    return {
        'states': statesCount,
        'bases': basesCount
    }

result = getOccurrenceByDate(data, '2020-06-05')

# Retorna a ocorrência das bases por datas
def getBaseCountsByDate(data):
    countsByDate = {}
    for row in data:
        date = row['date']
        base = row['base']
        if date not in countsByDate:
            countsByDate[date] = {}
        if base not in countsByDate[date]:
            countsByDate[date][base] = 1
        else:
            countsByDate[date][base] += 1
    return countsByDate

baseCountsByDate = getBaseCountsByDate(data)

# Verifica o top e o Bottom em número de atendimentos
def findMostAndLeastOccurredStates(data):
    stateCounts = countBasesByState(data)
    mostOccurredState = max(stateCounts, key=stateCounts.get)
    leastOccurredState = min(stateCounts, key=stateCounts.get)
    return {
        'mostOccurredState': mostOccurredState,
        'leastOccurredState': leastOccurredState
    }

mostAndLeastOccurredStates = findMostAndLeastOccurredStates(data)
mostOccurredState = mostAndLeastOccurredStates['mostOccurredState']
leastOccurredState = mostAndLeastOccurredStates['leastOccurredState']

# Verifica a quantidade de bases por Estado
def countBasesByState(data):
    stateBases = {}
    for row in data:
        state = row['country_state']
        base = row['base']
        if state not in stateBases:
            stateBases[state] = set()
        stateBases[state].add(base)
    stateBaseCount = {state: len(bases) for state, bases in stateBases.items()}
    return stateBaseCount

stateBaseCount = countBasesByState(data)

# Calcula a distribuição percentual de atendimentos entre os Estados
def calculateStatePercentage(states):
    total = sum(states.values())
    percentages = {state: '{:.3f}%'.format((count / total) * 100) for state, count in states.items()}
    return percentages

statePercentages = calculateStatePercentage(stateCounts)

# Exportar os resultados
results = {
    'totalOccurrences': totalOccurrences,
    'totalDays': totalDays,
    'alldates': alldates,
    'monthlyAverages': monthlyAverages,
    'totalMonthlyAverage': totalMonthlyAverage,
    'dailyAverage': dailyAverage,
    'sortedDates': sortedDates,
    'uniqueCountryStates': uniqueCountryStates,
    'polo': polo,
    'stateCounts': stateCounts,
    'baseCount': baseCount,
    'result': result,
    'baseCountsByDate': baseCountsByDate,
    'mostOccurredState': mostOccurredState,
    'leastOccurredState': leastOccurredState,
    'stateBaseCount': stateBaseCount,
    'statePercentages': statePercentages
}


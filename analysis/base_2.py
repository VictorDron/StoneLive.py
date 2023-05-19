import pandas as pd

# Leitura do arquivo XLSX
workbook = pd.read_excel('./database/base_2.xlsx')
data = workbook.values.tolist()

# Retorna os valores da coluna base
def getBaseColumn(data):
    baseColumn = [row[0] for row in data[1:]]
    return baseColumn

BaseColumn = getBaseColumn(data)

# Retorna os valores da coluna de estoque
def getStockColumn(data):
    stockColumn = [row[1] for row in data[1:]]
    return stockColumn

StockColumn = getStockColumn(data)

# Retorna o total de bases
def getTotalBases(data):
    baseColumn = getBaseColumn(data)
    return len(baseColumn)

TotalBases = getTotalBases(data)

# Retorna o total em estoque
def getTotalStock(data):
    stockColumn = getStockColumn(data)
    totalStock = sum(stockColumn)
    return totalStock

TotalStock = getTotalStock(data)

# Retorna a distribuição em percentual de estoque nas bases
def calculateStockDistribution(data):
    baseColumn = getBaseColumn(data)
    stockColumn = getStockColumn(data)

    stockByBase = {}
    totalStock = 0

    for base, stock in zip(baseColumn, stockColumn):
        if base not in stockByBase:
            stockByBase[base] = 0
        stockByBase[base] += stock
        totalStock += stock

    distribution = {}
    for base, stock in stockByBase.items():
        percent = (stock / totalStock) * 100
        distribution[base] = '{:.2f}%'.format(percent)

    return distribution

stockDistribution = calculateStockDistribution(data)

# Retorna o estoque por base
def calculateStockByBase(data):
    baseColumn = getBaseColumn(data)
    stockColumn = getStockColumn(data)

    stockByBase = {}

    for base, stock in zip(baseColumn, stockColumn):
        if base not in stockByBase:
            stockByBase[base] = 0
        stockByBase[base] += stock

    return stockByBase

stockByBase = calculateStockByBase(data)

# Exportar os resultados
results = {
    'BaseColumn': BaseColumn,
    'StockColumn': StockColumn,
    'TotalBases': TotalBases,
    'TotalStock': TotalStock,
    'stockDistribution': stockDistribution,
    'stockByBase': stockByBase
}

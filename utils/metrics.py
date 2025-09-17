def compute_deficit_gdp(revenue, expenditure, gdp):
    return (revenue - expenditure) / gdp

def compute_debt_gdp(debt_stock, gdp):
    return debt_stock / gdp

def primary_balance(revenue, expenditure, interest):
    return revenue - (expenditure - interest)

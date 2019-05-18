class Report:
    revenues: float
    gross_Income: float
    operating_Income: float
    profit_Before_Tax: float
    profit_to_Equity_Holders: float
    earnings_Per_Share: float
    number_of_shares: float
    dividend: float
    intangible_assets: float
    tangible_assets: float
    financial_assets: float
    non_current_assets: float
    cash_and_equivalents: float
    current_assets: float
    total_Assets: float
    total_Equity: float
    non_current_liabilities: float
    current_liabilities: float
    total_Liabilities_And_Equity: float
    net_Debt: float
    cash_flow_from_operating_activities: float
    cash_flow_from_investing_activities: float
    cash_flow_from_financing_activities: float
    cash_flow_for_the_year: float
    free_Cash_Flow: float
    stock_Price_Average: float
    stock_Price_High: float
    stock_Price_Low: float
    currency: str
    report_Start_Date: str
    report_End_Date: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

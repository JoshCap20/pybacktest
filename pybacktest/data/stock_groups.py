# Major Index ETFs
index_tickers = [
    "SPY",  # SPDR S&P 500 ETF Trust
    "QQQ",  # Invesco QQQ Trust (Nasdaq 100)
    "DIA",  # SPDR Dow Jones Industrial Average ETF Trust
    "IWM",  # iShares Russell 2000 ETF
    "EFA",  # iShares MSCI EAFE ETF (Developed Markets)
    "EEM",  # iShares MSCI Emerging Markets ETF
    "AGG",  # iShares Core U.S. Aggregate Bond ETF
    "TLT",  # iShares 20+ Year Treasury Bond ETF
]

# Sector ETFs (Select Sector SPDR Funds)
sector_tickers = {
    "Energy": ["XLE"],  # Energy Select Sector SPDR Fund
    "Materials": ["XLB"],  # Materials Select Sector SPDR Fund
    "Industrials": ["XLI"],  # Industrials Select Sector SPDR Fund
    "Consumer Discretionary": ["XLY"],  # Consumer Discretionary Select Sector SPDR Fund
    "Consumer Staples": ["XLP"],  # Consumer Staples Select Sector SPDR Fund
    "Health Care": ["XLV"],  # Health Care Select Sector SPDR Fund
    "Financials": ["XLF"],  # Financial Select Sector SPDR Fund
    "Information Technology": ["XLK"],  # Technology Select Sector SPDR Fund
    "Communication Services": ["XLC"],  # Communication Services Select Sector SPDR Fund
    "Utilities": ["XLU"],  # Utilities Select Sector SPDR Fund
    "Real Estate": ["XLRE"],  # Real Estate Select Sector SPDR Fund
}

# Major Stocks by Sector with Long Historical Data
stocks_by_sector = {
    "Energy": ["XOM", "CVX", "COP"],  # Exxon Mobil, Chevron, ConocoPhillips
    "Materials": [
        "LIN",
        "APD",
        "SHW",
    ],  # Linde plc, Air Products & Chemicals, Sherwin-Williams
    "Industrials": ["UNP", "HON", "UPS"],  # Union Pacific, Honeywell, UPS
    "Consumer Discretionary": ["AMZN", "HD", "MCD"],  # Amazon, Home Depot, McDonald's
    "Consumer Staples": ["PG", "KO", "PEP"],  # Procter & Gamble, Coca-Cola, PepsiCo
    "Health Care": [
        "JNJ",
        "PFE",
        "UNH",
    ],  # Johnson & Johnson, Pfizer, UnitedHealth Group
    "Financials": ["JPM", "BAC", "WFC"],  # JPMorgan Chase, Bank of America, Wells Fargo
    "Information Technology": ["AAPL", "MSFT", "INTC"],  # Apple, Microsoft, Intel
    "Communication Services": [
        "GOOGL",
        "FB",
        "T",
    ],  # Alphabet (Google), Facebook (Meta), AT&T
    "Utilities": ["NEE", "DUK", "SO"],  # NextEra Energy, Duke Energy, Southern Company
    "Real Estate": ["AMT", "PLD", "CCI"],  # American Tower, Prologis, Crown Castle
}

# Combine all tickers into a single list for backtesting
all_tickers = (
    index_tickers
    + [ticker for tickers in sector_tickers.values() for ticker in tickers]
    + [ticker for tickers in stocks_by_sector.values() for ticker in tickers]
)

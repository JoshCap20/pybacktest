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

SPY_500 = [
    "CNP",
    "FIS",
    "WAT",
    "IR",
    "FITB",
    "AXON",
    "TSLA",
    "EW",
    "FFIV",
    "PARA",
    "ABBV",
    "CAG",
    "DLTR",
    "CTVA",
    "SYK",
    "CMG",
    "MRK",
    "EXC",
    "ABT",
    "CAT",
    "DPZ",
    "MTD",
    "AMP",
    "ZBRA",
    "BXP",
    "JNJ",
    "QRVO",
    "SRE",
    "TT",
    "JBHT",
    "BAX",
    "CPT",
    "KDP",
    "HII",
    "APA",
    "INCY",
    "FTNT",
    "UNP",
    "MLM",
    "BEN",
    "EQT",
    "ES",
    "GOOG",
    "MO",
    "CBRE",
    "WBD",
    "ALB",
    "SOLV",
    "VRSN",
    "XEL",
    "ETN",
    "BMY",
    "CE",
    "CNC",
    "FSLR",
    "AMCR",
    "VRTX",
    "CAH",
    "BALL",
    "PEG",
    "EXPE",
    "USB",
    "HBAN",
    "MRNA",
    "KVUE",
    "SYY",
    "MSCI",
    "MCK",
    "COR",
    "NXPI",
    "HES",
    "TRMB",
    "HIG",
    "VTR",
    "MDT",
    "CEG",
    "K",
    "IVZ",
    "VST",
    "ANET",
    "DG",
    "NRG",
    "AEP",
    "NKE",
    "PKG",
    "CMI",
    "DHI",
    "QCOM",
    "SNA",
    "SPG",
    "MMC",
    "GDDY",
    "MSFT",
    "CCL",
    "LHX",
    "CHTR",
    "MKTX",
    "AJG",
    "MCHP",
    "HUM",
    "PG",
    "NWSA",
    "CRM",
    "TAP",
    "MET",
    "XOM",
    "AMTM",
    "TEL",
    "AES",
    "GS",
    "KMI",
    "LYV",
    "C",
    "MAR",
    "CSCO",
    "NCLH",
    "MCO",
    "AKAM",
    "UHS",
    "PEP",
    "ALLE",
    "CVX",
    "GM",
    "TTWO",
    "CPB",
    "PWR",
    "IP",
    "LW",
    "GPN",
    "WFC",
    "BA",
    "ADM",
    "NTAP",
    "TDY",
    "JKHY",
    "A",
    "AXP",
    "TRGP",
    "STE",
    "CPRT",
    "UDR",
    "ADP",
    "CDW",
    "PH",
    "COO",
    "CSGP",
    "NDAQ",
    "GD",
    "MCD",
    "GEV",
    "EIX",
    "TRV",
    "DE",
    "IDXX",
    "UBER",
    "CTRA",
    "RVTY",
    "MKC",
    "BG",
    "MTB",
    "D",
    "AME",
    "VRSK",
    "KLAC",
    "COST",
    "CF",
    "ATO",
    "APH",
    "CMS",
    "ANSS",
    "AAPL",
    "GLW",
    "AWK",
    "ECL",
    "FDX",
    "CRL",
    "WMT",
    "MPWR",
    "UPS",
    "NOW",
    "OMC",
    "VLTO",
    "BIIB",
    "EQR",
    "PRU",
    "VLO",
    "GIS",
    "IRM",
    "BWA",
    "BSX",
    "CBOE",
    "SW",
    "WYNN",
    "PNC",
    "AIG",
    "MNST",
    "AEE",
    "LLY",
    "GNRC",
    "COF",
    "CINF",
    "XYL",
    "LEN",
    "EQIX",
    "APD",
    "ROK",
    "WDC",
    "MAA",
    "PPL",
    "EL",
    "HD",
    "MA",
    "DOW",
    "PNR",
    "NI",
    "SWKS",
    "HPE",
    "J",
    "BRO",
    "ADSK",
    "NOC",
    "DELL",
    "PYPL",
    "IFF",
    "MHK",
    "AMGN",
    "ROST",
    "BLDR",
    "COP",
    "WTW",
    "ED",
    "ADI",
    "TSN",
    "YUM",
    "NUE",
    "EMN",
    "PFE",
    "UNH",
    "OXY",
    "WST",
    "JCI",
    "CCI",
    "RL",
    "SLB",
    "DOV",
    "OKE",
    "NVR",
    "IQV",
    "IPG",
    "FCX",
    "DLR",
    "HWM",
    "BLK",
    "JPM",
    "ENPH",
    "UAL",
    "SHW",
    "VMC",
    "STT",
    "AVGO",
    "CB",
    "CTAS",
    "NWS",
    "PPG",
    "TDG",
    "FICO",
    "TECH",
    "DAL",
    "HSY",
    "ADBE",
    "PHM",
    "LRCX",
    "MOS",
    "TJX",
    "SJM",
    "TYL",
    "FDS",
    "MAS",
    "HSIC",
    "CMCSA",
    "SO",
    "WY",
    "IBM",
    "AIZ",
    "DUK",
    "CZR",
    "BBY",
    "LNT",
    "BAC",
    "ARE",
    "META",
    "TXN",
    "V",
    "DHR",
    "CLX",
    "HST",
    "DTE",
    "AMD",
    "SNPS",
    "VTRS",
    "RTX",
    "TMO",
    "EFX",
    "PGR",
    "MGM",
    "ACN",
    "FANG",
    "MS",
    "FMC",
    "CRWD",
    "KEYS",
    "BKNG",
    "MTCH",
    "TFX",
    "DXCM",
    "HUBB",
    "GL",
    "ODFL",
    "AMT",
    "WRB",
    "HRL",
    "EVRG",
    "MMM",
    "BX",
    "ICE",
    "TXT",
    "CDNS",
    "GRMN",
    "GE",
    "ALGN",
    "STLD",
    "INTC",
    "ETR",
    "WEC",
    "FAST",
    "PSX",
    "MSI",
    "KEY",
    "STZ",
    "DAY",
    "LULU",
    "WM",
    "EOG",
    "APTV",
    "MPC",
    "CFG",
    "GWW",
    "DRI",
    "L",
    "PLD",
    "EPAM",
    "TGT",
    "INTU",
    "SPGI",
    "FTV",
    "STX",
    "VICI",
    "PTC",
    "LVS",
    "ELV",
    "GILD",
    "LDOS",
    "F",
    "ZBH",
    "HCA",
    "ABNB",
    "KMB",
    "URI",
    "NEM",
    "POOL",
    "KKR",
    "WMB",
    "REGN",
    "ROP",
    "RSG",
    "ACGL",
    "GOOGL",
    "LUV",
    "DVN",
    "SYF",
    "KIM",
    "MU",
    "SBAC",
    "AOS",
    "TSCO",
    "ORLY",
    "GPC",
    "DD",
    "IEX",
    "DOC",
    "CI",
    "TER",
    "ORCL",
    "DVA",
    "FOX",
    "AON",
    "LYB",
    "BDX",
    "AMAT",
    "RJF",
    "GEHC",
    "DFS",
    "NSC",
    "BKR",
    "AMZN",
    "DGX",
    "MRO",
    "TPR",
    "IT",
    "NFLX",
    "ESS",
    "HON",
    "PCG",
    "KHC",
    "SMCI",
    "PANW",
    "LOW",
    # "BRK.B",
    "SBUX",
    "EBAY",
    "LH",
    "NVDA",
    "PAYX",
    "ROL",
    "PSA",
    "CPAY",
    "PODD",
    "JBL",
    "OTIS",
    "PCAR",
    "MDLZ",
    "CARR",
    "FOXA",
    "LMT",
    "CSX",
    "CTLT",
    "HAL",
    "FE",
    "FI",
    "ON",
    # "BF.B",
    "PM",
    "DECK",
    "MOH",
    "CME",
    "AVY",
    "CL",
    "CVS",
    "EMR",
    "LKQ",
    "HOLX",
    "GEN",
    "ALL",
    "EXPD",
    "FRT",
    "WELL",
    "ITW",
    "DIS",
    "EXR",
    "VZ",
    "RCL",
    "TMUS",
    "SWK",
    "WAB",
    "WBA",
    "TFC",
    "CHRW",
    "KR",
    "PLTR",
    "PAYC",
    "BR",
    "ISRG",
    "PNW",
    "AFL",
    "PFG",
    "CTSH",
    "TROW",
    "JNPR",
    "INVH",
    "NEE",
    "AVB",
    "AZO",
    "T",
    "ERIE",
    "HAS",
    "CHD",
    "REG",
    "ULTA",
    "NTRS",
    "SCHW",
    "KO",
    "O",
    "EG",
    "HPQ",
    "RF",
    "BK",
    "LIN",
    "HLT",
    "EA",
    "KMX",
    "NDSN",
    "RMD",
    "ZTS",
]

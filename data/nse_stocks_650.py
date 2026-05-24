"""
NSE Stock Classification Data - 650+ Stocks
Contains Nifty 150, Midcap 200, and Smallcap 300 stocks
Production-grade with current and historical ticker mapping

Features:
- Current NSE ticker symbols (primary)
- Historical ticker fallback for renamed companies
- Prevents duplicate entries in databases
- Graceful handling of company name changes
"""

import yfinance as yf
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# TICKER RENAME MAPPING - Production Grade Historical Data Support
# =============================================================================
# Format: "OLD_TICKER": "NEW_TICKER"
# Used for: Historical data retrieval and preventing duplicates

TICKER_RENAME_MAP = {
    # Company name changes 2022-2026
    "CADILAHC": "ZYDUSLIFE",        # Cadila Healthcare → Zydus Lifesciences (Mar 2022)
    "AMARAJABAT": "ARE&M",          # Amara Raja Batteries → Amara Raja Energy & Mobility
    "SUVENPHAR": "COHANCE",         # Suven Pharmaceuticals → Cohance Lifesciences (May 2025)
    "BURGERKING": "RBA",            # Burger King India → Restaurant Brands Asia (Feb 2022)
    "EQUITAS": "EQUITASBNK",        # Equitas → Equitas Small Finance Bank
    "IDFC": "IDFCFIRSTB",           # IDFC → IDFC FIRST Bank (merged)
    "POLYCA": "POLYCAB",            # Polyca → Polycab India (proper symbol)

    # Mergers and Acquisitions
    "INOXLEISUR": "PVRINOX",        # INOX Leisure merged with PVR → PVR INOX (Feb 2023)

    # Corporate Restructuring / Name Changes
    "MCDOWELL-N": "UNITDSPR",       # United Spirits ticker change (Jun 2024)
    "JUBILANT": "JUBLPHARMA",       # Jubilant Life Sciences → Jubilant Pharmova (after demerger 2021)
    "IIFLSEC": "IIFLCAPS",          # IIFL Securities → IIFL Capital Services (Nov 2024)
    "IIFLWAM": "360ONE",            # IIFL Wealth Management → 360 One WAM (Jan 2023)
    "INFIBEAM": "CCAVENUE",         # Infibeam Avenues → AvenuesAI (Feb 2026)
    "JBM": "JBMA",                  # JBM → JBM Auto Limited
    "LAXMIMACH": "LMW",             # Laxmi Machine Works → LMW
    "MAHINDCIE": "CIEINDIA",        # Mahindra CIE Automotive → CIE Automotive India (2023)
    "MUTHOOTMIC": "MUTHOOTMF",      # Muthoot Microfin → Muthoot Microfin Ltd
    "MEGASOFT": "SIGMAADV",         # Megasoft → Sigma Advanced Systems (Feb 2026)
    "ORIENTREF": "RHIM",            # Orient Refractories → RHI Magnesita India (Jul 2021)
    "PROZONINTU": "PROZONER",       # Prozone Intu Properties → Prozone Realty

    # Tata Motors De-merger (Oct 2025)
    # Old TATAMOTORS split into two entities:
    # - TMPV (Passenger Vehicles + EV + JLR) - continues with historical data
    # - TMCV (Commercial Vehicles) - new listing (Nov 2025)
    # For historical data access, map to TMPV (which inherited the old ticker history)
    # Note: This is a special case - old ticker maps to PV business (TMPV)
    # CV business is now TMCV (new listing, no historical data pre-Oct 2025)

    # Future-proofing: Add more as companies rename
    # "OLD": "NEW",
}

# Reverse mapping for historical data lookup
TICKER_HISTORICAL_MAP = {v: k for k, v in TICKER_RENAME_MAP.items()}

# =============================================================================
# DELISTED STOCKS - Do Not Use
# =============================================================================
DELISTED_STOCKS = {
    # Confirmed Delisted Stocks (Fully Verified as of May 2026)
    "DHFL",          # Dewan Housing Finance - Delisted June 2021 (Bankruptcy)
    "ISEC",          # ICICI Securities - Delisted March 24, 2025 (merged with ICICI Bank)
    "JPINFRATEC",    # Jaypee Infratech - Delisted February 21, 2025 (Bankruptcy/NCLT)
    "KHAITANELE",    # Khaitan Electricals - Liquidation (2019) - Delisted
    "KRIPAINDU",     # Kripa Industries - Operations struck off - Delisted
    "PRESSMAN",      # Pressman Advertising - Merged with Signpost India (Sept 2023) - Delisted
}

# Pump & Dump / Suspicious / High Risk Stocks
# These stocks are technically listed but have red flags (ceased operations, very low volume, penny stocks, etc.)
# Verified as of May 2026
PUMP_AND_DUMP_STOCKS = {
    "INFORMEDIA",    # Infomedia Press - Ceased operations in 2012-13, no business operations, negative net worth
    "JETAIRWAYS",    # Jet Airways - In liquidation (Supreme Court order Nov 2024), suspended trading
    "GTLINFRA",      # GTL Infrastructure - Penny stock (₹1.22), negative book value (-₹4.99), high risk
    "DISHTV",        # Dish TV India - Penny stock (₹3.35), market cap ₹619 Cr, continuous losses
    # Note: TTML (₹42, negative book value -₹102) and IDEA (₹11, negative P/E) are distressed but large market cap
    # Keeping them in main list but flagged as high-risk telecom sector stocks
}

# =============================================================================
# HELPER FUNCTIONS - Production Grade Ticker Resolution
# =============================================================================

def get_current_ticker(ticker):
    """
    Get current NSE ticker symbol (handles renamed companies)

    Args:
        ticker (str): Input ticker symbol (can be old or new)

    Returns:
        str: Current NSE ticker symbol

    Example:
        >>> get_current_ticker("CADILAHC")
        "ZYDUSLIFE"
        >>> get_current_ticker("ZYDUSLIFE")
        "ZYDUSLIFE"
    """
    # If it's an old ticker, return the new one
    if ticker in TICKER_RENAME_MAP:
        return TICKER_RENAME_MAP[ticker]
    # Otherwise return as-is (already current)
    return ticker

def get_historical_ticker(ticker):
    """
    Get historical ticker for fallback data retrieval

    Args:
        ticker (str): Current ticker symbol

    Returns:
        str or None: Historical ticker if exists, None otherwise

    Example:
        >>> get_historical_ticker("ZYDUSLIFE")
        "CADILAHC"
    """
    return TICKER_HISTORICAL_MAP.get(ticker)

def get_all_tickers_for_symbol(ticker):
    """
    Get all ticker variations (current + historical) for comprehensive data retrieval

    Args:
        ticker (str): Input ticker (old or new)

    Returns:
        tuple: (current_ticker, historical_ticker or None)

    Example:
        >>> get_all_tickers_for_symbol("CADILAHC")
        ("ZYDUSLIFE", "CADILAHC")
        >>> get_all_tickers_for_symbol("RELIANCE")
        ("RELIANCE", None)
    """
    current = get_current_ticker(ticker)
    historical = get_historical_ticker(current)
    return (current, historical)

def is_delisted(ticker):
    """Check if stock is delisted"""
    current = get_current_ticker(ticker)
    return current in DELISTED_STOCKS

# Nifty 150 Stocks (Large Cap - Nifty 100 + Nifty Next 50)
NIFTY_150 = [
    # Nifty 100
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", "KOTAKBANK",
    "SBIN", "BHARTIARTL", "BAJFINANCE", "ITC", "ASIANPAINT", "LT", "AXISBANK",
    "DMART", "TITAN", "SUNPHARMA", "ULTRACEMCO", "NESTLEIND", "MARUTI",
    "HCLTECH", "ONGC", "NTPC", "POWERGRID", "WIPRO", "ADANIPORTS", "BAJAJFINSV",
    "COALINDIA", "M&M", "TECHM", "INDUSINDBK", "DRREDDY", "BPCL", "SBILIFE",
    "TATACONSUM", "HINDALCO", "BAJAJ-AUTO", "VEDL", "GODREJCP", "SHREECEM",
    "UPL", "HEROMOTOCO", "INDIGO", "HAVELLS", "ICICIPRULI", "PIDILITIND",
    "TATAPOWER", "HINDPETRO", "DABUR", "SIEMENS", "IOC", "GAIL", "AMBUJACEM",
    "BOSCHLTD", "ADANIPOWER", "DLF", "BANKBARODA", "MARICO", "BERGEPAINT",
    "SRF", "BANDHANBNK", "BEL", "CHOLAFIN", "COLPAL", "TORNTPHARM",
    "TRENT", "SAIL", "MOTHERSON", "LUPIN", "AUROPHARMA", "ACC", "CONCOR",
    "MUTHOOTFIN", "ZYDUSLIFE", "GODREJPROP", "INDIAMART", "CUMMINSIND",
    "LICI", "INDUSTOWER", "ABCAPITAL", "PAGEIND", "NAUKRI", "ALKEM",
    "HAL", "PNB", "ADANIENSOL", "POLYCAB", "TATACOMM", "IDEA",
    "RECLTD", "PFC", "IRFC", "IRCTC", "SOLARINDS", "VOLTAS",
    "FEDERALBNK", "JINDALSTEL", "CANBK", "ABB", "IDFCFIRSTB",
    
    # Nifty Next 50
    "LICHSGFIN", "UNIONBANK", "BIOCON", "SCHAEFFLER", "CROMPTON", "NAVINFLUOR",
    "PETRONET", "ASTRAL", "OBEROIRLTY", "BHARATFORG", "ASHOKLEY", "ZEEL",
    "MPHASIS", "PERSISTENT", "COFORGE", "SONACOMS", "CHAMBLFERT", "M&MFIN",
    "POONAWALLA", "BATAINDIA", "GODREJIND", "JUBLFOOD", "BALKRISIND", "ESCORTS",
    "SUNDRMFAST", "AIAENG", "EXIDEIND", "APOLLOTYRE", "CESC", "MRF",
    "PIIND", "LINDEINDIA", "SUPREMEIND", "PHOENIXLTD", "COROMANDEL", "KAJARIACER",
    "CGPOWER", "DIXON", "SJVN", "NHPC", "NMDC", "ABFRL", "RBLBANK",
    "MAXHEALTH", "BHEL", "OFSS", "PRESTIGE", "SBICARD", "HONAUT"
]

# Midcap 200 Stocks
MIDCAP_200 = [
    "KPITTECH", "DEEPAKNTR", "IIFL", "LTTS", "TVSMOTOR", "IPCALAB", "GLAXO",
    "SUNDARMFIN", "PGHH", "BLUESTARCO", "CLEAN", "3MINDIA", "SYNGENE", "AUBANK",
    "MANAPPURAM", "CREDITACC", "CENTRALBK", "TATACHEM", "NATIONALUM", "GNFC",
    "UBL", "ICICIGI", "IGL", "KANSAINER", "GRINDWELL", "IEX", "IREDA",
    "TIINDIA", "RELAXO", "DELTACORP", "RAJESHEXPO", "GRAPHITE", "RAIN",
    "JKCEMENT", "LAURUSLABS", "ZENSARTECH", "INDHOTEL", "FORTIS", "SUMICHEM",
    "NATCOPHARM", "RVNL", "CDSL", "AAVAS", "FLUOROCHEM", "KEI", "RADICO",
    "MOTILALOFS", "JBCHEPHARM", "CAPLIPOINT", "GICRE", "VBL", "ANGELONE",
    "SAFARI", "IRCON", "MAZDOCK", "RITES", "BEML", "GRSE", "COCHINSHIP",
    "RAILTEL", "HAPPSTMNDS", "NEWGEN", "INTELLECT", "KIMS", "RAINBOW", "MEDPLUS",
    "LXCHEM", "ANURAS", "TATVA", "RELIGARE", "HFCL", "GTLINFRA", "TTML",
    "BHARTIHEXA", "JYOTHYLAB", "VGUARD", "SYMPHONY", "AMBER", "BASF", "FINCABLES",
    "KEC", "CEATLTD", "JKTYRE", "MGL", "GUJGASLTD", "SKFINDIA", "TIMKEN",
    "GREAVESCOT", "IFBIND", "KNRCON", "PNC", "NESCO", "SOBHA", "BRIGADE",
    "MAHLIFE", "SUNTV", "PVRINOX", "SAREGAMA", "CENTURYPLY", "GREENPANEL", "GPPL",
    "JKLAKSHMI", "STARCEMENT", "HEIDELBERG", "RAMCOCEM", "JKPAPER", "TNPL",
    "HINDZINC", "WELCORP", "BIRLACORPN", "JSWHL", "RESPONIND", "GMDCLTD",
    "MOIL", "NETWORK18", "GATEWAY", "HATHWAY", "NAVNETEDUL", "MASTEK", "SONATSOFTW",
    "CYIENT", "RATEGAIN", "DATAMATICS", "VRLLOG", "MAHLOG", "TCI", "BLUEDART",
    "CARBORUNIV", "EIDPARRY", "RAJRATAN", "NOCIL", "AKZOINDIA", "ATUL", "HIKAL",
    "BALRAMCHIN", "DCMSHRIRAM", "THYROCARE", "VIJAYA", "SUDARSCHEM", "ALKYLAMINE",
    "TARSONS", "GHCL", "GALAXYSURF", "PFIZER", "ABBOTINDIA", "SANOFI", "GRANULES",
    "GLENMARK", "RENUKA", "BAJAJHLDNG", "GESHIP", "GODFRYPHLP", "MAHSCOOTER",
    "SUZLON", "JSWENERGY", "TORNTPOWER", "ADANIGREEN", "FINEORG", "CIPLA",
    "APLAPOLLO", "ROSSARI", "ROUTE", "METROPOLIS",
    # Additional Midcap 200 stocks
    "CRISIL", "POLYCAB", "NLCINDIA", "SULA", "KALYANKJIL", "TATAELXSI", "QUESS",
    "AETHER", "MIDHANI", "MMTC", "MSTCLTD", "NBCC", "NATIONALUM",
    "OIL", "ORIENTELEC", "PDSL", "PGHL", "PRINCEPIPE", "PRAJIND",
    "RAMCOCEM", "RATNAMANI", "RAYMOND", "REDINGTON", "RELAXO", "RITES",
    "ROUTE", "RCF", "SAIL", "SARDAEN", "SCHNEIDER", "SEQUENT",
    "SHARDACROP", "SHILPAMED", "SHOPERSTOP", "SHREECEM", "SHRIRAMFIN", "SIEMENS",
    "SJVN", "SOLARINDS", "SONACOMS", "SPARC", "SRF", "STARCEMENT",
    "SUMICHEM", "SUNDARAM", "SUNDRMFAST", "SUPRAJIT", "SUPREMEIND", "COHANCE",
    "SYMPHONY", "TANLA", "TATACHEM", "TATACOMM", "TATAELXSI",
    "TATAINVEST", "TMPV", "TMCV", "TATAPOWER", "TEAMLEASE", "TECHM",
    # TMPV = Tata Motors PV (was TATAMOTORS pre-Oct 2025, has historical data)
    # TMCV = Tata Motors CV (new listing Nov 2025, no historical data)
    "TEGA", "THERMAX", "THYROCARE", "TIINDIA", "TIMKEN", "TITAGARH"
]

# Smallcap 300 Stocks
SMALLCAP_300 = [
    "AARTIIND", "AARTIDRUGS", "AAVAS", "ABB", "ABBOTINDIA", "ABCAPITAL", "ABFRL",
    "ABSLAMC", "ACC", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANIPOWER",
    "AFFLE", "AGARIND", "AHLEAST",
    "AIAENG", "AJANTPHARM", "AKZOINDIA", "ALKYLAMINE", "ALLCARGO", "ALOKINDS",
    "ARE&M", "AMBER", "AMBUJACEM", "ANGELONE", "ANURAS", "APCOTEXIND",
    "APLAPOLLO", "APOLLOHOSP", "APOLLOPIPE", "APOLLOTYRE", "APTUS", "ARCHIDPLY",
    "ASAHIINDIA", "ASHAPURMIN", "ASHIANA", "ASHOKA", "ASIANPAINT", "ASTEC",
    "ASTERDM", "ASTRAZEN", "ASTRAL", "ATUL", "AUROPHARMA", "AUBANK",
    "AVALON", "AVANTIFEED", "AXISBANK", "BAJAJ-AUTO", "BAJAJCON", "BAJAJFINSV",
    "BAJAJHLDNG", "BAJFINANCE", "BALAMINES", "BALAJITELE", "BALKRISIND", "BALRAMCHIN",
    "BANCOINDIA", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "BASF", "BATAINDIA",
    "BBL", "BBTC", "BDL", "BEL", "BEML", "BERGEPAINT",
    "BFUTILITIE", "BGRENERGY", "BHARATFORG", "BHARATGEAR", "BHARTIARTL", "BHARTIHEXA",
    "BHEL", "BIRLACORPN", "BLAL", "BLISSGVS", "BLUEDART", "BLUESTARCO",
    "BODALCHEM", "BOSCHLTD", "BPCL", "BRIGADE", "BRITANNIA", "RBA",
    "BUTTERFLY", "ZYDUSLIFE", "CAMS", "CANFINHOME", "CANBK", "CAPLIPOINT",
    "CARBORUNIV", "CARERATING", "CARTRADE", "CASTROLIND", "CCL", "CEATLTD",
    "CENTENKA", "CENTRALBK", "CENTURYPLY", "CENTURYTEX", "CERA", "CESC",
    "CGPOWER", "CHALET", "CHAMBLFERT", "CHEMCON", "CHENNPETRO",
    "CHOLAFIN", "CHOLAHLDNG", "CIPLA", "CLEAN", "COALINDIA", "COCHINSHIP",
    "COFFEEDAY", "COFORGE", "COLPAL", "CONCOR", "COROMANDEL", "CREDITACC",
    "CRISIL", "CROMPTON", "CUB", "CUMMINSIND", "CYIENT", "DABUR",
    "DALBHARAT", "DATAMATICS", "DBCORP", "DBL", "DBREALTY", "DCBBANK",
    "DCMSHRIRAM", "DEEPAKFERT", "DEEPAKNTR", "DELTACORP", "DEN", "DEVYANI",
    "DHANUKA", "DHARSUGAR", "DISHTV", "DIVISLAB",
    "DIXON", "DLF", "DMART", "DOLLAR", "DREAMFOLKS", "DRREDDY",
    "DSSL", "DTIL", "EDELWEISS", "EICHERMOT", "EIDPARRY", "EIHOTEL",
    "ELECON", "ELGIEQUIP", "EMAMILTD", "ENDURANCE", "ENGINERSIN", "EQUITASBNK",
    "ERIS", "EROSMEDIA", "ESCORTS", "EVEREADY", "EXCELINDUS",
    "EXIDEIND", "FAIRCHEMOR", "FCL", "FEDERALBNK", "FDC", "FINEORG",
    "FINPIPE", "FINCABLES", "FIRSTCRY", "FIVESTAR", "FLUOROCHEM", "FORTIS",
    "FUSION", "GAEL", "GAIL", "GALAXYSURF", "GARFIBRES",
    "GATEWAY", "GESHIP", "GFLLIMITED", "GHCL", "GICRE",
    "GILLETTE", "GLAND", "GLAXO", "GLENMARK", "GLOBUSSPR", "GMMPFAUDLR",
    "GMDCLTD", "GNFC", "GOACARBON", "GODFRYPHLP", "GODREJAGRO", "GODREJCP",
    "GODREJIND", "GODREJPROP", "GOKEX", "GOKUL", "GPIL", "GPPL",
    "GRANULES", "GRAPHITE", "GRASIM", "GREENPANEL", "GREENPLY", "GREAVESCOT",
    "GRINDWELL", "GRSE", "GSFC", "GSPL", "GTLINFRA", "GUFICBIO",
    "GUJALKALI", "GUJGASLTD", "GULFOILLUB", "HAL", "HAPPSTMNDS", "HATHWAY",
    "HAVELLS", "HCLTECH", "HCG", "HDFCAMC", "HDFCBANK", "HDFCLIFE",
    "HEIDELBERG", "HERANBA", "HERITGFOOD", "HEROMOTOCO", "HESTERBIO", "HFCL", "HIKAL",
    "HINDALCO", "HINDCOPPER", "HINDPETRO", "HINDUNILVR", "HINDZINC", "HLEGLAS",
    "HMT", "HMVL", "HOMEFIRST", "HONAUT", "HSCL", "HUDCO", "ICICIBANK",
    "ICICIGI", "ICICIPRULI", "ICICISEC", "IDBI", "IDEA", "IDFCFIRSTB",
    "IEX", "IFBIND", "IFCI", "IIFL", "IIFLSEC", "IIFLWAM", "IITL",
    "INDBANK", "INDIGOPNTS", "INDIGO", "INDHOTEL", "INDIACEM", "INDIAMART", "INDIANB",
    "INDIANHUME", "INDNIPPON", "INDOCO", "INDOSTAR", "INDOTECH", "INDRAMEDCO", "INDSWFTLAB",
    "INDUSTOWER", "INFIBEAM", "INFORMEDIA", "INFY", "INGERRAND", "INOXGREEN", "PVRINOX",  # PVRINOX (was INOXLEISUR, merged with PVR)
    "INOXWIND", "INSECTICID", "INTELLECT", "IOB", "IOC", "IPCALAB", "IRCON",
    "IRCTC", "IREDA", "IRFC", "IRIS", "IRISDOREME", "ISEC", "ITC",
    "ITDCEM", "ITI", "IVC", "IVP", "JAGRAN", "JAGSNPHARM", "JAMNAAUTO",
    "JAYAGROGN", "JBM", "JBMA", "JCHAC", "JETAIRWAYS", "JKCEMENT", "JKLAKSHMI",
    "JKPAPER", "JKTYRE", "JMA", "JMFINANCIL", "JPASSOCIAT", "JPINFRATEC", "JPPOWER",
    "JSL", "JSLHISAR", "JSWENERGY", "JSWHL", "JSWSTEEL", "JUBLPHARMA", "JUBLFOOD",  # JUBLPHARMA (was JUBILANT)
    "JUSTDIAL", "JYOTHYLAB", "KAJARIACER", "KALYANKJIL", "KANSAINER", "KARMAENG", "KARURVYSYA",
    "KCP", "KDDL", "KEC", "KEI", "KEYFINSERV", "KFINTECH", "KHADIM",
    "KHAITANELE", "KILITCH", "KIMS", "KINGFA", "KIRLOSENG", "KIRLPNU", "KITEX",
    "KKC", "KNRCON", "KOLTEPATIL", "KOPRAN", "KOTAKBANK", "KPITTECH", "KRBL",
    "KREBSBIO", "KRIPAINDU", "KRISHANA", "KSBL", "KSL", "LALPATHLAB", "LAMBODHARA",
    "LATENTVIEW", "LAXMIMACH", "LEMONTREE", "LICI", "LICHSGFIN", "LINDEINDIA", "LT",
    "LTFOODS", "LTIM", "LTTS", "LUMAXTECH", "LUPIN", "LUXIND", "LXCHEM",
    "LYKALABS", "MAANALU", "MAHABANK", "MAHAPEXLTD", "MAHINDCIE", "MAHLIFE", "MAHLOG",
    "MAHSCOOTER", "MAHSEAMLES", "MAITHANALL", "MAKEINDIA", "MALUPAPER", "MANALIPETC", "MANAPPURAM",
    "MANGLMCEM", "MANINDS", "MANINFRA", "MANKIND", "MAPMYINDIA", "MARICO", "MARKSANS",
    "MARUTI", "MASTEK", "MATRIMONY", "MAXHEALTH", "MAXIND", "MAYURUNIQ", "MAZDA",
    "MAZDOCK", "UNITDSPR", "MCX", "MEDANTA", "MEDPLUS", "MEGASOFT", "MEP",  # UNITDSPR (was MCDOWELL-N)
    "METAL", "METROPOLIS", "MGL", "MHRIL", "MIDHANI", "MINDACORP", "MINDAIND",
    "MINDSPACE", "MISC", "MMTC", "MOIL", "MOL", "MOLDTKPAC", "MONARCH",
    "MOREPENLAB", "MOTHERSON", "MOTILALOFS", "MPHASIS", "MPSLTD", "MRF", "MRPL",
    "MSUMI", "MSTCLTD", "MTARTECH", "MUTHOOTFIN", "MUTHOOTMIC", "NACLIND", "NATIONALUM",
    "NAUKRI", "NAVINFLUOR", "NAVKARCORP", "NAVNETEDUL", "NAZARA", "NBCC", "NCC",
    "NDTV", "NELCAST", "NELCO", "NEOGEN", "NESCO", "NESTLEIND", "NETWORK18",
    "NEULANDLAB", "NEWGEN", "NFL", "NH", "NHPC", "NIACL", "NIITLTD",
    "NLCINDIA", "NMDC", "NOCIL", "NSLNISP", "NTPC", "NUVOCO", "OBEROIRLTY",
    "OFSS", "OIL", "OLECTRA", "OMAXE", "ONEPOINT", "ONGC", "ONMOBILE",
    "ORIENTALTL", "ORIENTBELL", "ORIENTCEM", "ORIENTELEC", "ORIENTHOT", "ORIENTREF", "ORISSAMINE",
    "PANAMAPET", "PANCHMAHAL", "PANACEABIO", "PARACABLES", "PARAGMILK", "PARAS", "PARSVNATH",
    "PATELENG", "PATINTLOG", "PCJEWELLER", "PDSL", "PEARLPOLY", "PEL", "PERSISTENT",
    "PETRONET", "PFC", "PFIZER", "PGEL", "PGHH", "PGHL", "PHOENIXLTD",
    "PIDILITIND", "PIIND", "PIL", "PILANIINVS", "PNBGILTS", "PNB", "PNC",
    "PNCINFRA", "POLYCAB", "POLYMED", "POLYPLEX", "POONAWALLA", "POWERGRID", "POWERINDIA",
    "PRAENG", "PRAJIND", "PRAKASH", "PRECAM", "PRECOT", "PREMEXPLN", "PRESSMAN",
    "PRESTIGE", "PRISMX", "PRIVISCL", "PROZONINTU", "PSPPROJECT", "PTC", "PURVA",
    "PVP", "PVRINOX", "QUICKHEAL", "QUESS", "RADICO", "RADIOCITY", "RAIN"
]

def validate_stock_data(ticker, try_historical=True):
    """
    Production-grade validation with fallback to historical ticker

    Args:
        ticker (str): Ticker symbol to validate
        try_historical (bool): If True, try historical ticker as fallback

    Returns:
        bool: True if valid data found, False otherwise

    Logic:
        1. Try current ticker (e.g., ZYDUSLIFE)
        2. If fails and try_historical=True, try old ticker (e.g., CADILAHC)
        3. Handles renamed companies gracefully
    """
    # Check if delisted
    if is_delisted(ticker):
        logger.debug(f"{ticker} is delisted, skipping")
        return False

    # Get current ticker
    current_ticker = get_current_ticker(ticker)

    # Try current ticker first
    try:
        stock = yf.Ticker(f"{current_ticker}.NS")
        df = stock.history(period="1mo")
        if not df.empty and len(df) >= 5:
            return True
    except Exception as e:
        logger.debug(f"Current ticker {current_ticker}.NS failed: {str(e)[:50]}")

    # Fallback: Try historical ticker if available
    if try_historical:
        historical_ticker = get_historical_ticker(current_ticker)
        if historical_ticker:
            try:
                stock = yf.Ticker(f"{historical_ticker}.NS")
                df = stock.history(period="1mo")
                if not df.empty and len(df) >= 5:
                    logger.info(f"✓ {current_ticker} found via historical ticker {historical_ticker}")
                    return True
            except Exception as e:
                logger.debug(f"Historical ticker {historical_ticker}.NS also failed: {str(e)[:50]}")

    return False

def fetch_stock_data_with_fallback(ticker, period="1y", min_days=5):
    """
    Production-grade data fetching with automatic fallback and graceful error handling

    Args:
        ticker (str): Ticker symbol
        period (str): Data period (default: 1y)
        min_days (int): Minimum days of data required for validation (default: 5)

    Returns:
        tuple: (yfinance.Ticker object or None, actual_ticker_used, success: bool, error_message: str or None)

    Return Values:
        - (stock, ticker, True, None) - Success with primary ticker
        - (stock, ticker, True, "Using fallback") - Success with historical ticker
        - (None, ticker, False, "error message") - Failed (both tickers failed)

    Error Handling:
        ✅ Never crashes - always returns a tuple
        ✅ Tries primary ticker first
        ✅ Falls back to historical ticker if primary fails
        ✅ Returns None if both fail (caller can skip gracefully)

    Example:
        >>> stock, ticker, success, msg = fetch_stock_data_with_fallback("ZYDUSLIFE")
        >>> if success:
        >>>     hist = stock.history(period="1y")
        >>> else:
        >>>     print(f"Skipping {ticker}: {msg}")
    """
    current_ticker = get_current_ticker(ticker)
    historical_ticker = get_historical_ticker(current_ticker)

    # ATTEMPT 1: Try current/primary ticker
    try:
        stock = yf.Ticker(f"{current_ticker}.NS")
        df = stock.history(period="5d")  # Quick validation check

        if not df.empty and len(df) >= min_days:
            logger.debug(f"✓ {current_ticker}: Primary ticker OK ({len(df)} days)")
            return stock, current_ticker, True, None
        else:
            logger.debug(f"⚠ {current_ticker}: Primary ticker has insufficient data ({len(df)} days)")

    except Exception as e:
        logger.debug(f"⚠ {current_ticker}: Primary ticker failed - {str(e)[:100]}")

    # ATTEMPT 2: Try historical/fallback ticker (only if exists)
    if historical_ticker:
        try:
            logger.info(f"🔄 {current_ticker}: Trying fallback ticker {historical_ticker}...")
            stock = yf.Ticker(f"{historical_ticker}.NS")
            df = stock.history(period="5d")  # Quick validation check

            if not df.empty and len(df) >= min_days:
                logger.info(f"✓ {current_ticker}: Fallback ticker {historical_ticker} OK ({len(df)} days)")
                return stock, current_ticker, True, f"Using fallback ticker {historical_ticker}"
            else:
                logger.warning(f"⚠ {current_ticker}: Fallback ticker {historical_ticker} has insufficient data ({len(df)} days)")

        except Exception as e:
            logger.warning(f"⚠ {current_ticker}: Fallback ticker {historical_ticker} failed - {str(e)[:100]}")

    # BOTH FAILED: Return None to signal caller to skip this stock
    error_msg = f"No data available (tried {current_ticker}.NS"
    if historical_ticker:
        error_msg += f" and {historical_ticker}.NS"
    error_msg += ")"

    logger.error(f"❌ {current_ticker}: {error_msg}")
    return None, current_ticker, False, error_msg

def fetch_stock_history_safe(ticker, period="1y", **kwargs):
    """
    Ultra-safe wrapper for fetching stock history with comprehensive error handling

    Args:
        ticker (str): Ticker symbol
        period (str): History period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        **kwargs: Additional arguments passed to stock.history()

    Returns:
        tuple: (DataFrame or None, ticker, success: bool, error_message: str or None)

    Return Values:
        - (DataFrame, ticker, True, None) - Success
        - (None, ticker, False, "error message") - Failed

    Features:
        ✅ Never crashes - always returns a tuple
        ✅ Tries primary → fallback ticker
        ✅ Returns empty DataFrame as None for consistency
        ✅ Detailed error messages for debugging

    Example:
        >>> hist, ticker, success, msg = fetch_stock_history_safe("ZYDUSLIFE", period="1y")
        >>> if success:
        >>>     print(f"Got {len(hist)} days of data for {ticker}")
        >>> else:
        >>>     print(f"Failed for {ticker}: {msg}")
        >>>     continue  # Move to next stock
    """
    try:
        # Use the fallback mechanism
        stock, ticker_name, success, msg = fetch_stock_data_with_fallback(ticker)

        if not success:
            # Both primary and fallback failed
            return None, ticker_name, False, msg

        # Fetch the requested history period
        try:
            hist = stock.history(period=period, **kwargs)

            if hist is None or hist.empty:
                error_msg = f"No historical data for period '{period}'"
                logger.warning(f"⚠ {ticker_name}: {error_msg}")
                return None, ticker_name, False, error_msg

            logger.debug(f"✓ {ticker_name}: Fetched {len(hist)} days of data (period: {period})")
            return hist, ticker_name, True, None

        except Exception as e:
            error_msg = f"Error fetching history: {str(e)[:100]}"
            logger.error(f"❌ {ticker_name}: {error_msg}")
            return None, ticker_name, False, error_msg

    except Exception as e:
        # Catch-all for unexpected errors
        current = get_current_ticker(ticker)
        error_msg = f"Unexpected error: {str(e)[:100]}"
        logger.error(f"❌ {current}: {error_msg}")
        return None, current, False, error_msg

def fetch_stock_info_safe(ticker):
    """
    Ultra-safe wrapper for fetching stock info with comprehensive error handling

    Args:
        ticker (str): Ticker symbol

    Returns:
        tuple: (dict or None, ticker, success: bool, error_message: str or None)

    Return Values:
        - (info_dict, ticker, True, None) - Success
        - (None, ticker, False, "error message") - Failed

    Features:
        ✅ Never crashes
        ✅ Tries primary → fallback ticker
        ✅ Returns None on failure

    Example:
        >>> info, ticker, success, msg = fetch_stock_info_safe("ZYDUSLIFE")
        >>> if success:
        >>>     print(f"Company: {info.get('longName')}")
        >>> else:
        >>>     print(f"Failed for {ticker}: {msg}")
        >>>     continue
    """
    try:
        stock, ticker_name, success, msg = fetch_stock_data_with_fallback(ticker)

        if not success:
            return None, ticker_name, False, msg

        try:
            info = stock.info

            if not info:
                error_msg = "No company info available"
                logger.warning(f"⚠ {ticker_name}: {error_msg}")
                return None, ticker_name, False, error_msg

            logger.debug(f"✓ {ticker_name}: Fetched company info")
            return info, ticker_name, True, None

        except Exception as e:
            error_msg = f"Error fetching info: {str(e)[:100]}"
            logger.error(f"❌ {ticker_name}: {error_msg}")
            return None, ticker_name, False, error_msg

    except Exception as e:
        current = get_current_ticker(ticker)
        error_msg = f"Unexpected error: {str(e)[:100]}"
        logger.error(f"❌ {current}: {error_msg}")
        return None, current, False, error_msg

def get_all_stocks_with_classification():
    """
    Returns all NSE stocks with their CURRENT classification

    Production Features:
    - Automatically converts old tickers to current (e.g., CADILAHC → ZYDUSLIFE)
    - Removes delisted stocks
    - Prevents duplicates (old + new ticker for same company)
    - Returns only current NSE symbols

    Returns:
        List of tuples: [(current_ticker, cap_size), ...]

    Example:
        [("ZYDUSLIFE", "Large Cap"), ("RELIANCE", "Large Cap"), ...]
    """
    all_stocks = []

    # Add Nifty 150 (Large Cap)
    for ticker in NIFTY_150:
        current = get_current_ticker(ticker)
        if not is_delisted(current):
            all_stocks.append((current, "Large Cap"))

    # Add Midcap 200
    for ticker in MIDCAP_200:
        current = get_current_ticker(ticker)
        if not is_delisted(current):
            all_stocks.append((current, "Mid Cap"))

    # Add Smallcap 300
    for ticker in SMALLCAP_300:
        current = get_current_ticker(ticker)
        if not is_delisted(current):
            all_stocks.append((current, "Small Cap"))

    # Remove duplicates (keep first occurrence with highest market cap classification)
    # Priority: Large Cap > Mid Cap > Small Cap
    seen = {}
    cap_priority = {"Large Cap": 1, "Mid Cap": 2, "Small Cap": 3}

    for ticker, cap in all_stocks:
        if ticker not in seen:
            seen[ticker] = cap
        else:
            # Keep the higher priority classification
            if cap_priority[cap] < cap_priority[seen[ticker]]:
                seen[ticker] = cap

    unique_stocks = [(ticker, cap) for ticker, cap in seen.items()]

    logger.info(f"Total unique stocks (current tickers only): {len(unique_stocks)}")
    return unique_stocks

def get_validated_stocks():
    """
    Returns only stocks that have valid data on Yahoo Finance
    This may take time on first run - results should be cached
    """
    all_stocks = get_all_stocks_with_classification()
    validated = []

    logger.info(f"Validating {len(all_stocks)} stocks against Yahoo Finance...")

    for i, (ticker, cap) in enumerate(all_stocks, 1):
        if i % 50 == 0:
            logger.info(f"Validated {i}/{len(all_stocks)} stocks...")

        if validate_stock_data(ticker):
            validated.append((ticker, cap))
        else:
            logger.warning(f"Removing {ticker} - insufficient data")

    logger.info(f"Validation complete: {len(validated)}/{len(all_stocks)} stocks valid")
    return validated

# Cache for validated stocks
_validated_cache = None

def get_stocks_cached():
    """Get stocks with caching to avoid repeated validation"""
    global _validated_cache
    if _validated_cache is None:
        _validated_cache = get_validated_stocks()
    return _validated_cache

# =============================================================================
# PRODUCTION-GRADE HELPER FOR BOTS
# =============================================================================

def get_stock_for_notion(ticker):
    """
    Get the CURRENT ticker that should be used in Notion database

    This ensures:
    - Only one entry per company in Notion
    - Always uses current NSE symbol
    - No duplicates from old/new ticker names

    Args:
        ticker (str): Input ticker (can be old or new)

    Returns:
        str: Current ticker to use in Notion

    Example:
        >>> get_stock_for_notion("CADILAHC")
        "ZYDUSLIFE"
        >>> get_stock_for_notion("ZYDUSLIFE")
        "ZYDUSLIFE"
    """
    return get_current_ticker(ticker)

# =============================================================================
# USAGE GUIDE FOR BOT DEVELOPERS - PRODUCTION GRADE (NEVER CRASHES)
# =============================================================================
"""
🚀 PRODUCTION-GRADE BOT IMPLEMENTATION GUIDE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METHOD 1: RECOMMENDED - Ultra-Safe Wrappers (NEVER CRASHES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from data.nse_stocks_650 import (
    get_all_stocks_with_classification,
    fetch_stock_history_safe,
    fetch_stock_info_safe,
    get_stock_for_notion
)

# Get all stocks (current tickers only, no duplicates)
stocks = get_all_stocks_with_classification()

stats = {"success": 0, "failed": 0, "skipped": 0}

for ticker, cap_size in stocks:
    print(f"Processing {ticker}...")

    # SAFE: Fetch historical data (tries primary → fallback, never crashes)
    hist, ticker_name, success, error_msg = fetch_stock_history_safe(ticker, period="1y")

    if not success:
        # Gracefully handle failure - log and move on
        print(f"⚠️ Skipping {ticker_name}: {error_msg}")
        stats["skipped"] += 1
        continue  # ✅ Move to next stock, bot doesn't crash

    # SAFE: Fetch company info
    info, ticker_name, success, error_msg = fetch_stock_info_safe(ticker)

    if not success:
        print(f"⚠️ Partial data for {ticker_name}: {error_msg}")
        # You can still use historical data even if info fails

    # Process data (hist is guaranteed to be valid DataFrame here)
    price = hist['Close'].iloc[-1]
    volume = hist['Volume'].sum()

    # Always use current ticker for Notion (prevents duplicates)
    notion_ticker = get_stock_for_notion(ticker_name)

    # Send to Notion
    try:
        send_to_notion({
            "ticker": notion_ticker,  # ✅ Always current symbol
            "market_cap": cap_size,
            "price": price,
            "volume": volume,
            "company": info.get("longName") if info else "N/A"
        })
        stats["success"] += 1
    except Exception as e:
        print(f"❌ Notion error for {notion_ticker}: {e}")
        stats["failed"] += 1
        continue  # ✅ Move to next stock

print(f"\n📊 Stats: {stats}")
# ✅ Bot completed without crashing!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METHOD 2: Advanced - Manual Fallback Control
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from data.nse_stocks_650 import (
    get_all_stocks_with_classification,
    fetch_stock_data_with_fallback,
    get_stock_for_notion
)

stocks = get_all_stocks_with_classification()

for ticker, cap_size in stocks:
    # Returns: (stock_obj or None, ticker, success, error_msg)
    stock, ticker_name, success, error_msg = fetch_stock_data_with_fallback(ticker)

    if not success:
        print(f"⚠️ Skipping {ticker_name}: {error_msg}")
        continue  # ✅ Move to next stock

    # Now you have a valid stock object, fetch what you need
    try:
        hist = stock.history(period="1y")
        info = stock.info

        if hist.empty:
            print(f"⚠️ No historical data for {ticker_name}")
            continue

        # Process...

    except Exception as e:
        print(f"❌ Error processing {ticker_name}: {e}")
        continue  # ✅ Always continue to next stock

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY PRINCIPLES (NEVER CRASH)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ ALWAYS check success flag before using data
2. ✅ ALWAYS use try-except around data processing
3. ✅ ALWAYS continue to next stock on error
4. ✅ ALWAYS use get_stock_for_notion() before sending to database
5. ✅ NEVER assume data exists - always validate

FLOW:
1. Primary ticker (ZYDUSLIFE) → Try fetch data
2. If fails → Fallback ticker (CADILAHC) → Try fetch data
3. If both fail → Return None, log error, continue to next stock
4. ✅ Bot never crashes, always completes

NOTION DATABASE:
- Only current tickers stored (e.g., ZYDUSLIFE)
- No duplicates (no CADILAHC + ZYDUSLIFE entries)
- Single source of truth

BENEFITS:
✅ Production-ready error handling
✅ Never crashes on missing data
✅ Automatic primary → fallback logic
✅ No duplicate entries in database
✅ Comprehensive logging for debugging
✅ Future-proof for company renames
"""

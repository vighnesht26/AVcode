"""All settings and assumptions in ONE place. Edit here, not in the other files."""
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).parent / "data"))  
TRADE_CSV = DATA_DIR / "merged_master_trade_data2.csv"
IO_XLSX = DATA_DIR / "MoSPI_Industry_Input_Output_Matrices23.xlsx"
IO_SHEET = "A_2023"  # 66x66 coefficient matrix sheet


SPREAD_STRENGTH = 0.6   
SPREAD_ROUNDS = 4        
DEFAULT_REFILL = 0.3     


CONCORDANCE = {
    2709: ("Crude Petroleum", .88), 2711: ("Natural Gas", .50), 2701: ("Coal & Lignite", .25),
    85: ("Manufacture of electronic component", .50), 84: ("Manufacture of machinery", .35), 71: ("Other Manufacturing", .60),
    29: ("Manufacture of chemical and chemical", .30), 39: ("Manufacture of rubber & plastic", .15),
    28: ("Manufacture of chemical and chemical", .20), 31: ("Agriculture", .15), 72: ("Manufacture of Basic Iron", .08),
    87: ("Manufacture of Transport", .06), 15: ("Production, processing", .40), 7: ("Agriculture", .05),
}


GULF_COUNTRIES = ["Iraq", "Saudi Arabia", "United Arab Emirates", "Kuwait", "Qatar", "Oman", "Iran"]
GULF_TRIGGERS = ["hormuz", "strait", "gulf", "persian gulf", "middle east", "west asia"]
WAR_WORDS = ["war", "conflict", "attack", "strike", "invasion", "blockade", "sanction"]
COUNTRY_ALIASES = {"russia": "Russian Federation", "usa": "USA", "united states": "USA", "america": "USA", "uae": "United Arab Emirates",
    "emirates": "United Arab Emirates", "korea": "Rep. of Korea", "south korea": "Rep. of Korea", "saudi": "Saudi Arabia", "turkey": "Türkiye",
    "turkiye": "Türkiye", "vietnam": "Viet Nam", "hong kong": "China, Hong Kong SAR", "taiwan": "Other Asia, nes", "tanzania": "United Rep. of Tanzania",
    "uk": "United Kingdom", "britain": "United Kingdom", "bolivia": "Bolivia (Plurinational State of)"}
COMMODITY_KEYWORDS = {   # phrase -> HS codes (longer phrases are matched first)
    "edible oil": [15], "vegetable oil": [15], "cooking oil": [15], "palm oil": [15], "sunflower oil": [15],
    "crude oil": [2709], "crude": [2709], "petroleum": [2709], "petrol": [2709], "diesel": [2709], "oil": [2709],
    "natural gas": [2711], "lng": [2711], "lpg": [2711], "gas": [2711], "coal": [2701],
    "electronics": [85], "electronic": [85], "phone": [85], "semiconductor": [85], "chip": [85],
    "machinery": [84], "machine": [84], "gold": [71], "diamond": [71], "gem": [71], "jewel": [71],
    "chemical": [29, 28], "plastic": [39], "polymer": [39], "fertilizer": [31], "fertiliser": [31], "urea": [31],
    "steel": [72], "iron": [72], "vehicle": [87], "car": [87], "auto": [87], "vegetable": [7], "pulses": [7],
}
SEVERITY_WORDS = {1.0: ["stop", "halt", "ban", "shut", "cease", "embargo", "block", "completely", "totally", "fully", "cut off", "suspend"],
                  0.5: ["half", "halve", "partial", "partly", "reduce", "cut", "slash", "curb", "restrict", "limit"],
                  0.25: ["quarter", "slightly", "little"]}

INDIA = [21, 78]
COORDS = {"Russian Federation":[61,100],"China":[35,103],"United Arab Emirates":[24,54],"Saudi Arabia":[24,45],"USA":[38,-97],"Iraq":[33,44],"Switzerland":[47,8],"Brazil":[-10,-52],"Rep. of Korea":[36,128],"Angola":[-12,18],"Nigeria":[9,8],"Qatar":[25.3,51.2],"Japan":[36,138],"Australia":[-25,134],"Indonesia":[-2,118],"Kuwait":[29.3,47.5],"Other Asia, nes":[23.7,121],"Thailand":[15,101],"Germany":[51,10],"Venezuela":[7,-66],"Oman":[21,57],"Canada":[56,-106],"Malaysia":[4,102],"Viet Nam":[16,107],"Peru":[-10,-76],"Ghana":[8,-1],"Singapore":[1.3,103.8],"South Africa":[-30,25],"Argentina":[-38,-64],"China, Hong Kong SAR":[22.3,114.2],"Colombia":[4,-73],"Italy":[42,12],"Morocco":[32,-6],"Mexico":[23,-102],"United Kingdom":[54,-2],"France":[46,2],"Hungary":[47,19],"Mozambique":[-18,35],"Chile":[-35,-71],"Iran":[32,53],"Türkiye":[39,35],"Botswana":[-22,24],"Dominican Rep.":[19,-70],"Egypt":[27,30],"Bolivia (Plurinational State of)":[-17,-65],"Gabon":[-1,12],"Sweden":[62,15],"Congo":[-1,15],"Kazakhstan":[48,67],"Guinea":[10,-11],"Myanmar":[21,96],"Philippines":[13,122],"Libya":[27,17],"Czechia":[50,15],"Belgium":[51,4],"Jordan":[31,36],"Netherlands":[52,5],"Spain":[40,-4],"Austria":[47,14],"United Rep. of Tanzania":[-6,35]}

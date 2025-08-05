import pandas as pd
import numpy as np
import os

# --- Fields and their positions (tuple for inclusive start:exclusive end) ---
FIELD_POSITIONS_52 = {
    'yr': (0, 2),
    'mo': (2, 4),
    'dy': (4, 6),
    'hr': (6, 8),
    'IB': (8, 9),
    'Lat': (9, 14),
    'Lon': (14, 19),
    'ID': (19, 24),
    'LO': (24, 25),
    'ww': (25, 27),
    'N': (27, 28),
    'Nh': (28, 30),
    'h': (30, 32),
    'CL': (32, 34),
    'CM': (34, 36),
    'CH': (36, 38),
    'AM': (38, 41),
    'AH': (41, 44),
    'UM': (44, 45),
    'UH': (45, 46),
    'IC': (46, 48),
    'SA': (48, 52),
    'RI': (52, 56),
    'SLP': (56, 61),
    'WS': (61, 64),
    'WD': (64, 67),
    'AT': (67, 71),
    'DD': (71, 74),
    'EL_SST': (74, 78), #only sst used since only parsing ocean
    'IW': (78, 79),
    'IP_IH': (79, 80)
}

FIELD_POSITIONS_97 = {
    'yr': (0, 4),
    'mo': (4, 6),
    'dy': (6, 8),
    'hr': (8, 10),
    'IB': (10, 11),
    'Lat': (11, 16),
    'Lon': (16, 21),
    'ID': (21, 26),
    'LO': (26, 27),
    'ww': (27, 29),
    'N': (29, 30),
    'Nh': (30, 32),
    'h': (32, 34),
    'CL': (34, 36),
    'CM': (36, 38),
    'CH': (38, 40),
    'AM': (40, 43),
    'AH': (43, 46),
    'UM': (46, 47),
    'UH': (47, 48),
    'IC': (48, 50),
    'SA': (50, 54),
    'RI': (54, 58),
    'SLP': (58, 63),
    'WS': (63, 66),
    'WD': (66, 69),
    'AT': (69, 73),
    'DD': (73, 76),
    'EL_SST': (76, 80),
    'IW': (80, 81),
    'IP_IH': (81, 82)
}

MISSING_VALUE_FLAGS = {
    'ID': ['9'],
    'ww': ['-1'],
    'Nh': ['-1'],
    'h': ['-1'],
    'CL': ['-1'],
    'CM': ['-1'],
    'CH': ['-1'],
    'AM': ['900'],
    'AH': ['900'],
    'UM': ['9'],
    'UH': ['9'],
    'SLP': ['-1'],
    'WS': ['-1'],
    'WD': ['-1'],
    'AT': ['900'],
    'DD': ['900'],
    'EL_SST': ['9000'],
    'IW': ['9'],
    'IP_IH': ['9'],
}

djf = ["DEC", "JAN", "FEB"] #remember this bleeds into another yr
mam = ["MAR", "APR", "MAY"] 
jja = ["JUN", "JUL", "AUG"]
son = ["SEP", "OCT", "NOV"]

seasons = [djf, mam, jja, son]

def clean_and_check(val, key):
    """Cleans section of sequence and checks whether valid

    Args:
        val (str): section of sequence corresponding to var
        key (str): var name

    Returns:
        int or NaN: value
        boolean: True if valid value, valid if is a misssing value or an integer
    """
    raw = val.strip().lower()
    
    if key in MISSING_VALUE_FLAGS and raw in MISSING_VALUE_FLAGS[key]:
        return (np.nan, True)  # Mark as missing, but valid

    try:
        intval = int(raw)
    except:
        return (np.nan, False)  # Cannot parse
    
    return (intval, True)  # If no range given, accept


def parse_sequence(seq, fieldPositions):
    """generates clean dictionary of var names and the value from one sequence

    Args:
        seq (string): one 80-char or more line of data
        fieldPositions (dictionary): the Fields and their positions, there are 
        two different dictionaries for 1952-97 and 1997-2008

    Returns:
        dictionary: var names and cleaned values
    """
    seq = seq.strip()
    
    if len(seq) < 80:
        print(len(seq))
        print(f"Less than 80-char, skipping: {seq}")
        return None

    parsed = {}

    # Populate parsed with key and value
    for key, (start, end) in fieldPositions.items():
        parsed[key] = seq[start:end]

    # Clean value and repopulate
    for key in list(parsed.keys()):
        val, valid = clean_and_check(parsed[key], key)
        if key == "Lat" or key == "Lon":
            parsed[key] = val /100
        else:
            parsed[key] = val
        if not valid:
            print(f"Invalid field {key} in sequence: {seq}")
            return None

    #Create seperate keys for el_sst/ip_ih and add values
    if parsed['LO'] == 2: #should only be parsing ocean
        parsed['EL'] = np.nan
        parsed['SST'] = parsed['EL_SST']
        parsed['IP'] = np.nan
        parsed['IH'] = parsed['IP_IH']
           
        # Remove EL_SST raw field
        del parsed['EL_SST']
        del parsed['IP_IH']
    
    else:
        print(f"Invalid LO in sequence: {seq}")
        return None

    return parsed


def parse_file_to_df(path, pre98):
    """
    Args:
        path (string): path to file
        pre98 (boolean): whether 

    Returns:
        df
    """
    
    with open(path, 'r') as f:
        lines = f.readlines()

    parsed_data = []
    
    if pre98: fieldPositions = FIELD_POSITIONS_52
    else: fieldPositions = FIELD_POSITIONS_97

    for line in lines:
        result = parse_sequence(line, fieldPositions)
        if result is not None:
            parsed_data.append(result)

    df = pd.DataFrame(parsed_data)
    return df


"""
Parse files by season per year. 

To change btwn post and pre 1997 -
 - fromPath
 - uncomment and comment getting file names
 - year range
 - parse_file_to_df func call true or false 
 

"""


fromPath = "data/EECRA/ship_199801_200812/"

files = os.listdir(fromPath)
    
for fullYear in range(1998, 2008 +1): #1952, 1997 + 1
    shortYr = str(fullYear)[2:]
    for season in seasons:
        
        # get the file names corresponding to the months needed - pre 1997
        """if season[0] == "DEC": 
            fn1 = season[0] + str(int(shortYr) - 1) + "O"   #djf1999 is dec 1998, jan 1999, and feb 1999
        else:
            fn1 = season[0] + shortYr + "O"
            
        fn2 = season[1] + shortYr + "O"
        fn3 = season[2] + shortYr + "O"""
        #--
        
        # get the file names corresponding to the months needed - post 1997
        if season[0] == "DEC":
            if fullYear == 1998: needDEC97 = True
            fn1 = season[0] + str(int(shortYr) - 1) + "i"
        else:
            fn1 = season[0] + shortYr + "i"
            
        fn2 = season[1] + shortYr + "i"
        fn3 = season[2] + shortYr + "i"
        #--
        
        if (fn1 not in files or fn2 not in files or fn3 not in files) and not needDEC97:
            print ("no", str(season), "in yr", str(fullYear))
            continue
        
        try:
            if not needDEC97: df1 = parse_file_to_df(fromPath+fn1, False)
            else: df1 = parse_file_to_df("data/EECRA/ship_195112_199712/DEC97O", True)
            
            df2 = parse_file_to_df(fromPath+fn2, False)
            df3 = parse_file_to_df(fromPath+fn3, False)
        except Exception as e:
            print(fn2, "season files corrupted?")
            print(e)
            continue
            
        try:
            seasondf = pd.concat([df1, df2, df3])
            seasondf.to_csv("data/EECRA/ocean_seasonal/df_"+season[0][0]+season[1][0]+season[2][0]+str(fullYear)+".csv", index=False)
            print("saved", str(season), "in yr", str(fullYear))
        except Exception as e:
            print("failed to save", str(season), "in yr", str(fullYear))
            print(e)
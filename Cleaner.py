

def clean(star_wars):
    renameColumns = {
        "Have you seen any of the 6 films in the Star Wars franchise?": 'SeenSW',
        "Do you consider yourself to be a fan of the Star Wars film franchise?": "IsStarWarsFan",
        "Which of the following Star Wars films have you seen? Please select all that apply.": "SeenSW1",
        "Unnamed: 4" : "SeenSW2",
        "Unnamed: 5" : "SeenSW3",
        "Unnamed: 6" : "SeenSW4",
        "Unnamed: 7" : "SeenSW5",
        "Unnamed: 8" : "SeenSW6",
        "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "RankSW1",
        "Unnamed: 10": "RankSW2",
        "Unnamed: 11": "RankSW3",
        "Unnamed: 12": "RankSW4",
        "Unnamed: 13": "RankSW5",
        "Unnamed: 14": "RankSW6",
        "Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.": "ViewOfHanSolo",
        "Unnamed: 16": "ViewOfLukeSkywalker",
        "Unnamed: 17": "ViewOfPrincessLeiaOrgana",
        "Unnamed: 18": "ViewOfAnakinSkywalker",
        "Unnamed: 19": "ViewOfObiWanKenobi",
        "Unnamed: 20": "ViewOfEmperorPalpatine",
        "Unnamed: 21": "ViewOfDarthVader",
        "Unnamed: 22": "ViewOfLandoCalrissian",
        "Unnamed: 23": "ViewOfBobaFett",
        "Unnamed: 24": "ViewOfC-3P0",
        "Unnamed: 25": "ViewOfR2D2",
        "Unnamed: 26": "ViewOfJarJarBinks",
        "Unnamed: 27": "ViewOfPadmeAmidala",
        "Unnamed: 28": "ViewOfYoda",
        "Are you familiar with the Expanded Universe?": "FamiliarWithExpandedUniverse",
        "Which character shot first?":"WhoShotFirst",
        star_wars.columns[31]: "IsExpandedUniverseFan",
        "Do you consider yourself to be a fan of the Star Trek franchise?": "IsStarTrekFan",
        "Household Income": "Income",
        "Location (Census Region)": "Location"
    }

    star_wars.rename(columns=renameColumns, inplace=True)

    # drop first row

    star_wars = star_wars.ix[1:]

    # for "which star wars films have you seen?" change it to a 1 or 0 value

    columns = [
        'SeenSW1',
        'SeenSW2',
        'SeenSW3',
        'SeenSW4',
        'SeenSW5',
        'SeenSW6',
    ]

    for column in columns:
        star_wars[column] = star_wars[column].apply(lambda x: 0 if(str(x) == 'nan') else 1)


    def convertToBool(x):
        if x == 'Yes':
            return 1
        elif x == 'No':
            return 0

    toBoolColumns = [
        "SeenSW",
        "IsStarWarsFan",
        "IsStarTrekFan",
        "FamiliarWithExpandedUniverse",
        "IsExpandedUniverseFan",
    ]

    for column in toBoolColumns:
        # convert to boolean
        star_wars[column] = star_wars[column].apply(lambda x: convertToBool(x))
        # if empty value set to average
        star_wars[column] = star_wars[column].apply(lambda x: round(star_wars[column].mean()) if str(x) == 'nan' else x)

    # change gender to 0, 1

    def convertGenderToBool(x):

        if x == 'Male':
            return 1
        elif x == 'Female':
            return 0

    star_wars['Gender'] = star_wars['Gender'].apply(lambda x: convertGenderToBool(x) if str(x) != "nan" else x)
    star_wars['Gender'] = star_wars['Gender'].apply(lambda x: star_wars['Gender'].mode()[0] if str(x) == "nan" else x)

    # change view of to -2, -1, 0, 1, or 2
    # we assume that both neutral and unfamiliar counts as 0.

    newValues = {
        "Very favorably": 2,
        "Somewhat favorably": 1,
        "Neither favorably nor unfavorably (neutral)": 0,
        "Unfamiliar (N/A)": 0,
        "Somewhat unfavorably": -1,
        "Very unfavorably": -2,
    }

    columns = [
        "ViewOfHanSolo",
        "ViewOfLukeSkywalker",
        "ViewOfPrincessLeiaOrgana",
        "ViewOfAnakinSkywalker",
        "ViewOfObiWanKenobi",
        "ViewOfEmperorPalpatine",
        "ViewOfDarthVader",
        "ViewOfLandoCalrissian",
        "ViewOfBobaFett",
        "ViewOfC-3P0",
        "ViewOfR2D2",
        "ViewOfJarJarBinks",
        "ViewOfPadmeAmidala",
        "ViewOfYoda",
    ]

    for c in columns:
        star_wars = star_wars.replace({c: newValues })
        # replace empty values with the average
        star_wars[c] = star_wars[c].apply(lambda x: round(star_wars[c].mean()) if str(x) == "nan" else x)

    # drop who shot first column
    star_wars=star_wars.drop('WhoShotFirst', 1)

    # convert classes to integers

    ageGroups = {
        '18-29': 1,
        '30-44': 2,
        '45-60': 3,
        '> 60': 4
    }

    incomeGroups = {
        '$0 - $24,999': 1,
        '$25,000 - $49,999': 2,
        '$50,000 - $99,999': 3,
        '$100,000 - $149,999': 4,
        '$150,000+': 5
    }

    educationGroups = {
        'Less than high school degree': 0,
        'High school degree': 1,
        'Some college or Associate degree': 2,
        'Bachelor degree': 3,
        'Graduate degree': 4,
    }

    locationGroups = {
        'South Atlantic': 0,
        'West South Central': 1,
        'West North Central': 2,
        'Middle Atlantic': 3,
        'East North Central': 4,
        'Pacific': 5,
        'Mountain': 6,
        'New England': 7,
        'East South Central': 8
    }

    star_wars = star_wars.replace({'Age': ageGroups})
    star_wars = star_wars.replace({'Income': incomeGroups})
    star_wars = star_wars.replace({'Education': educationGroups})
    star_wars = star_wars.replace({'Location': locationGroups})

    columns = [
        'Age',
        'Income',
        'Education',
        'Location'
    ]

    for column in columns:

        # replace empty values with the average
        f = lambda x: star_wars[column].mode()[0] if str(x) == 'nan' else x
        star_wars[column] = star_wars[column].apply(f)

    dropColumns = [
        'RankSW1',
        'RankSW2',
        'RankSW3',
        'RankSW4',
        'RankSW5',
        'RankSW6',
    ]

    for c in dropColumns:
        star_wars = star_wars.drop(c, 1)

    return star_wars
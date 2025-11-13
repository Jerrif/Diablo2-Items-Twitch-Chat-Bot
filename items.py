# scrapes diablo.gamepedia.com for unique and set item stats and stores them in a sqlite3 database

import urllib.request
import re
import time
import sqlite3

urls_uniques = [
    'https://diablo.gamepedia.com/Unique_Axes_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Bows_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Crossbows_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Daggers_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Javelins_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Maces_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Polearms_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Scepters_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Spears_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Staves_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Swords_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Throwing_Weapons_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Wands_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Armor_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Belts_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Boots_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Circlets_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Gloves_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Helms_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Shields_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Amazon_Weapons_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Assassin_Katars_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Barbarian_Helms_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Druid_Pelts_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Necromancer_Shrunken_Heads_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Paladin_Shields_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Sorceress_Orbs_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Rings_(Diablo_II)',
    'https://diablo.gamepedia.com/Unique_Amulets_(Diablo_II)'
]

urls_sets = [
    'https://diablo.gamepedia.com/Angelic_Raiment_(Diablo_II)',
    'https://diablo.gamepedia.com/Arcanna%27s_Tricks_(Diablo_II)',
    'https://diablo.gamepedia.com/Arctic_Gear_(Diablo_II)',
    'https://diablo.gamepedia.com/Berserker%27s_Arsenal_(Diablo_II)',
    'https://diablo.gamepedia.com/Cathan%27s_Traps_(Diablo_II)',
    'https://diablo.gamepedia.com/Civerb%27s_Vestments_(Diablo_II)',
    'https://diablo.gamepedia.com/Cleglaw%27s_Brace_(Diablo_II)',
    'https://diablo.gamepedia.com/Death%27s_Disguise_(Diablo_II)',
    'https://diablo.gamepedia.com/Hsarus%27_Defense_(Diablo_II)',
    'https://diablo.gamepedia.com/Infernal_Tools_(Diablo_II)',
    'https://diablo.gamepedia.com/Iratha%27s_Finery_(Diablo_II)',
    'https://diablo.gamepedia.com/Isenhart%27s_Armory_(Diablo_II)',
    'https://diablo.gamepedia.com/Milabrega%27s_Regalia_(Diablo_II)',
    'https://diablo.gamepedia.com/Sigon%27s_Complete_Steel_(Diablo_II)',
    'https://diablo.gamepedia.com/Tancred%27s_Battlegear_(Diablo_II)',
    'https://diablo.gamepedia.com/Vidala%27s_Rig_(Diablo_II)',
    'https://diablo.gamepedia.com/Aldur%27s_Watchtower_(Diablo_II)',
    'https://diablo.gamepedia.com/Bul-Kathos%27_Children_(Diablo_II)',
    'https://diablo.gamepedia.com/Cow_King%27s_Leathers_(Diablo_II)',
    'https://diablo.gamepedia.com/The_Disciple_(Diablo_II)',
    'https://diablo.gamepedia.com/Griswold%27s_Legacy_(Diablo_II)',
    'https://diablo.gamepedia.com/Heaven%27s_Brethren_(Diablo_II)',
    'https://diablo.gamepedia.com/Hwanin%27s_Majesty_(Diablo_II)',
    'https://diablo.gamepedia.com/Immortal_King_(Diablo_II)',
    'https://diablo.gamepedia.com/M%27avina%27s_Battle_Hymn_(Diablo_II)',
    'https://diablo.gamepedia.com/Natalya%27s_Odium_(Diablo_II)',
    'https://diablo.gamepedia.com/Naj%27s_Ancient_Vestige_(Diablo_II)',
    'https://diablo.gamepedia.com/Orphan%27s_Call_(Diablo_II)',
    'https://diablo.gamepedia.com/Sander%27s_Folly_(Diablo_II)',
    'https://diablo.gamepedia.com/Sazabi%27s_Grand_Tribute_(Diablo_II)',
    'https://diablo.gamepedia.com/Tal_Rasha%27s_Wrappings_(Diablo_II)',
    'https://diablo.gamepedia.com/Trang-Oul%27s_Avatar_(Diablo_II)'
    ]


# Create the items database
connection = sqlite3.connect("d2items.db")
db = connection.cursor()

def main():
    dbInit("uniques")
    dbInit("sets")
    getItems(urls_uniques, 'uniques')
    getItems(urls_sets, "sets")

    unique_ring_text = "Use !unique ringname, where ringname is one of the following:" \
        " bulkathosweddingband, carrionwind, dwarfstar," \
        " manaldheal, nagelring, naturespeace, ravenfrost," \
        " thestoneofjordan, whispprojector"
    unique_amulet_text = "Use !unique amuletname, where amuletname is one of the following:" \
        " atmasscarab, crescentmoon, highlordswrath, maraskaleidoscope," \
        " metalgrid, nokozanrelic, saracenschance, seraphshymn, thecatseye," \
        " theyeyeofetlich, themahimoakcurio, therisingsun"
    set_ring_text = "Use !set ringname, where ringname is one of the following:" \
        " angelichalo, cathansseal"
    set_amulet_text = "Use !set amuletname, where amuletname is one of the following:" \
        " angelicwings, arcannassign, cathanssigil, civerbsicon, irathascollar," \
        " tancredsweird, vidlassnare, tellingofbeads, talrashasadjudication"

    # Add the special ring data into the DB
    db.execute("INSERT INTO 'uniques'('search_string', 'item_name', 'item_text') VALUES(?, ?, ?)", ("ring", "ring", str(unique_ring_text)))
    db.execute("INSERT INTO 'uniques'('search_string', 'item_name', 'item_text') VALUES(?, ?, ?)", ("amulet", "amulet", str(unique_amulet_text)))
    db.execute("INSERT INTO 'sets'('search_string', 'item_name', 'item_text') VALUES(?, ?, ?)", ("ring", "ring", str(set_ring_text)))
    db.execute("INSERT INTO 'sets'('search_string', 'item_name', 'item_text') VALUES(?, ?, ?)", ("amulet", "amulet", str(set_amulet_text)))

    connection.commit()

    print()
    print("Total items added to database: ", connection.total_changes)

    connection.close()


# Create the tables and indicies if they don't exist already
def dbInit(table):
    if table == "uniques":
        create_table = """CREATE TABLE "{}"(
        search_string TEXT,
        item_name TEXT PRIMARY KEY,
        item_text TEXT);""".format(table.replace('"', '""'))
        create_index1 = """CREATE INDEX idx_search_uniques ON uniques (search_string)"""
        create_index2 = """CREATE INDEX idx_item_name_uniques ON uniques (item_name)"""
    elif table == "sets":
        create_table = """CREATE TABLE "{}"(
        search_string TEXT,
        item_name TEXT PRIMARY KEY,
        set_name TEXT,
        item_text TEXT);""".format(table.replace('"', '""'))
        create_index1 = """CREATE INDEX idx_search_sets ON sets (search_string)"""
        create_index2 = """CREATE INDEX idx_item_name_sets ON sets (item_name)"""

    try:
        db.execute(create_table)
    except sqlite3.OperationalError:
        print("Table already exists")

    try:
        db.execute(create_index1)
        db.execute(create_index2)
    except sqlite3.OperationalError:
        print("Index already exists")

    connection.commit()

# for url in urls_sets:
def getItems(urls, table):
    print("Parsing URL list:\n")
    print(urls)
    for url in urls:
        # Fetch the data from the URL
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        respData = resp.read()

        # Get the name of the set (if applicable) from the title of the page
        if table == "sets":
            reg = re.search(r'<title>(.+?) ?\(', str(respData))
            set_name = reg.group(1).replace("\\", "")

        # Get the HTML for each item
        items = re.findall(r'<table.*?\/table></div>', str(respData))

        # for item in items:
        for i in range(0, len(items)):
            if set_name:
                getStats(items[i], table, set_name)
            else:
                getStats(items[i], table)

        # Add a small sleep between webpages, so the website doesn't think we're DDOSing them
        time.sleep(3)

    connection.commit()

def getStats(items, table, set_name=""):

    print("\n----------------------------")

    search_string = "itemname"
    item_text = "["
    item_name = ""
    indestructible = False

    stats = re.findall(r'(Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?:(?=<\/span>)|(?=<br /><br />))|Level Requirement: \d{1,2})', str(items)) # This should catch everything. Hopefully. Update: it does.

    # for stat in stats:
    for j in range(0, len(stats)):

        # Strip off the remainder of the HTML that I couldn't catch with regex, and the superfluous '(varies)'
        stats[j] = re.sub(r'<.+?.+?>|\\| ?\(varies\)', "", stats[j])

        # If there's a 2H damage stat, add that in
        if re.match(r'\(\d+-\d+\) to \(\d+-\d+\)|16 to 34', stats[j]):
            stats[j] = "2H Damage: " + stats[j]

        # [Indestructible] gets put in twice: once on the durability line, and again in the stats
        if stats[j].count("Indestructible") and indestructible == True:
            indestructible = False
            continue
        elif stats[j].count("Indestructible") and indestructible == False:
            indestructible = True

        # Remove the arbitrary weapon speed stat which just shows up as a number like [20]
        # Also, remove the block% for individual classes on shields.
        if re.match(r'^\[-?\d{0,2}\]$|^\d{0,2}\%$|\(Only Spawns In Patch', stats[j]):
            continue

        # Get the item name (without spaces). Will always be the first item
        if j == 0:
            item_name = stats[j].replace(" ", "").replace("'", "").replace("-", "").lower()

        # Get the search string. Making it lowercase now makes it easier later
        if j == 1:
            # There are a few mistakes in the website that I'm using to get the data. Just correcting them manually here
            if stats[j] == "Handed Sword":
                stats[j] = "Two-Handed Sword"
            elif stats[j] == "s Bow":
                stats[j] = "Hunter's Bow"
            elif stats[j] == "Nu":
                stats[j] = "Chu-Ko-Nu"
            elif stats[j] == "Corbin":
                stats[j] = "Bec-De-Corbin"

            search_string = stats[j].replace(" ", "").replace("'", "").replace("-", "").lower()

            if stats[j] == "Ring" or stats[j] == "Amulet":
                search_string = item_name

        if re.match(r'^\d+$', stats[j]) or stats[j] == "":
            print("REMOVING: ", stats[j])
            continue

        # Add square brackets as delimiters for each stat
        if j != len(stats) - 1:
            item_text += stats[j] + ']['
        else:
            item_text += stats[j] + ']'

    if item_text.endswith('['):
        item_text = item_text.rstrip('[')

    print(item_text)

    # dcur.execute('INSERT INTO "{}" VALUES(?, ?)'.format(group.replace('"', '""')), (food, 1))
    # db.execute("INSERT INTO 'uniques'('search_string', 'item_name', 'item_text') VALUES(?, ?, ?)", (str(search_string), str(item_name), str(item_text)))
    if table == "uniques":
        db.execute('INSERT INTO "{}"(search_string, item_name, item_text) VALUES(?, ?, ?)'.format(table.replace('"', '""')), (str(search_string), str(item_name), str(item_text)))
    elif table == "sets":
        db.execute('INSERT INTO "{}"(search_string, item_name, set_name, item_text) VALUES(?, ?, ?, ?)'.format(table.replace('"', '""')), (str(search_string), str(item_name), str(set_name), str(item_text)))



if __name__ == "__main__":
    main()

# stats = re.findall(r'<span.+?>(.*?)(?=<\/span>)', str(item))
# <span.+?>(.*?)(?=<\/span>)|Minimum (Strength|Dexterity):.+?(\d{2,3}|-)<
# (Minimum Strength: (?:<span style=\"color: #\w{6};\">)\d{2,3}|<span.+?>.*?(?=<\/span>))
# (Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?=<\/span>)|Level Requirement: \d{2})
# (Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?=<\/span>|\[\d*\])|Level Requirement: \d{2})
# (Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?:(?=<\/span>)|(?=<br))|Level Requirement: \d{1,2})

# stats = re.findall(r'<span.+?>(.*?)(?=<\/span>)|Minimum (Strength|Dexterity):.+?(\d{2,3}|-)<', str(items))

# # stats = re.findall(r'(Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?:(?=<\/span>)|(?=<br))|Level Requirement: \d{1,2})', str(items[i])) # This is for the uniques

# stats = re.findall(r'(Minimum (?:Strength|Dexterity): (?:<span style=\"color: #\w{6};\">)(?:\d{2,3}|-)|<span.+?>.*?(?:(?=<\/span>))|Level Requirement: \d{1,2})', str(items[i])) # Just testing. This is for sets. I think it gives the same results. It's only missing |(?=<br)

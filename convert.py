import json
import sys

from bs4 import BeautifulSoup


if len(sys.argv) < 2:
    print('Too few arguments, please specify a file to be converted')
    sys.exit(1)

# Open and parse the file
FILE_NAME = sys.argv[1]

with open(FILE_NAME, encoding='utf8') as f:
    soup = BeautifulSoup(f.read().strip(), 'xml')

# Empty characters array
characters = []

# Iterate over dict items
# TODO: break the code into functions
for character in soup.find_all('character'):
    character_data = {}
    
    #
    # Only add the most important info (for now)
    #

    # Character literal
    character_data['literal'] = character.literal.text

    # Readings and meanings object
    try:
        rm = character.reading_meaning.rmgroup
    except AttributeError:
        character_data['onyomi'] = None
        character_data['kunyomi'] = None
        character_data['meanings'] = None
        rmgroup_present = False
    else:
        rmgroup_present = True

    # Readings
    if rmgroup_present:
        character_data['onyomi'] = [
            yomi.text for yomi in rm.find_all('reading') 
                if yomi['r_type'] == 'ja_on'
        ] or None
        character_data['kunyomi'] = [
            yomi.text for yomi in rm.find_all('reading') 
                if yomi['r_type'] == 'ja_kun'
        ] or None

    # Nanori readings
    nanori = character.reading_meaning.find_all('nanori')
    character_data['nanori'] = [
        yomi.text for yomi in nanori
    ] or None

    # English meanings
    if rmgroup_present:
        character_data['meanings'] = [
            meaning.text for meaning in rm.find_all('meaning') 
                if not meaning.has_attr('m_lang')
        ] or None

    # And finally...
    characters.append(character_data)


# Save to a file
OUTPUT_NAME = sys.argv[2] if len(sys.argv) >= 3 else 'kanjidic2.json'

with open(OUTPUT_NAME, 'w', encoding='utf8') as f:
    json.dump(characters, f, ensure_ascii=False)

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
        continue
    
    # Readings
    character_data['onyomi'] = [
        yomi.text for yomi in rm.find_all('reading') if yomi['r_type'] == 'ja_on'
    ]
    character_data['kunyomi'] = [
        yomi.text for yomi in rm.find_all('reading') if yomi['r_type'] == 'ja_kun'
    ]

    # And finally...
    characters.append(character_data)


# Save to a file
OUTPUT_NAME = sys.argv[2] if len(sys.argv) >= 3 else 'kanjidic2.json'

with open(OUTPUT_NAME, 'w', encoding='utf8') as f:
    json.dump(characters, f, ensure_ascii=False)

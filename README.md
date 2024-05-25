# Kindle vocab.db tools
    
  1. Mount your Kindle via USB and copy `system/vocabulary/vocab.db`
     file.
  2. `vocab_sync.py` syncs the new words from `vocab.db` to
     `definitions.db`.
  3. `fetch_defs.py` fetches missing word definitions in
     `definitions.db`. This is optional and requires an OpenAI API key.
  4. `anki_export.py` exports `definitions.db` into Anki deck (.apkg file)

  
  Config file:
  
  ```
  [openai]
  key = <your open AI key>
  
  [anki]
  deck_id = <your unique deck id>
  deck_name = <name of your deck. E.g. "John's Kindle Vocabulary"

  ```

  You need an OpenAI API key to fetch definitions. It is only used by
  `fetch_defs.py`.
  
  Anki `deck_id` uniquely identifies your personal deck. This will
  allow you to re-import it when the new words were added and the deck
  file was re-generated.  You can generate a unique `deck_id` using
  the following command:
  
  ```
  python3 -c "import random; print(random.randrange(1 << 30, 1 << 31))"
  ```

# Requirements
  * python3
  * sqlite3

  How to set up virtual env
  (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
  
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  python3 -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

# TODO
  
  - The cards are very simple now: just a word and definitions. It should be possible to add IPA,
    usage examples, and audio.
  - The use of OpenAI to fetch definitions may be controversial. An alternative definitions source,
    such as Oxford Dictionaries API may be implemented. This was the reason we split definitions
    fetching into a separate script.
  

## Related
https://github.com/wzyboy/kindle_vocab_anki
https://github.com/johan456789/yaktoa

# Kindle vocab.db tools
    
  1. Mount your Kindle via USB and copy `system/vocabulary/vocab.db`
     file.
  2. `vocab_sync.py` syncs the new words from `vocab.db` to
     `definitions.db`.
  3. `fetch_defs.py` fetches missing word definitions in
     `definitions.db`. This is optional and requires OpenAI API key.

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

## Related
https://github.com/wzyboy/kindle_vocab_anki
https://github.com/smb-apache/yaktoa

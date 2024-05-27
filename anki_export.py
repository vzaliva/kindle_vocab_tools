#!/usr/bin/env python

import sys
from os import path
import sqlite3
import click
from icecream import ic
import configparser
import genanki
import html

# Unique ID of this model (schema)
model_id=1684351491

model = genanki.Model(
  model_id,
  'Kindle vocabulary builder',
  fields=[
    {'name': 'Word'},
    {'name': 'Definition'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Word}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
    },
  ])

# Custom Note class using only word (without definition)
# as GUID.
class DictNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0])

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--config-file', default="config.cfg", help='config.cfg file')
@click.option('--definitions-file', default="definitions.db", help='definitions data file')
@click.option('--anki-file', default="myvocab.apkg", help='Anki deck file (will be overwritten)')
def anki_export(verbose, config_file, definitions_file, anki_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    if path.exists(definitions_file):
        if verbose:
            print("Opening definitions `%s`" % definitions_file)
    else:
        print("Definitions file `%s` not found" % definitions_file)
        exit(1)

    deck_id = config['anki']['deck_id']
    deck_name = config['anki']['deck_name']
        
    deck = genanki.Deck(int(deck_id), deck_name)

    n = 0
    try:
       db = sqlite3.connect(definitions_file)
       c = db.cursor()
       c.execute("SELECT id, definition FROM DEFS WHERE definition_status = 1")
       defs = c.fetchall()
       for d in defs:
           # Split the full_id into language code and word
           full_id = d[0]
           definition = d[1]
           language_code, word = full_id.split(':')
           if verbose:
               print ("Exporting %s" % word)

           fields = [html.escape(f) for f in [word, definition]]               
           note = DictNote(model = model, fields=fields)          
           
           n = n + 1
           
           deck.add_note(note)
           
       if verbose:
           print ("Writing %s" % anki_file)
           genanki.Package(deck).write_to_file(anki_file)

    except Exception as e:
        print("An error occurred. Export failed:", e)
    finally:
        c.close()
        db.close()    
        print("%d cards were added" % n)

if __name__ == '__main__':
    anki_export()

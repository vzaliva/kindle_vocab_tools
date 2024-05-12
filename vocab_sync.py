#!/usr/bin/env python

import sys
from os import path
import sqlite3
import click
from icecream import ic
import configparser

def count(cursor, table):
    cursor.execute("select count(*) from %s" % table)
    results = cursor.fetchone()
    return int(results[0])

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--vocab-file', default="vocab.db", help='vocab.db file')
@click.option('--config-file', default="config.cfg", help='config.cfg file')
@click.option('--definitions-file', default="definitions.db", help='definitions data file')
def resync(verbose, vocab_file, config_file, definitions_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    if verbose:
        if path.exists(definitions_file):
            print("Opening existing %s" % definitions_file)
        else:
            print("Creating %s" % definitions_file)
                        
    db = sqlite3.connect(definitions_file)
    c = db.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS DEFS (
          id TEXT PRIMARY KEY NOT NULL,
          definition TEXT,
          pronunciation TEXT,
          pronunciation_url TEXT,
          source TEXT,
          sync_ts INTEGER DEFAULT 0,
          definition_ts INTEGER DEFAULT 0,
          definition_status INTEGER DEFAULT 0
        )
        ''')

    db.commit()
    
    db.execute("ATTACH DATABASE '%s' AS v" % vocab_file)
    if verbose:
        print("%d words in Kindle vocab.db" % count(c, "v.WORDS"))
    dcount0 = count(c,"DEFS")
    c.execute(
        '''
        insert into DEFS (id, sync_ts, definition_ts, definition_status)
        select WORDS.id, strftime('%s', 'now'), 0 , 0
        from v.WORDS
        WHERE WORDS.id NOT IN (SELECT id FROM DEFS)
        ''')
    dcount1 = count(c,"DEFS")
    if verbose:
        print("%d new words added to definitions table" % (dcount1-dcount0))
    c.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    resync()

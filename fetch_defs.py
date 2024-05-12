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


# DEFS.definition_status values:
# 0 - new
# 1 - successfully fetched

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--config-file', default="config.cfg", help='config.cfg file')
@click.option('--definitions-file', default="definitions.db", help='definitions data file')
def fetch_defs(verbose, config_file, definitions_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    app_key = config['openai']['key']

    if verbose:
        if path.exists(definitions_file):
            print("Opening existing %s" % definitions_file)
        else:
            print("Creating %s" % definitions_file)
                        
    db = sqlite3.connect(definitions_file)
    c = db.cursor()
    if verbose:
        n = count(c,"DEFS")
        print ("Total %d definitions" % n)

    c.execute("select id from DEFS where definition_status=0")
    words = c.fetchall()
    lang_words = [(word[0].split(':')[0], word[0].split(':')[1]) for word in words]
    ic(lang_words)
        
    c.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    fetch_defs()
    

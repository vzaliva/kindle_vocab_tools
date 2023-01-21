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
def fetch_defs(verbose, vocab_file, config_file, definitions_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    app_id  = config['oxforddictionaries']['app_id']
    app_key = config['oxforddictionaries']['app_key']

    if verbose:
        if path.exists(definitions_file):
            print("Opening existing %s" % definitions_file)
        else:
            print("Creating %s" % definitions_file)
                        
    db = sqlite3.connect(definitions_file)
    c = db.cursor()
    
    c.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    fetch_defs()
    

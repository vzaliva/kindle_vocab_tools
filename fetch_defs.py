#!/usr/bin/env python

import sys
import time
from os import path
import sqlite3
import click
from icecream import ic
import configparser
import openai

def count(cursor, table):
    cursor.execute("select count(*) from %s" % table)
    results = cursor.fetchone()
    return int(results[0])


def fetch_definition(full_id):
    try:
        # Split the full_id into language code and word
        language_code, word = full_id.split(':')
        
        # Create the prompt for the OpenAI API
        prompt = f"""Give me the dictionary definition of the word
        `{word}` in the language `{language_code}`. Do not say that
        this is the definition, just the definition itself. If this
        word is predominantly used in some English dialect (e.g.,
        British or American), mention that. If there are several
        meanings, enumerate them. If the word could be used as
        different parts of speech (e.g., both verb and noun), say
        that. If possible, give short usage examples (one short
        sentence), preferably from literature, for all meanings and parts of
        speech. Make it look like a brief, well-structured dictionary definition
        that could fit on a mobile phone screen.
        """
        
        # Call the OpenAI API using the gpt-4 model
        response =  openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        definition = response.choices[0].message.content.strip()
        return definition
    except Exception as e:
        print(f"Failed to fetch definition for {full_id}: {e}")
        return None

# DEFS.definition_status values:
# 0 - new
# 1 - successfully fetched

@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--force', is_flag=True, help='force re-fetching all definitions')
@click.option('--config-file', default="config.cfg", help='config.cfg file')
@click.option('--definitions-file', default="definitions.db", help='definitions data file')
def fetch_defs(verbose, force, config_file, definitions_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    openai.api_key = config['openai']['key']

    if verbose:
        if path.exists(definitions_file):
            print("Opening existing %s" % definitions_file)
        else:
            print("Creating %s" % definitions_file)


    conn = sqlite3.connect(definitions_file)
    cursor = conn.cursor()

    n = 0
    try:
        # Start a transaction
        conn.execute('BEGIN')

        # Select IDs where definition_status = 0
        if force:
            cursor.execute("SELECT id FROM DEFS")
        else:
            cursor.execute("SELECT id FROM DEFS WHERE definition_status = 0")

            ids_to_update = cursor.fetchall()
        
        for id_tuple in ids_to_update:
            id = id_tuple[0]
            if verbose:
                print ("Fetcing %s" % id)
            definition = fetch_definition(id)
            if definition:
                #if verbose:
                #    print ("\t Definition: %s" % definition)
                
                # Current timestamp
                current_ts = int(time.time())
                # Update the definition, timestamp, and status
                cursor.execute(
                    "UPDATE DEFS SET definition = ?, definition_ts = ?, definition_status = 1 WHERE id = ?",
                    (definition, current_ts, id)
                )
                n = n + 1
            else:
                # Stop further processing if a fetch error occurs
                print("Stopping updates due to fetch error.")
                break

            # Commit the changes made so far
            conn.commit()
    except Exception as e:
        # Handle other types of errors without rolling back
        print("An error occurred during the update process, but changes will not be rolled back:", e)
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()    
        print("%d definitions were added" % n)

if __name__ == '__main__':
    fetch_defs()
    

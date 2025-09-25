# Apple AddressBook to CSV Converter

A Python utility to convert Apple AddressBook (.abbu) files to CSV format, extracting essential contact information.

## Why?
I had an export of an Apple Contacts that I wanted to get access to.  The only (obvious) way to get the data from the abbu file was to import and merge with my core contacts.  Nope.  Dont need that. Just needed a phone number. Quick search on the web revealed .. nothing easy other than the general solution of export your current contacts, import the new stuff, then delete it all and re-import your original contacts.  Bleh.

So, As all self assigned projects go, to save time and the find an easy way, I spent the afternoon learning way more about the Apple Contacts export and how it is really a SQLite3 file with multiple databases.  You can do this yourself - just change the .abbu to .sql and Finder will epand it to folders.  From there, it is finding the data and the query. Enjoy..

Oh.. Make a spare copy of your abbu file.. This shouldn't cause problems, but it is not throughly tested. Once I got the info I was looking for, I wrapped up my efforts. If you find any bugs - let me know. Or not.

## Features

- Extracts first name, last name, email address, and phone number from Apple AddressBook files
- Automatically finds the database with the most contacts in .abbu directories
- Handles multiple email addresses and phone numbers per contact
- Clean CSV output with proper UTF-8 encoding
- Command-line interface with argument validation

## Requirements

- Python 3.11 or higher
- No external dependencies (uses built-in sqlite3, csv, argparse modules)

## Installation

1. Clone or download this repository (well, the convert_contacts.py is all you need, the rest are just formalities)
2. Ensure Python 3.11+ is installed

## Usage

### Basic Usage

```bash
python3 convert_contacts.py --in "path/to/Contacts.abbu" --out "output.csv"
```

### Examples

```bash
# Convert from .abbu directory
python3 convert_contacts.py --in "Contacts-06-02-2025.abbu" --out "my_contacts.csv"

# Convert from direct database file
python3 convert_contacts.py --in "AddressBook-v22.abcddb" --out "contacts.csv"
```

## Input Formats

The utility accepts two input formats:

1. **Apple AddressBook Directory (.abbu)**: The utility will automatically scan for AddressBook database files and use the one with the most contacts
2. **Direct Database File (.abcddb)**: Direct path to an AddressBook SQLite database file

## Output Format

The CSV output contains the following columns:
- First Name
- Last Name
- Email
- Phone

Empty fields - are - included as blank values to maintain consistent CSV structure.

## How It Works

1. Connects to the SQLite database within the AddressBook file
2. Queries the `ZABCDRECORD` table for contact records
3. Joins with `ZABCDEMAILADDRESS` and `ZABCDPHONENUMBER` tables for contact details
4. Exports results to CSV with proper data cleaning and UTF-8 encoding

## License

This project is provided as-is for personal use in converting Apple AddressBook data.

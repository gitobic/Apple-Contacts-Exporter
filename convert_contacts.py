#!/usr/bin/env python3
"""
Convert Apple AddressBook (.abbu) contacts to CSV format.
Extracts first name, last name, email, and phone number from contacts.

Sample command: 
python3 convert_contacts.py --in "Contacts-export.abbu" --out "/path/to/your/output.csv"

"""

import sqlite3
import csv
import sys
import argparse
from pathlib import Path

def count_contacts_in_db(db_path: str) -> int:
    """Count the number of contact records in a database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ZABCDRECORD WHERE (ZFIRSTNAME IS NOT NULL OR ZLASTNAME IS NOT NULL)")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

def extract_contacts_to_csv(db_path: str, output_path: str = "contacts2.csv"):
    """Extract contacts from AddressBook SQLite database to CSV."""

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to join contacts with their email addresses and phone numbers
    query = """
    SELECT DISTINCT
        r.ZFIRSTNAME as first_name,
        r.ZLASTNAME as last_name,
        e.ZADDRESS as email,
        p.ZFULLNUMBER as phone
    FROM ZABCDRECORD r
    LEFT JOIN ZABCDEMAILADDRESS e ON r.Z_PK = e.ZOWNER
    LEFT JOIN ZABCDPHONENUMBER p ON r.Z_PK = p.ZOWNER
    WHERE (r.ZFIRSTNAME IS NOT NULL OR r.ZLASTNAME IS NOT NULL)
    ORDER BY r.ZLASTNAME, r.ZFIRSTNAME, e.ZADDRESS, p.ZFULLNUMBER
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone'])

        # Write contact data
        for row in results:
            first_name = row[0] or ""
            last_name = row[1] or ""
            email = row[2] or ""
            phone = row[3] or ""

            # Clean up data
            first_name = first_name.strip() if first_name else ""
            last_name = last_name.strip() if last_name else ""
            email = email.strip() if email else ""
            phone = phone.strip() if phone else ""

            writer.writerow([first_name, last_name, email, phone])

    conn.close()

    # Print summary
    total_rows = len(results)
    print(f"Exported {total_rows} contact records to {output_path}")

    return total_rows

def main():
    """Main function to run the contact conversion."""

    # Set up command line argument parser
    parser = argparse.ArgumentParser(
        description="Convert Apple AddressBook (.abbu) contacts to CSV format"
    )
    parser.add_argument(
        "--in",
        dest="input_file",
        required=True,
        help="Path to the .abbu file or AddressBook database file"
    )
    parser.add_argument(
        "--out",
        dest="output_file",
        required=True,
        help="Output CSV file path (including filename)"
    )

    args = parser.parse_args()

    # Determine the database path
    input_path = Path(args.input_file)

    if input_path.is_dir() and input_path.suffix == ".abbu":
        # If it's an .abbu directory, find the AddressBook database with the most contacts
        db_files = list(input_path.glob("**/AddressBook*.abcddb"))
        if not db_files:
            print(f"Error: No AddressBook database found in {input_path}")
            sys.exit(1)

        # Find the database with the most contacts
        best_db = None
        max_contacts = 0

        print(f"Found {len(db_files)} database files, checking for contacts...")
        for db_file in db_files:
            contact_count = count_contacts_in_db(str(db_file))
            print(f"  {db_file.name}: {contact_count} contacts")
            if contact_count > max_contacts:
                max_contacts = contact_count
                best_db = str(db_file)

        if best_db is None or max_contacts == 0:
            print("Error: No database contains contact records")
            sys.exit(1)

        print(f"Using database with {max_contacts} contacts: {Path(best_db).name}")
        db_path = best_db
    elif input_path.suffix == ".abcddb":
        # Direct path to database file
        db_path = str(input_path)
    else:
        print(f"Error: Input must be either a .abbu directory or .abcddb database file")
        sys.exit(1)

    # Check if database exists
    if not Path(db_path).exists():
        print(f"Error: Database file not found: {db_path}")
        sys.exit(1)

    # Extract contacts
    try:
        extract_contacts_to_csv(db_path, args.output_file)
        print("✅ Conversion completed successfully!")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
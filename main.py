#!/usr/bin/python3
"""A simple commandline interface to use a sqlite database as a way to define dns-rpz zone to block resolving of bad domains"""
import configparser
import sqlite3
import sys
from datetime import datetime

VALID_COMMANDS = [
    "add",
    "remove",
    "search",
    "render"
]

ZONEHEAD = """
$TTL	{}
@	IN	SOA	localhost. root.localhost. (
\t\t{}; Serial
\t\t{}\t\t; Refresh
\t\t{}\t\t; Retry
\t\t{}\t\t; Expire
\t\t{}\t\t)	; Negative Cache TTL
;
@	IN	NS	localhost.
"""

HELP = """
RPZ-blocklist
A command line interface to block some domains from being resolved for DNS-blocking purposes.
Developed for a complement to adguard DNS.

COMMANDS
\t add DOMAIN \t appends the specified domain to the blocklist.
\t remove DOMAIN \t pops the specified domain from the blocklist.
\t search DOMAIN \t checks if the specified domain is in the blocklist.
\t render \t \t renders a bind9 rpz-zone at the location defined in config.ini
"""
NOW = datetime.now()

def add_domain(domain: str):
    """Appends the <domain> to the domain-blacklist database defined in config.ini"""
    try:
        cursor.execute("INSERT INTO domains(domain) VALUES('{}');".format(domain))
        connection.commit()
        print("Sucessfully appended {} to blocklist".format(domain))
    except sqlite3.IntegrityError:
        print("Could not append {} to blocklist, duplicate entry".format(domain))
    finally:
        connection.close()

def remove_domain(domain: str):
    """Pops the <domain> from the domain-blacklist database defined in config.ini"""
    try:
        cursor.execute("DELETE FROM domains WHERE domain = '{}';".format(domain))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()

def search(domain: str):
    """Searches for <domain> in the database and returns it if found"""
    result = []
    for record in cursor.execute("SELECT domain FROM domains where domain LIKE '%{}%'".format(domain)):
        result.append(record)
    if len(result) > 0:
        print(result)
    else:
        print("No domains found")

def display_help():
    """Displays a help screen"""
    print(HELP)

def render_zone():
    """renders a dns-zone and prints it to console"""
    print(ZONEHEAD.format(
        config.get("zone", "ttl"),
        NOW.strftime("%y%m%d%H%M"),
        config.get("zone", "refresh"),
        config.get("zone", "retry"),
        config.get("zone", "expire"),
        config.get("zone", "negative_cache_ttl")
    ))
    for domain in cursor.execute("SELECT domain FROM domains"):
        print("{} \tCNAME\t.".format(domain[0]))


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read("/etc/dns-blacklist/config.ini")
        connection = sqlite3.connect(config.get('database', 'file'))
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS domains(domain text PRIMARY KEY NOT NULL, UNIQUE(domain));''')
        connection.commit()

    except sqlite3.Error as error:
        print("Database error: {}".format(error))
        sys.exit(50)
    except configparser.Error as error:
        print("Config error: {}".format(error))
        sys.exit(60)

    if len(sys.argv[1:]) > 0:
        subcommand = sys.argv[1]
        data = sys.argv[2] if len(sys.argv[1:]) > 1 else ""

        if subcommand in VALID_COMMANDS:
            if subcommand == "add":
                add_domain(data)
            elif subcommand == "remove":
                remove_domain(data)
            elif subcommand == "search":
                search(data)
            elif subcommand == "render":
                render_zone()
        else:
            display_help()
    else:
        display_help()

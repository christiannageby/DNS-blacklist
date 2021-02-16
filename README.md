# DNS-blacklist
Dns-blacklist is a command line interface which purpose is to build bind9 RPZ-zones to block dns-resolving of specified domains.
The main storage for the domains is inside a sqlite3 database for easier management, however the rendering of the zone needs to be runt manuall, or maye with a crontab.

## Configuration
All the parameters that is configurable is located inside of config.ini

## Installation

## Usage
To use the program run the DNS-balcklist command like this:
`dns-blacklist <subcommand> <value>`

### Add
The add subcommand is used to add a bad domain to the bad-domains database.
`dns-blacklist add test.com`

### Remove 
The remove subcommand is used to remove a domain from the blacklist.
`dns-blacklist remove test.com`

### Search
The search subcommand is used to search for a domain in the bad-domains database.
The search is perfored with SQL's LIKE statement `domain LIKE '%domain%';`.
`dns.blacklist search test.com`

### Render
Displays a bind9 rpz-zone. Output might be redirected to a file.
Serial number is current date and time (Hour:minute) and all other parameters is defined in config.ini
`dns-blacklist render > db.rpz`
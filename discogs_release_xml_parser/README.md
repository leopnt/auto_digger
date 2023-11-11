# Discogs release xml parser

Parse discogs release XML into MariaDB MySQL Database

## Instruction

1. Create `.env` file in this directory with DB connection parameters

   ```txt
   USER='myusername'
   PASS='mypassword'
   IP_OR_HOSTNAME='mariadb_service_ip'
   PORT='mariadb_service_port'
   DB_NAME='mariadb_database_name'
   ```

2. Run

   ```shell
   cargo run -- <path/to/discogs_release.xml>
   ```

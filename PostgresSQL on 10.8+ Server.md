#### About PostgresSQL

First off make OS X Server a little more posix friendly...
```shell
sudo ln -s /Library/Server/PostgreSQL\ For\ Server\ Services/Socket/ /var/pgsql_server_socket
```
when you're working with the server postgres you'll want to use the provided postgres install so...
```shell
cd /Applications/Server.app/Contents/ServerRoot/usr/bin
```
and you can take a look at the avaliable tables and their owners via this
```shell
sudo ./psql -h /var/pgsql_server_socket -U _postgres --list
serveradmin start postgres_server
```
then back up the db's
```shell
./pg_dump -h /Library/Server/PostgreSQL\ For\ Server\ Services/Socket --username=caldav caldav > ~/Desktop/caldav.sql
./pg_dump -h /Library/Server/PostgreSQL\ For\ Server\ Services/Socket --username=_devicemgr device_management > ~/Desktop/device_management.sql  
```
on 10.9 caldav is dynamic so use find to locate the actual dir it's a little different
```shell
CALDAV_SQL=`find /var/run/caldavd -name ccs_postgres_*`
./pg_dump -h ${CALDAV_SQL} --username=caldav caldav > ~/Desktop/caldav.sql
```

here's how to wipe the Profile Manager
```shell
/Applications/Server.app/Contents/ServerRoot/usr/share/devicemgr/backend/wipeDB.sh

sudo ./pg_dumpall  -h /var/pgsql_server_socket --username=_postgres > ~/Desktop/pg_all.sql

sudo serveradmin stop postgres_server
sudo serveradmin start postgres_server
```
then to restore
```shell
sudo ./createdb -h /var/pgsql_server_socket -U _postgres postgres
sudo ./psql -h /var/pgsql_server_socket -U _postgres -f ~/Desktop/pg_all.sql
```
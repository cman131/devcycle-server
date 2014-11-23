## Scripts
This folder contains scripts that can be used to insert test data into the DCS Postgres database. 

Use:  `psql -d DCS -f /path/to/script/script.sql` for running scripts without having to connect

1. `reset_rider_and_affgroup.sql`: SQL script to reset the "rider\_rider" and "affinity\_group" tables. This script will not only truncate and delete all data, but it also will set the sequence number for each table back to 1 so that when you insert a record, it starts at 1. 

2. `insert_rider_affinity_group.sql`: This will not only truncate the tables and reset the sequence back to 1, but it will also come up with random id's for the rider id and affinity group id's. This script <b>MAY HAVE TO BE RAN MULTIPLE TIMES</b> until it inserts. because the random may try to insert a rider id and affinity group that was already defined. This script is a transaction so it's either all or nothing.

3. `location_test_setup.sql`: Inserts a tour config, tour route, and location data for riders
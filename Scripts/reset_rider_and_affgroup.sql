/*
* 	reset_rider_and_affgroup.sql
* 	author: Joshua Eklund
*
* 	Description: SQL script to reset the rider_rider and affinity_group 
* 	tables. This script will not only truncate and delete all data, but it also
* 	will set the sequence number for each table back to 1 so that when you
* 	insert a record, it starts at 1. 
*/

BEGIN;
	--Delete all data in rider_rider, location_update_location, and rider_affinity_group_mapping tables
	truncate rider_rider cascade;
	--Delete all data in the affinity_group tables
	truncate affinity_group cascade;
	
	--Reset PKEYS to 1
	ALTER SEQUENCE rider_rider_id_seq RESTART WITH 1;
	UPDATE rider_rider SET id = DEFAULT;
	
	ALTER SEQUENCE affinity_group_id_seq RESTART WITH 1;
	UPDATE affinity_group SET id = DEFAULT;
	
	ALTER SEQUENCE rider_affinity_group_mapping_id_seq RESTART WITH 1;
	UPDATE rider_affinity_group_mapping SET id = DEFAULT;

COMMIT;
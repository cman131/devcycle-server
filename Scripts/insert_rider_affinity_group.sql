/*
* 	insert_rider_affinity_group.sql
* 	author: Joshua Eklund
* 	Description: SQL script to test the database for the  affinity group and rider relationships that exist
* 	between the rider_rider table, the affinity_group table, and the rider_affinity_group_mapping table
* 
* This will not only truncate the tables and reset the sequence back to 1, but it will also come up with random 
* id's for the rider id and affinity group id's. This script MAY HAVE TO BE RAN MULTIPLE TIMES until it inserts.
* because the random may try to insert a rider id and affinity group that was already defined. This script is a '
* transaction so it's either all or nothing. 
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
	
	
	--Insert values
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'android 4.2', round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'iOS 7'  , round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'kindle', round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'nook', round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'iOS 8', round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());
	INSERT INTO rider_rider VALUES(nextval('rider_rider_id_seq'), 'android 4.1.1', round(random() * 9999999999999), round(random() * 9999999999999), clock_timestamp());

	INSERT INTO affinity_group VALUES(nextval('affinity_group_id_seq'), 'Ronald Mc. Donald House', 'RMCD', clock_timestamp());
	INSERT INTO affinity_group VALUES(nextval('affinity_group_id_seq'), 'Bike New York', 'BNY', clock_timestamp());
	INSERT INTO affinity_group VALUES(nextval('affinity_group_id_seq'), 'Target', 'TRGT', clock_timestamp());
	INSERT INTO affinity_group VALUES(nextval('affinity_group_id_seq'), 'Walmart', 'WMRT', clock_timestamp());
	
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));
	INSERT INTO rider_affinity_group_mapping VALUES(nextval('rider_affinity_group_mapping_id_seq'),  floor(random()*(currval('affinity_group_id_seq')-1)+1), floor(random()*(currval('rider_rider_id_seq')-1)+1));

COMMIT;

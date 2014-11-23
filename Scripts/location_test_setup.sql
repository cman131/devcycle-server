INSERT INTO tour_config_tourroute(id, name, route) VALUES(1, 'Toms Test Route', 
'0105000020E610000001000000010200000005000000EB3981F0048052C0999B6699E25C4440DA3981D0158052C04150F41D565B4440843A8190CF7E52C05B51409AEF5B4440263A81207B7F52C05FD47D7D115D
4440BE3981C0078052C0CB61FB1FEB5C4440');

INSERT INTO tour_config_tourconfig(id, tour_name, tour_logo, tour_id, tour_organization, dcs_url, gcm_sender_id, is_cancelled, tour_route_id, start_time, max_tour_time, 
server_polling_rate, location_polling_rate, server_polling_range) VALUES(1, 'Toms Test Tour', '~/', 1, 'Centri-Pedal', 'centri-pedal2.se.rit.edu', 'lol', false, 1, 
1394573283, 1000, 10, 10, 10);

INSERT INTO location_update_location (id, time, rider_id, provider, coords, tour_id_id) VALUES
(1, 1394573283, 1, 'GPS', ST_GeomFromText('POINT(40.771204 -73.972337)', 4326), 1),
(2, 1394573283, 2, 'GPS', ST_GeomFromText('POINT(40.614803 -74.064370)', 4326), 1),
(3, 1394573283, 3, 'GPS', ST_GeomFromText('POINT(40.773647 -73.959856)', 4326), 1),
(4, 1394573283, 4, 'GPS', ST_GeomFromText('POINT(40.798215 -73.952367)', 4326), 1),
(5, 1394573283, 5, 'GPS', ST_GeomFromText('POINT(40.802060 -73.949755)', 4326), 1),
(6, 1394573283, 6, 'GPS', ST_GeomFromText('POINT(40.814068 -73.940801)', 4326), 1);
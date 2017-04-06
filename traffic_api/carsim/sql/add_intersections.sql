\COPY traffic_api_intersectiondata (id,latitude,longitude,street_a,street_b)
FROM 'intersections.csv' DELIMITER ',' CSV;

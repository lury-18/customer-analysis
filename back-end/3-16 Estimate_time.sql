USE olist;

/*
Please help me to create this table!
*/
CREATE VIEW geo_avg AS
SELECT zip_code, AVG(latitude) AS latitude, AVG(longitude) AS longitude, city, state
FROM geo_loc
GROUP BY zip_code, city, state;

/*
Please help me to create this table as well! Thanks a lot!
*/
CREATE VIEW time_table_7 AS
SELECT customer_id, order_id, s.seller_id,
       DATEDIFF(approval_time,purchase_time)*24*60*60 + TIME_TO_SEC(approval_time) - TIME_TO_SEC(purchase_time) AS approval_duration,
       DATEDIFF(delivered_carrier,purchase_time)*24*60*60 + TIME_TO_SEC(delivered_carrier) - TIME_TO_SEC(purchase_time) AS carrier_duration,
       DATEDIFF(delivered_customer,purchase_time)*24*60*60 + TIME_TO_SEC(delivered_customer) - TIME_TO_SEC(purchase_time) AS customer_duration,
	   g1.latitude AS cust_lat, g1.longitude AS cust_long, g2.latitude AS seller_lat, g2.longitude AS seller_long,
       p.weight, p.length_cm, p.height_cm, p.width_cm,
       oi.shipping_limit_date AS carrier_limit, o.estimated_delivery
FROM orders o
INNER JOIN customers c
USING (customer_id)
INNER JOIN order_items oi
USING (order_id)
INNER JOIN geo_avg g1
ON g1.zip_code = c.zip_code
INNER JOIN seller s
ON s.seller_id = oi.seller_id
INNER JOIN geo_avg g2
ON g2.zip_code = s.zip_code
INNER JOIN products p
ON p.product_id = oi.product_id
WHERE o.order_status = 'delivered'
AND customer_id IS NOT NULL
AND order_id IS NOT NULL
AND s.seller_id IS NOT NULL
AND delivered_customer IS NOT NULL
AND purchase_time IS NOT NULL
AND approval_time IS NOT NULL
AND delivered_carrier IS NOT NULL
AND delivered_customer IS NOT NULL
AND g1.latitude IS NOT NULL
AND g2.latitude IS NOT NULL
AND oi.shipping_limit_date IS NOT NULL
AND o.estimated_delivery IS NOT NULL
AND p.weight IS NOT NULL
AND p.length_cm IS NOT NULL
AND p.height_cm IS NOT NULL
AND p.width_cm IS NOT NULL;

CREATE VIEW time_table_8 AS
SELECT customer_id, order_id, s.seller_id,
       DATEDIFF(approval_time,purchase_time) AS approval_duration,
       DATEDIFF(delivered_carrier,purchase_time) AS carrier_duration,
       DATEDIFF(delivered_customer,purchase_time) AS customer_duration,
	   g1.latitude AS cust_lat, g1.longitude AS cust_long, g2.latitude AS seller_lat, g2.longitude AS seller_long,
       p.weight, p.length_cm, p.height_cm, p.width_cm,
       oi.shipping_limit_date AS carrier_limit, o.estimated_delivery
FROM orders o
INNER JOIN customers c
USING (customer_id)
INNER JOIN order_items oi
USING (order_id)
INNER JOIN geo_avg g1
ON g1.zip_code = c.zip_code
INNER JOIN seller s
ON s.seller_id = oi.seller_id
INNER JOIN geo_avg g2
ON g2.zip_code = s.zip_code
INNER JOIN products p
ON p.product_id = oi.product_id
WHERE o.order_status = 'delivered'
AND customer_id IS NOT NULL
AND order_id IS NOT NULL
AND s.seller_id IS NOT NULL
AND delivered_customer IS NOT NULL
AND purchase_time IS NOT NULL
AND approval_time IS NOT NULL
AND delivered_carrier IS NOT NULL
AND delivered_customer IS NOT NULL
AND g1.latitude IS NOT NULL
AND g2.latitude IS NOT NULL
AND oi.shipping_limit_date IS NOT NULL
AND o.estimated_delivery IS NOT NULL
AND p.weight IS NOT NULL
AND p.length_cm IS NOT NULL
AND p.height_cm IS NOT NULL
AND p.width_cm IS NOT NULL;

SELECT COUNT(*) FROM time_table_6;

/*
Try to improve model accuracy 3/18
*/

SELECT * FROM time_table;

SELECT COUNT(*) FROM time_table;

# We have 96213 0's in 117355 orders
SELECT approval_duration, COUNT(*) 
FROM (SELECT TRUNCATE(approval_duration/24/60/60, 0) AS approval_duration FROM time_table) AS sq
GROUP BY approval_duration;

# Average of approval time is 0.2726.
SELECT AVG(TRUNCATE(approval_duration/24/60/60, 0)) FROM time_table;

/*
In overall 117355 orders, we have 96213 0 days in approval time. The average of approval time is 0.2726
So I think it's reasonable to predict approval time as 0 days.
*/

/*
Prediction for delivery time to logistic partner
idea: 
*/


# 476 sellers made over 50 deals
SELECT COUNT(*)
FROM (SELECT seller_id,COUNT(*) AS seller_count FROM time_table GROUP BY seller_id ORDER BY seller_count DESC) AS subq
WHERE seller_count >= 50;

SELECT seller_id,COUNT(*) AS seller_count FROM time_table GROUP BY seller_id ORDER BY seller_count DESC;

CREATE VIEW seller_filter AS
SELECT seller_id
FROM (SELECT seller_id,COUNT(*) AS seller_count FROM time_table GROUP BY seller_id ORDER BY seller_count DESC) AS subq
WHERE seller_count >= 50;

CREATE VIEW time_table_1 AS
SELECT 
    TRUNCATE(carrier_duration/24/60/60, 0) AS carrier_duration,
    cust_lat,
    cust_long,
    seller_lat,
    seller_long
FROM
    time_table t
WHERE
    t.seller_id IN (SELECT 
            seller_id
        FROM
            (SELECT 
                seller_id, COUNT(*) AS seller_count
            FROM
                time_table
            GROUP BY seller_id
            ORDER BY seller_count DESC) AS subq
        WHERE
            seller_count >= 50);

SELECT * FROM time_table_1;


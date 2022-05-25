/*
Dataset description is on https://www.kaggle.com/olistbr/brazilian-ecommerce/?select=olist_customers_dataset.csv
*/

USE olist;
SELECT * FROM customers;
SELECT COUNT(*) FROM customers; # 99441 customers

SELECT * FROM geo_loc;
SELECT COUNT(DISTINCT zip_code) FROM geo_loc; # 19015
SELECT DISTINCT(city) FROM geo_loc;
SELECT DISTINCT(state) FROM geo_loc;
SELECT COUNT(*) FROM geo_loc; # Geometric Location correspond to zip_code, 1000163 rows

SELECT * FROM prod_cat_name;
SELECT COUNT(*) FROM prod_cat_name; # portugese name vs english name, 71 rows (category_name)

SELECT * FROM products;
SELECT COUNT(*) FROM products; # 32951 rows

SELECT * FROM seller;
SELECT COUNT(*) FROM seller; # 3095 rows

SELECT * FROM order_items;
SELECT COUNT(*) FROM order_items; # 112650 rows

SELECT * FROM order_reviews;
SELECT COUNT(*) FROM order_reviews; # 99223 rows

SELECT * FROM orders;
SELECT COUNT(*) FROM orders; # 99441 rows

SELECT * FROM payments;
SELECT COUNT(*) FROM payments; # 103886 rows

/*
Some potential models:
1. Estimate the delivery time for a customer in any city
2. Return the overall rating for certain seller
3. Return the estimated price for a item (given catagory of the item, length/width of the item, weight of the item etc.)
4. Estiamte the freight value given the customer position, order_item etc.
5. Recommend a seller for a certain catagory based on seller rating, No. of reviews, delivered rate, etc.
*/


SELECT COUNT(*) FROM time_table;
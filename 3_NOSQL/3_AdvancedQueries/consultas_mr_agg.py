# -*- coding: utf-8 -*-
"""
Authors: Jorge Ferreiro & Tommaso Innocenti
Implicit Schema
+------------------------------------------------------+
| key                | types  | occurrences | percents |
| ------------------ | ------ | ----------- | -------- |
| _id                | String |           1 |    100.0 |
| country            | String |           1 |    100.0 |
| gender             | String |           1 |    100.0 |
| orders             | Array  |           1 |    100.0 |
| orders.XX.item     | String |           1 |    100.0 |
| orders.XX.quantity | Number |           1 |    100.0 |
| orders.XX.total    | Number |           1 |    100.0 |
+------------------------------------------------------+

orders is an array with attributes (item, quantity and total)

"""

# Importaciones
import pymongo
from bottle import get, run, template, route, static_file
from pymongo import MongoClient 
from bson.son import SON
from bson.code import Code

# Assets: adding support to use images on the view
@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='views/')

client 	= MongoClient()
db 		= client['giw']

# MapReduce: usuarios en cada pais.
@get('/users_by_country_mr')
def users_by_country_mr():

	mapper = Code("""
		function countryMap() {
			emit(this.country, { count: 1 });
		}
		""")

	reducer = Code("""
		function countryReduce(key, values) {
			var total = 0;

			for (var i = 0; i < values.length; i++) {
				total += Math.round(values[i].count);
			}

			print(typeof(total))
			return { count: NumberInt(total) }
		}
		""")

	results = db.users.inline_map_reduce(mapper, reducer)
	return template('table_map_reduce', results=results, count=len(results));

# Aggregation Pipeline: 
# usuarios en cada pais (orden descendente por numero de usuarios).
@get('/users_by_country_agg')
def users_by_country_agg():
	
	pipeline = [
		{"$group": {"_id": "$country", "count": {"$sum": 1}}},
		{"$sort": SON([("count", -1), ("_id", -1)])}
	]

	results= list(db.users.aggregate(pipeline))
	return template('table_pipeline', results=results, count=len(results));

# MapReduce: gasto total en cada pais.
@get('/spending_by_country_mr')
def spending_by_country_mr():

	mapper = Code("""
		function mapper() {
			var total = 0;
			var orders = this.orders;

			if (orders) { // Don't access null orders
				for (i=0; i < orders.length; i++) {
					total += orders[i].total
				}
			}

			emit(this.country, { count: total });
		}
	""")

	reducer = Code("""
		function reducer(key, values) {
			var total = 0;

			for (var i = 0; i < values.length; i++) {
				total += values[i].count;
			}

			return { count: total }
		}
	""")

	results = db.users.inline_map_reduce(mapper, reducer)
	return template('table_map_reduce', results=results, count=len(results));

# Aggregation Pipeline: 
# gasto total en cada pais (orden ascendente por el nombre del pais)
@get('/spending_by_country_agg')
def spending_by_country_agg():
	
	pipeline = [
		{"$unwind": "$orders" },
		{"$group": {"_id": "$country", "count": {"$sum": "$orders.total" }}},
		{"$sort": SON([("_id", 1)])}
	]

	results= list(db.users.aggregate(pipeline))
	return template('table_pipeline', results=results, count=len(results));

# MapReduce: gasto total realizado por las mujeres que han realizdo EXACTAMENTE
# 3 compras.
@get('/spending_female_3_orders_mr')
def spending_female_3_orders_mr():
	
	total = 0

	mapper = Code("""
		function spendingMap() {	
			if (this.gender == "Female") {
				var total = 0;
				var orders = this.orders;

				if (orders) {
					if (orders.length == 3) {
						for (i=0; i < orders.length; i++) {
							total += orders[i].total
						}
					}
					emit(this.gender, total);
				}
			}
		}
	""")

	reducer = Code("""
		function spendingReduce(key, values) {
			var total = 0;

			for (var i = 0; i < values.length; i++) {
				total += values[i]
			}

			return total;
		}
	""")

	results = db.users.inline_map_reduce(mapper, reducer)
	if len(results) > 0: total= results[0]['value'] # set total with the result of the query
	return template('totalfemale', total=total);

# Aggregation Pipeline: gasto total realizado por las mujeres que han realizdo 
# EXACTAMENTE 3 compras.
@get('/spending_female_3_orders_agg')
def spending_female_3_orders_agg():

	total 	= 0

	pipeline = [
		{ "$match" : { 
			"gender" : "Female", 
			"orders": { "$size" : 3 }} 
		},
		{ "$unwind": "$orders" },
		{ "$group": {
			"_id": "$gender", 
			"count": {"$sum": "$orders.total" }}
		},
		{
			"$project" : {
				"_id": 0,
				"count": 1
			}
		}
	]
	
	results	= list(db.users.aggregate(pipeline))
	if len(results) > 0: total= results[0]['count'] # set total with the result of the query

	return template('totalfemale', total=total);

	
###############################################################################
###############################################################################

if __name__ == "__main__":
	run(host='localhost',port=8080,debug=True)

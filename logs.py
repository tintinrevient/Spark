from __future__ import print_function
from pyspark.sql import SparkSession
from pyspark.sql.types import BooleanType
import sys

if __name__ == "__main__":
	spark = SparkSession.builder.getOrCreate()
	sc = spark.sparkContext

	ghLog = spark.read.json(sys.argv[1])

	pushes = ghLog.filter("type = 'PushEvent'")
	grouped = pushes.groupBy("actor.login").count()
	ordered = grouped.orderBy(grouped['count'], ascending=False)

	# Broadcast the employees set
	employees = [line.rstrip('\n') for line in open(sys.argv[2])]
	bcEmployees = sc.broadcast(employees)

	def isEmployee(user):
		return user in bcEmployees.value

	spark.udf.register("SetContainsUdf", isEmployee, returnType=BooleanType())
	filtered = ordered.filter("SetContainsUdf(login)")

	filtered.write.format(sys.argv[4]).save(sys.argv[3])
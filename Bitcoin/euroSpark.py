import mysql.connector
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

spark = SparkSession.builder.appName("KafkaSpark").getOrCreate()
sc=spark.sparkContext
ssc=StreamingContext(sc,20)

# Define schema for the incoming JSON data
schema = StructType([
    StructField("time", StructType([
        StructField("updated", StringType()),
        StructField("updatedISO", StringType()),
        StructField("updateduk", StringType())
    ])),
    StructField("disclaimer", StringType()),
    StructField("chartName", StringType()),
    StructField("bpi", StructType([
        StructField("USD", StructType([
            StructField("code", StringType()),
            StructField("symbol", StringType()),
            StructField("rate", StringType()),
            StructField("description", StringType()),
            StructField("rate_float", DoubleType())
        ])),
        StructField("GBP", StructType([
            StructField("code", StringType()),
            StructField("symbol", StringType()),
            StructField("rate", StringType()),
            StructField("description", StringType()),
            StructField("rate_float", DoubleType())
        ])),
        StructField("EUR", StructType([
            StructField("code", StringType()),
            StructField("symbol", StringType()),
            StructField("rate", StringType()),
            StructField("description", StringType()),
            StructField("rate_float", DoubleType())
        ]))
    ]))
])

# Read messages from Kafka topic
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bitcoin-price-euro") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert the value column from binary to string
df = df.selectExpr("CAST(value AS STRING)")

## Parse the JSON data and extract the fields
parsed_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*") \
    .select("time.updated","bpi.EUR.code", "bpi.EUR.rate_float")


# Define the function to insert data into the database
def write_to_mysql(row):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password123#@!",
        database="Bitcoin"
    )

    # Create cursor object
    cursor = mydb.cursor()

    # Define the SQL query to insert data into the table
    query = "INSERT INTO euroBitcoin(time,code,rate) VALUES (%s,%s,%s)"

    # Execute the SQL query with the row data
    cursor.execute(query, (row.updated,row.code,row.rate_float))

    # Commit the changes and close the connection
    mydb.commit()
    mydb.close()




# Write the data to the MySQL database using foreach method
parsed_df.writeStream.outputMode("append").format("console").foreach(write_to_mysql).start().awaitTermination() 


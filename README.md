# Bitcoin-Insights-Real-Time-Monitoring-and-Price-Comparison

## Project Description

The project aims to develop a **real-time monitoring and price comparison system for Bitcoin**, utilizing the CoinDesk Bitcoin Price Index API. By integrating the API through Apache Kafka, users receive real-time updates on Bitcoin prices in multiple currencies. The system enables users to stay informed about the latest market fluctuations, empowering them to make timely decisions for their cryptocurrency investments or transactions.

## Purpose

The primary purpose of the project is to provide users with a seamless platform to monitor and compare Bitcoin prices across various currencies in real-time. By having access to up-to-date information, users can identify favorable exchange rates and potential investment opportunities. The system aims to enhance users' decision-making capabilities and optimize their cryptocurrency transactions.

---

## How to Run

Install MySQL on your Ubuntu system.

Open the MySQL terminal using the command: mysql -u root -p.

Execute the command to set up the MySQL user password.

Create a database named "Bitcoin" using the code provided in the "schema.txt" file.

Start the ZooKeeper server using the command: bin/zookeeper-server-start.sh config/zookeeper.properties.

Start the Kafka server using the command: bin/kafka-server-start.sh config/server.properties.

Run the Apache Spark application using the command: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 spark_streaming.py.


## Conclusion
The project is designed to collect real-time Bitcoin price data and store it for further processing. It sets the foundation for future analyses and insights into cryptocurrency trends, providing valuable information to users for well-informed decision-making.


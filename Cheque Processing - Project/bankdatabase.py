import mysql.connector

connection =mysql.connector.connect(user="deepanshu", password="rgipt@7890", host="bobhackathon.mysql.database.azure.com", port=3306, database="bankdetails")

cursor = connection.cursor()

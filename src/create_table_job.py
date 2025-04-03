# Databricks notebook source

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

catalog_name = dbutils.widgets.get("catalogo")

print(f"Using catalog: {catalog_name}")

# Get username and format for schema name test


def get_schema_name():
    user_name = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName()
    user_name = user_name.toString().split('@')[0].split('(')[1].replace('.', '_')
    return user_name


schema_name = get_schema_name()
print(f"Using schema: {schema_name}")

# Set up catalog and schema
spark.sql(f"USE CATALOG {catalog_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
spark.sql(f"USE SCHEMA {schema_name}")

# Create the table
create_table_sql = """
CREATE OR REPLACE TABLE funcionarios (
  id INT,
  nome STRING,
  departamento STRING,
  salario DOUBLE,
  cpf STRING
) USING DELTA
"""

spark.sql(create_table_sql)

# Prepare data to insert
data = [
    (1, "João Silva", "TI", 5000.00, "123.456.789-00"),
    (2, "Maria Santos", "RH", 4500.00, "987.654.321-00"),
    (3, "Pedro Oliveira", "TI", 4800.00, "456.789.123-00"),
    (4, "Ana Costa", "Financeiro", 5500.00, "789.123.456-00"),
    (5, "Carlos Santos", "Financeiro", 6000.00, "321.654.987-00"),
    (6, schema_name, "Financeiro", 6000.00, "123.456.789-10")
]

schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("nome", StringType(), False),
    StructField("departamento", StringType(), False),
    StructField("salario", DoubleType(), False),
    StructField("cpf", StringType(), False)
])

df = spark.createDataFrame(data, schema)

# Save DataFrame as a table
df.write.format("delta").mode("overwrite").saveAsTable("funcionarios")

# Verify data was inserted
result = spark.sql("SELECT * FROM funcionarios")

display(result)

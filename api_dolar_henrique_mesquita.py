# Databricks notebook source
# MAGIC %md
# MAGIC # Consumindo API do Banco Central com a cotação diária do dólar (até 30/12/2025)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Importando library pandas para extrair o dataset via api e exportar para o Azure SQL Server

# COMMAND ----------

import pandas as pd

def incoming_data(url):
    df = pd.read_csv(url)
    return df

url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial=%2701-01-2019%27&@dataFinalCotacao=%2712-31-2025%27&$top=9000&$format=text/csv&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
table_name = 'dolar_henrique_mesquita.dolar2_Stage_henrique_mesquita'

jdbcServer = "sql-estudo.database.windows.net"
jdbcDatabase = "db-estudos"
jdbcPort = 1433
jdbcUsername = "admin-azure"
jdbcPassword = "a&Ehs&HB"
jdbcUrl = f"jdbc:sqlserver://{jdbcServer}:{jdbcPort};database={jdbcDatabase};user={jdbcUsername};password={jdbcPassword}"

df = incoming_data(url)
df2 = spark.createDataFrame(df)
df2.write  \
    .format('jdbc')  \
    .mode('overwrite')  \
    .option('url', jdbcUrl) \
    .option('dbtable', table_name) \
    .save()
     
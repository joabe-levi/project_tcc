"""
Ingestao Bronze: le o JSON bruto do volume de ingestao via Auto Loader e
grava (incremental, so processa arquivo novo) na tabela Delta
pipeline_tcc.bronze.formularios.

Roda como task de Job no Databricks (compute serverless), disparado pelo
file arrival trigger definido em resources/jobs.yml.
"""

from pyspark.sql import SparkSession

VOLUME_PATH = "/Volumes/pipeline_tcc/ingestao/formularios_json/"
CHECKPOINT_SCHEMA = "/Volumes/pipeline_tcc/bronze/checkpoints/formularios/schema"
CHECKPOINT_DATA = "/Volumes/pipeline_tcc/bronze/checkpoints/formularios/data"
TARGET_TABLE = "pipeline_tcc.bronze.formularios"


def main():
    spark = SparkSession.builder.getOrCreate()

    df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", CHECKPOINT_SCHEMA)
        .option("cloudFiles.inferColumnTypes", "true")
        .option("multiLine", "true")  # arquivos gerados com json.dump(..., indent=2) - 1 objeto por arquivo
        .load(VOLUME_PATH)
    )

    query = (
        df.writeStream.format("delta")
        .option("checkpointLocation", CHECKPOINT_DATA)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(TARGET_TABLE)
    )

    query.awaitTermination()
    print(f"ingestao concluida: {TARGET_TABLE}")


if __name__ == "__main__":
    main()

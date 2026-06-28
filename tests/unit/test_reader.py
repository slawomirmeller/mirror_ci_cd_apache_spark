from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType

from us_accidents_etl.config.settings import ETLConfig
from us_accidents_etl.extract.reader import read_accidents_csv


def test_read_accidents_csv_reads_header_and_infers_schema(
    spark: SparkSession, tmp_path
):
    csv_path = tmp_path / "accidents.csv"
    csv_path.write_text(
        "Severity,Weather_Condition,City\n"
        "3,Rain,Miami\n"
        "4,Snow,Denver\n",
        encoding="utf-8",
    )

    cfg = ETLConfig(input_path=str(csv_path), output_path=str(tmp_path / "out"))

    df = read_accidents_csv(spark, cfg)

    assert df.columns == ["Severity", "Weather_Condition", "City"]
    assert isinstance(df.schema["Severity"].dataType, IntegerType)
    assert isinstance(df.schema["Weather_Condition"].dataType, StringType)
    assert [tuple(row) for row in df.collect()] == [
        (3, "Rain", "Miami"),
        (4, "Snow", "Denver"),
    ]

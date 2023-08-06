from typing import Dict, Any

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from p360_export.data.pick.ColumnMappingGetter import ColumnMappingGetter

from p360_export.data.pick.DataPickerInterface import DataPickerInterface
from p360_export.exceptions.data_picker import UserIdMappingMissingException


class GoogleAdsDataPicker(DataPickerInterface):
    def __init__(self, spark: SparkSession, column_mapping_getter: ColumnMappingGetter):
        self.__column_mapping_getter = column_mapping_getter
        self.__spark = spark

    @property
    def export_destination(self):
        return "google_ads"

    def pick(self, df: DataFrame, query: str, table_id: str, config: Dict[str, Any]) -> DataFrame:
        df.createOrReplaceTempView(table_id)

        df = self.__spark.sql(query)

        column_mapping = self.__column_mapping_getter.get(config)

        if "user_id" not in column_mapping:
            raise UserIdMappingMissingException("Mapping for user_id not specified.")

        for new_name, old_name in column_mapping.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df

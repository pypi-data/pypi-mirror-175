#  Copyright 2022 The Feathub Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import uuid

from pyflink.table import (
    Table as NativeFlinkTable,
    Schema as NativeFlinkSchema,
)

from feathub.common import types
from feathub.common.exceptions import FeathubException
from feathub.common.types import DType
from feathub.common.utils import to_java_date_format
from feathub.processors.flink.table_builder.flink_table_builder_constants import (
    EVENT_TIME_ATTRIBUTE_NAME,
)


def generate_random_table_name() -> str:
    random_sink_name = "anonymous" + str(uuid.uuid4()).replace("-", "") + "table"
    return random_sink_name


def get_schema_from_table(table: NativeFlinkTable) -> NativeFlinkSchema:
    schema_builder = NativeFlinkSchema.new_builder()
    for field_name in table.get_schema().get_field_names():
        schema_builder.column(
            field_name, table.get_schema().get_field_data_type(field_name)
        )
    schema = schema_builder.build()
    return schema


def define_watermark(
    flink_schema: NativeFlinkSchema,
    max_out_of_orderness_interval: str,
    timestamp_field: str,
    timestamp_format: str,
    timestamp_field_dtype: DType,
) -> NativeFlinkSchema:
    builder = NativeFlinkSchema.new_builder()
    builder.from_schema(flink_schema)

    if timestamp_field_dtype == types.Timestamp:
        builder.column_by_expression(EVENT_TIME_ATTRIBUTE_NAME, f"`{timestamp_field}`")
    elif timestamp_format == "epoch":
        if (
            timestamp_field_dtype != types.Int32
            and timestamp_field_dtype != types.Int64
        ):
            raise FeathubException(
                "Timestamp field with epoch format only supports data type of "
                "Int32 and Int64."
            )
        builder.column_by_expression(
            EVENT_TIME_ATTRIBUTE_NAME,
            f"CAST("
            f"  FROM_UNIXTIME(CAST(`{timestamp_field}` AS INTEGER)) "
            f"AS TIMESTAMP(3))",
        )
    else:
        if timestamp_field_dtype != types.String:
            raise FeathubException(
                "Timestamp field with non epoch format only "
                "supports data type of String."
            )
        java_datetime_format = to_java_date_format(timestamp_format).replace(
            "'", "''"  # Escape single quote for sql
        )
        builder.column_by_expression(
            EVENT_TIME_ATTRIBUTE_NAME,
            f"TO_TIMESTAMP(`{timestamp_field}`, '{java_datetime_format}')",
        )

    builder.watermark(
        EVENT_TIME_ATTRIBUTE_NAME,
        watermark_expr=f"`{EVENT_TIME_ATTRIBUTE_NAME}` "
        f"- {max_out_of_orderness_interval}",
    )
    return builder.build()

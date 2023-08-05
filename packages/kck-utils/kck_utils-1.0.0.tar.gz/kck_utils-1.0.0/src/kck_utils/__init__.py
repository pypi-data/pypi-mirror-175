import logging
from logging import config as log_config


class CallbackUtils:
    def __init__(self,
                 logging_url: str):
        self.logging_url = logging_url
        log_config.fileConfig(self.logging_url, disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def parse_callback_data(self, callback_data: str) -> dict:
        self.logger.debug("Entering function")
        params = [
            "apps",
            "story",
            "scene",
            "page",
            "action"
        ]
        output = dict()
        parts = callback_data.split(":")
        output["apps"] = parts[0].split(".")
        for param in params:
            if len(parts) > params.index(param) + 1:
                output[param] = parts[params.index(param)]
            else:
                output[param] = None
        return output


class DBUtils:
    def __init__(self,
                 logging_url: str):
        self.logging_url = logging_url
        log_config.fileConfig(self.logging_url, disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def column_list_to_column_string(self, column_list: list[list[str]]) -> str:
        self.logger.debug("Entering function")
        column_string = ""
        for item in column_list:
            column_name = item[0]
            column_string = column_string + column_name + ", "
        if column_string.endswith(", "):
            column_string = column_string[:-len(", ")]
        return column_string

    def update_sql(self, input_sql: list[dict], table_name: str, key_column: str, key_value) -> list[dict]:
        self.logger.debug("Entering function")
        output_sql = [dict()]
        output_sql[0]["sql"] = input_sql[0]["sql"].replace("<table_name>", table_name)
        output_sql[0]["sql"] = output_sql[0]["sql"].replace("<key_column>", key_column)
        output_sql[0]["sql"] = output_sql[0]["sql"].replace("<key_value>", str(key_value))
        output_sql[0]["expects_results"] = input_sql[0]["expects_results"]
        return output_sql

from homecloud import HomeCloudClient, on_fail
import json
import requests


class HailmaryClient(HomeCloudClient):
    def __init__(
        self,
        app_name: str = "hailmary",
        send_logs: bool = True,
        log_send_thresh: int = 10,
        log_level: str = "INFO",
        timeout: int = 10,
    ):
        super().__init__(app_name, send_logs, log_send_thresh, log_level, timeout)

    @on_fail
    def hello(self) -> str:
        """Contacts the server and returns the app name."""
        self.logger.debug(f"Saying hello to the {self.app_name} server.")
        return json.loads(self.send_request("get", "/homecloud").text)["app_name"]

    @on_fail
    def get_content(
        self,
        paths: list[str],
        includes_pattern: list[str] = [],
        excludes_pattern: list[str] = [],
    ) -> dict[str, str]:
        """Return requested content in a dictionary where
        the key is a relative file path and the value is the file content.

        All requested files must be relative to the 'serving_directory'
        field in homecloud_config.toml.

        If a requested resource is not a sub path of 'serving_directory' and/or
        doesn't exist, it'll will be silently dropped from the returned results."""
        response = self.send_request(
            "get",
            "/content",
            data={
                "paths": paths,
                "includes_pattern": includes_pattern,
                "excludes_pattern": excludes_pattern,
            },
        )
        files = json.loads(response.text)
        received_files = "\n".join([f"'{file}'" for file in files])
        self.logger.info(f"Received the following files:\n{received_files}")
        return files

    @on_fail
    def get_serving_directory(self) -> str:
        response = self.send_request("get", "/serving-directory")
        return response.text


if __name__ == "__main__":
    from pathlib import Path

    c = HailmaryClient()
    f = Path(c.get_serving_directory())
    print(f)

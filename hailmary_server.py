import os
from pathlib import Path
from fastapi import FastAPI
import lanutils
from homecloud.homecloud_logging import get_logger
import tomlkit
import argparse

import hailmary_get_routes
import hailmary_post_routes

root = Path(__file__).parent
config = tomlkit.loads((root / "homecloud_config.toml").read_text())

app = FastAPI()
app.include_router(hailmary_get_routes.router)
app.include_router(hailmary_post_routes.router)
logger = get_logger("hailmary_server")


def get_port_range() -> tuple[int, int]:
    """Get port_range from 'homecloud_config.toml'.
    Need to do all this casting because tomlkit class types
    mess things up."""
    port_range = tuple(config["port_range"])
    return (int(port_range[0]), int(port_range[1]))


def get_serving_address() -> tuple[str, int]:
    print("Obtaining ip address...")
    ip = lanutils.get_myip()[0][0]
    print("Finding available port in range...")
    port = lanutils.get_available_port(ip, get_port_range())
    return (ip, port)


def start_server(uvicorn_args: list[str] = ["--reload"]):
    logger = get_logger("hailmary_server")
    ip, port = get_serving_address()
    logger.info(f"Server started: http://{ip}:{port}")
    os.system(
        f"uvicorn {Path(__file__).stem}:app {' '.join(uvicorn_args)} --host {ip} --port {port}"
    )


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--serving_directory",
        type=str,
        default=None,
        help=""" Sets the 'serving_directory' in homecloud_config.toml
        to this value. Files can only be accessed and transferred if
        they are relative to the 'serving_directory'.""",
    )

    args = parser.parse_args()

    return args


def main():
    args = get_args()
    if args.serving_directory:
        config["serving_directory"] = args.serving_directory
        (root / "homecloud_config.toml").write_text(tomlkit.dumps(config))
    elif config["serving_directory"].strip() == "":
        raise RuntimeError(
            f"No serving directory in config. Add manually to 'homecloud_config.toml' or pass it to this script with the '-s/--serving_directory' switch."
        )
    if not Path(config["serving_directory"]).exists():
        raise FileNotFoundError(
            f"Serving directory '{Path(config['serving_directory'])}' doesn't exist."
        )
    print(f"Serving files below {config['serving_directory']}")
    start_server(config["uvicorn_args"])


if __name__ == "__main__":
    main()

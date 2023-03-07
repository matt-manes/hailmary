from fastapi import APIRouter
import hailmary_request_models
from homecloud import homecloud_logging
from pathlib import Path
import tomlkit

root = Path(__file__).parent
router = APIRouter()
logger = homecloud_logging.get_logger("hailmary_server")


@router.get("/homecloud")
def homecloud(request: hailmary_request_models.Request) -> dict:
    # You can add to the payload here if you want
    # but don't remove anything or the server will be
    # undiscoverable by homecloud clients.
    logger.info(f"{request.host} says hello")
    return {"app_name": "hailmary", "host": request.host, "cwd": Path.cwd()}


@router.get("/serving-directory")
def get_serving_directory() -> Path:
    config = tomlkit.loads((root / "homecloud_config.toml").read_text())
    directory = Path(config["serving_directory"])
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' doesn't exist.")
    else:
        return directory


@router.get("/content")
def get_content(request: hailmary_request_models.ContentRequest) -> dict[str, str]:
    """Return requested content in a dictionary where
    the key is a relative file path and the value is the file content.

    All requested files must be relative to the 'serving_directory'
    field in homecloud_config.toml.

    If a requested resource is not a sub path of 'serving_directory' and/or
    doesn't exist, it'll will be silently dropped from the returned results."""
    if type(request.paths) == str:
        request.paths = [request.paths]
    requested_resources = ", ".join(f"'{path}'" for path in request.paths)
    logger.info(
        f"{request.host} is requesting {requested_resources}\nincludes_pattern: '{request.includes_pattern}'\nexcludes_pattern: '{request.excludes_pattern}'"
    )
    serving_directory = get_serving_directory()
    content = {}
    files = []
    for path in request.paths:
        path = Path(path)
        if not path.is_absolute():
            path = serving_directory / path
        path = path.resolve()
        if not path.is_relative_to(serving_directory) or not path.exists():
            continue
        if path.is_dir():
            files.extend([file for file in path.rglob("*")])
        else:
            files.append(path)
    if request.includes_pattern:
        files = [
            file
            for file in files
            if any(file.match(pattern) for pattern in request.includes_pattern)
        ]
    if request.excludes_pattern:
        files = [
            file
            for file in files
            if all(not file.match(pattern) for pattern in request.excludes_pattern)
        ]
    for file in files:
        if file.is_file():
            sub_path = file.relative_to(serving_directory)
            try:
                content[sub_path] = file.read_text()
            except:
                content[sub_path] = ""
    print([c for c in content])
    return content

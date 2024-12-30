from pathlib import Path
import subprocess

import cerberus
import toml

config_file = Path("config.toml")
logs_dir = Path("logs/")

logs_dir.mkdir(exist_ok=True)  # Ensure logs dir exists
config_file.touch()  # Ensure that the file exists

# Schema for config file
schema = {
    "id": {
        "type": "dict",
        "schema": {
            "owners": {
                "type": "list",
                "schema": {"type": "integer"},
                "required": True,
            },
            "developers": {
                "type": "list",
                "schema": {"type": "integer"},
                "required": True,
            },
        },
        "required": True,
    },
    "logger": {
        "type": "dict",
        "schema": {
            "filepath": {"type": "string", "required": True},
            "mode": {"type": "string", "allowed": ["a", "w"], "required": True},
            "max_bytes": {"type": "integer", "min": 0, "required": True},
            "backup_count": {"type": "integer", "min": 0, "required": True},
            "encoding": {"type": "string", "required": True},
            "format": {"type": "string", "required": True},
        },
        "required": True,
    },
    "commands": {
        "type": "dict",
        "schema": {
            "prefix": {"type": "string", "required": True},
            "strip_after_prefix": {"type": "boolean", "required": True},
            "case_insensitive": {"type": "boolean", "required": True},
            "hello": {
                "type": "dict",
                "schema": {
                    "cooldown": {"type": "integer", "min": 0, "required": True},
                    "responses": {
                        "type": "list",
                        "schema": {"type": "string"},
                        "required": True,
                    },
                },
                "required": True,
            },
        },
        "required": True,
    },
}

v = cerberus.Validator(schema)  # type: ignore
config_data = toml.loads(config_file.read_text())

# Validate data
if not v.validate(config_data):  # type: ignore
    raise Exception(f"{str(config_file)} schema validation failed!", v.errors)  # type: ignore

try:
    subprocess.run(["python", "-m", "riko"])
except KeyboardInterrupt:
    print("KeyboardInterrupt signal detected. Shutting down.")

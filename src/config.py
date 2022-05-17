from dataclasses import MISSING, Field, dataclass, field
from dataclasses_json import dataclass_json, config
import dotenv


def _int_field(*args, **kwargs) -> Field:
    return field(*args, **kwargs, metadata=config(encoder=str, decoder=int))


@dataclass_json
@dataclass(frozen=True)
class BotConfig:
    DISCORD_BOT_TOKEN: str

    COMMAND_PREFIX: str = field(default="!")

    DISCORD_ERROR_CHANNEL_ID: int = _int_field(default=975919254815784962)
    DISCORD_DOWNTIME_ALERT_CHANNEL_ID: int = _int_field(default=975919733658509422)



def load_config() -> BotConfig:
    return BotConfig.from_dict(dotenv.dotenv_values())


def _get_field_value_or_example(field: Field) -> object:
    if field.default is not MISSING:
        return field.default

    if field.type is int:
        return 123456

    if field.type is float:
        return 123.456

    if field.type is str:
        return "string"

    return field.type.__name__


def generate_example_env():
    lines = []
    current_section = ""

    for name, field in BotConfig.__dataclass_fields__.items():
        if (section := name.split("_")[0]) != current_section:
            current_section = section
            lines.append("\n")

        lines.append(f"{name}={_get_field_value_or_example(field)}\n")

    with open("example.env", "w+") as example_env:
        example_env.writelines(lines[1:])


if __name__ == "__main__":
    generate_example_env()

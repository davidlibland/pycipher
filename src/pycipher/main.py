"""The main entrypoint"""
from pathlib import Path
from random import shuffle

import click
import yaml

from pycipher.ciphers.keyword import KeywordCipher
from pycipher.ciphers.substitution import UPPERCASE_LETTERS, SubstitutionCipher


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file", type=click.Path(path_type=Path))
@click.option(
    "--config",
    "-c",
    type=click.Path(path_type=Path),
    help="The config for the cipher.",
)
@click.option(
    "--encode/--decode",
    is_flag=True,
    type=bool,
    show_default=True,
    default=True,
    help="Whether to encode or decode the message",
)
def file(file, config, encode):
    with file.open() as f:
        message = f.read()

    with config.open() as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    result = run(message, config, encode)
    with (file.parent / f"{file.stem}_decoded.txt").open("w") as f:
        f.write(result)


@cli.command()
@click.argument("message", type=str)
@click.option(
    "--config",
    "-c",
    type=click.Path(path_type=Path),
    help="The config for the cipher.",
)
@click.option(
    "--encode/--decode",
    is_flag=True,
    type=bool,
    show_default=True,
    default=True,
    help="Whether to encode or decode the message",
)
def message(message, config, encode):
    with config.open() as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    result = run(message, config, encode)

    click.echo(result)


def run(message, config, encode):
    cipher_type = config["cipher_type"]
    match cipher_type:
        case "substitution":
            alphabet = config["substitution"]
            cipher = SubstitutionCipher(shuffled_alphabet=alphabet)
        case "keyword":
            keyword = config["keyword"]
            cipher = KeywordCipher(keyword=keyword)
        case _:
            raise click.ClickException(
                f"Unrecoginized cipher type: {cipher_type}"
            )

    if encode:
        return cipher.encode(message)
    else:
        return cipher.decode(message)


@cli.command()
@click.argument("output_file", type=click.Path(path_type=Path, dir_okay=False))
def make_config(output_file):
    """Make a config"""
    ciphers = {
        "substitution": SubstitutionCipher,
    }
    cipher_type = click.prompt(
        f"What cipher would you like to make a config for? ({'/'.join(ciphers)})",
        type=str,
    )
    config = {"cipher_type": cipher_type}
    match cipher_type:
        case "substitution":
            make_random = click.prompt(
                "Do you want to generate a random permutation?", type=bool
            )
            if make_random:
                alphabet = list(UPPERCASE_LETTERS)
                shuffle(alphabet)
                alphabet = "".join(alphabet)
            else:
                alphabet = click.prompt(
                    "Please enter an alphabet permutation:", type=str
                )
                alphabet = alphabet.upper()
            try:
                SubstitutionCipher(alphabet)  # Test that the cipher builds.
            except Exception as e:
                raise click.ClickException(str(e))
            config["substitution"] = alphabet
        case "keyword":
            keyword = click.prompt(
                "What keyword would you like to use?", type=str
            )
            config["keyword"] = keyword
        case _:
            raise click.ClickException(
                f"Unrecoginized cipher type: {cipher_type}"
            )
    with output_file.open("w") as f:
        yaml.dump(config, f)


if __name__ == "__main__":
    cli()

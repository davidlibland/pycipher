"""
Use the click testrunner to ensure that we can run the CLI and generate some coverage.
"""
import click.testing as c_test

from pycipher.main import cli


def test_cli():
    """ensure that we can print something using the cli"""
    runner = c_test.CliRunner()
    result = runner.invoke(
        cli,
        [],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, "failed to run"

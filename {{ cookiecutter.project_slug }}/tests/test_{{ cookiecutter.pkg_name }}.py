from typer.testing import CliRunner

from {{ cookiecutter.pkg_name }}.main import app

runner = CliRunner()


def test_{{ cookiecutter.pkg_name }}():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World!" in result.stdout

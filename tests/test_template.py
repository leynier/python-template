from typer.testing import CliRunner

from template.main import app

runner = CliRunner()


def test_template():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World!" in result.stdout

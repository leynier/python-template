import os


def test_requirements():
    os.system(
        "poetry export -f requirements.txt -o requirements_temp.txt --without-hashes"
    )
    with open("./requirements.txt") as actual:
        with open("./requirements_temp.txt") as temp:
            actual_lines = actual.readlines()
            temp_lines = temp.readlines()
            for actual_line, temp_line in zip(actual_lines, temp_lines):
                actual_line = actual_line.split(";")[0].strip("\r\n").strip("\n")
                temp_line = temp_line.split(";")[0].strip("\r\n").strip("\n")
                assert actual_line == temp_line, "requirements.txt not updated"

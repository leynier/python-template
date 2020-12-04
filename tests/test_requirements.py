import os


def test_requirements():
    os.system(
        "poetry export -f requirements.txt -o requirements_temp.txt --without-hashes"
    )
    with open("./requirements.txt") as actual:
        with open("./requirements_temp.txt") as temp:
            actual_str = actual.read()
            temp_str = temp.read()
            print("----------------------------------")
            print(actual_str)
            print("----------------------------------")
            print(temp_str)
            print("----------------------------------")
            assert actual_str == temp_str, "requirements.txt not updated"

import pytest

from spindex import print_warnings, Color


def test_print_warnings_should_not_print_any_output_when_no_warnings(capsys):

    # Arrange
    warnings: list[str] = []
    header: str = "Test title"
    action: str = "test action"
    abort = True

    # Act
    print_warnings(warnings, header, action, abort)
    captured = capsys.readouterr()

    # Assert
    assert len(captured.out) == 0


def test_print_warnings_should_abort_when_at_least_one_warning(capsys):

    # Arrange
    warnings: list[str] = ["test warning"]
    header: str = "Test title"
    action: str = "test action"
    abort = True

    # Act / Assert
    with pytest.raises(SystemExit):
        print_warnings(warnings, header, action, abort)

    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"\n{header}\n{Color.red.value}\n{warnings[0]}\n"


def test_print_warnings_should_abort_when_the_user_chooses_not_to_take_the_associated_action(capsys, monkeypatch):

    # Arrange
    warnings: list[str] = ["test warning"]
    header: str = "Test title"
    action: str = "test action"
    abort = False

    # monkeypatch the "input" function, so that it returns "n".
    # This simulates the user entering "n" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "n")

    # Act / Assert
    with pytest.raises(SystemExit):
        print_warnings(warnings, header, action, abort)

    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"\n{header}\n{Color.red.value}\n{warnings[0]}\n{Color.default.value}\n"


def test_print_warnings_should_abort_when_the_user_chooses_any_non_y_value(capsys, monkeypatch):

    # Arrange
    warnings: list[str] = ["test warning"]
    header: str = "Test title"
    action: str = "test action"
    abort = False

    # monkeypatch the "input" function, so that it returns "O".
    # This simulates the user entering "O" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "O")

    # Act / Assert
    with pytest.raises(SystemExit):
        print_warnings(warnings, header, action, abort)

    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"\n{header}\n{Color.red.value}\n{warnings[0]}\n{Color.default.value}\n"


def test_print_warnings_should_not_abort_when_the_user_chooses_to_continue(capsys, monkeypatch):

    # Arrange
    warnings: list[str] = ["test warning"]
    header: str = "Test title"
    action: str = "test action"
    abort = False

    # monkeypatch the "input" function, so that it returns "y".
    # This simulates the user entering "y" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "y")

    # Act
    print_warnings(warnings, header, action, abort)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"\n{header}\n{Color.red.value}\n{warnings[0]}\n"


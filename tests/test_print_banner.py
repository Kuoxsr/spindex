from sound_pack_indexer import print_banner, Color


def test_print_banner_should_build_banner_correctly(capsys):

    dummy_variable: str = "nonsense"
    title = "Processing test banner:"
    info = f"This is the {dummy_variable} that should appear under the banner"
    print_banner(title, info)

    captured = capsys.readouterr()

    # Assert
    bar = "------------------------"
    assert captured.out == f"{Color.green.value}\n{bar}\n{title}\n{bar}\n{Color.cyan.value}{info}{Color.default.value}\n"


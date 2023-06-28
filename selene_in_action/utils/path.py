def relative_from_root(path: str):
    import selene_in_action
    from pathlib import Path

    return (
        Path(selene_in_action.__file__)
        .parent.parent.joinpath(path)
        .absolute()
        .__str__()
    )

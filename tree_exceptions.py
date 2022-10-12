class DuplicateKeyException:
    def __init__(self, key: str) -> None:
        Exception.__init__(self, f'{key} already exists.')

"""패키지·도구 연결 스모크 테스트 (구현 전 플레이스홀더)."""


def test_magic_square_package_importable() -> None:
    import magic_square

    assert magic_square.__doc__

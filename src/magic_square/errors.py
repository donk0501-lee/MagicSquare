"""계약 예외 타입만 정의 (GREEN에서 경계·도메인이 채움)."""


class MagicSquareContractError(Exception):
    """경계(I1~I4) 또는 대외 오류 스키마 (code + message)."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class MagicSquareDomainError(Exception):
    """도메인 실패(예: 두 시도 모두 비마방진). 경계에서 NOT_MAGIC_SQUARE로 매핑."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)

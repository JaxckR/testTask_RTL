from typing import override


class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error occurred"

    def __str__(self) -> str:
        return self.message


class TokensExpiredError(ApplicationError):
    @override
    @property
    def message(self) -> str:
        return "Токены закончились. Напишите, пожалуйста, позже"

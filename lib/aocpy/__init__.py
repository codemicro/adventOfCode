from typing import Any


class BaseChallenge:

    @staticmethod
    def one(instr: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def two(instr: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def vis(instr: str, outputDir: str) -> Any:
        raise NotImplementedError

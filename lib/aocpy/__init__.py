from typing import Any


class BaseChallenge:

    def one(self, instr: str) -> Any:
        raise NotImplementedError

    def two(self, instr: str) -> Any:
        raise NotImplementedError

    def vis(self, instr: str, outputDir: str) -> Any:
        raise NotImplementedError

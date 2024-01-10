import os
from typing import Any, Dict, Union

from .errors import InvalidFileTypeError, SyntaxErrorFile
from .parser import get_parser


class Env:
    """Reads the environment variables"""

    def __init__(
        self,
        path: str = 'core/.env'
    ) -> None:
        self.path = self._validate_path(path=path)

    def load_environ(self, modify=True) -> Union[Dict, None]:
        """Loads the environment variables

        Args:
            modify (bool, optional): Modifies the os.environ. Defaults to True.

        Raises:
            SyntaxErrorFile: Syntax error in the file.

        Returns:
            Dict: Environment variables. If modify is true.
            None: If modify is true.
        """
        environ = self._create_environ()
        for index, item in self._read_environ_file():
            if not len(item) or item.startswith('#'):
                continue
            if '=' not in item:
                raise self._get_error(
                    index=index, message='The "=" symbol is required')

            key, value = item.split('=')
            key, type_ = key.split(':') if ':' in key else (key, 'str')
            environ[key] = self._parsear(
                value=value, type_=type_, index=index)

        if not modify:
            return environ
        os.environ = environ.copy()

    def _parsear(self, value: str, type_: str, index: int) -> Any:
        parser = get_parser(type_=type_)
        if parser is None:
            raise self._get_error(
                index=index, message='The type is not valid')
        try:
            return parser(value)
        except ValueError:
            raise self._get_error(
                index=index,
                message=f'The value "{value}" is not of type "{type_}"'
            )

    def _get_error(self, index: int, message: str) -> SyntaxErrorFile:
        return SyntaxErrorFile(
            f'Syntax error on line {index+1} of the .env file. {message}.')

    def _validate_path(self, path: str):
        if not path.endswith('.env'):
            raise InvalidFileTypeError('The file type is not valid.')
        return path

    def _read_environ_file(self) -> enumerate:
        with open(self.path) as file:
            return enumerate(file.read().splitlines())

    def _create_environ(self) -> Dict:
        environ: Dict = {}
        environ.update(os.environ.copy())
        return environ

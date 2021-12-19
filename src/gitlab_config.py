import configparser
import re
from dataclasses import dataclass

from pathlib import Path
from typing import Union

import git


@dataclass
class GitLabConfig():
    url: str
    token: str = None
    protocol: str = 'http'

    def __post_init__(self):
        self.project = ProjectManager(self)

    @classmethod
    def from_config_file(cls: 'GitLabConfig', config_file: Union[str, Path]) -> 'GitLabConfig':
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        if not config_file.exists():
            raise FileExistsError('Config file not found!')

        config = GitLabConfigParser(config_file)
        cls.protocol = config.protocol
        cls.url = config.url
        cls.token = config.token
        return cls(protocol=config.protocol, url=config.url, token=config.token)


@dataclass
class GitLabConfigParser():
    protocol: str = 'http'
    url: str = None
    token: str = None

    def __init__(self, path: Union[str, Path]) -> None:

        self._config = configparser.ConfigParser()
        self._config.read(path)

        try:
            _url = self._config.get('gitlab', 'url')
            pattern = re.compile('https?://')
            if re.search(pattern, _url):
                sw = _url.split('://')
                self.protocol = sw[0]
                _url = sw[1]
            self.url = _url
        except Exception:
            pass
        try:
            self.token = self._config.get('gitlab', 'token')
        except Exception:
            pass


class Manager():
    def __init__(self, gl: GitLabConfig) -> None:
        self.gitlab = gl


class ProjectManager(Manager):

    def clone(self, project_name: str, save_path: Union[str, Path]) -> git.Repo:
        token = f'oauth2:{t}@' if (t := self.gitlab.token) else ''
        url = f'{self.gitlab.protocol}://{token}{self.gitlab.url}/{project_name}'
        save_path = save_path if isinstance(save_path, Path) else Path(save_path)
        if save_path.exists():
            print('Save path already exsists!')
            return None
        return git.Repo.clone_from(url, save_path)

from pathlib import Path

import git

from gitlab_config import GitLabConfig

if __name__ == '__main__':

    # gl = GitLabConfig('localhost')
    gitlab = GitLabConfig.from_config_file('data/gitlab.cfg')
    print(gitlab)
    repo_path = Path('data/aaa')
    repo = git.Repo(repo_path) if repo_path.exists() else gitlab.project.clone('test01/aa01', repo_path)

    print(repo)

    print(repo.untracked_files)

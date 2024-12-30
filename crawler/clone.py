

import subprocess
import os
def clone_github_repo(repo_url, destination_path=None):
    if not repo_url:
        raise ValueError("The repository URL must not be empty.")

    try:
        os.mkdir("../" + destination_path)
        command = ["git", "clone", repo_url]
        if destination_path:
            command.append(destination_path)

        subprocess.run(command, check=True)
        return f"Repository cloned successfully to {'current directory' if not destination_path else destination_path}."

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone repository: {e}")

    

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler.clone import clone_github_repo
from readmeAI.create_readme import create_readme
def main(repo):
    # clone_github_repo(repo_url=repo, destination_path="cloned_repository_new")
    
    create_readme("cloned_repository_new")





if __name__ == "__main__":
    repository = "https://github.com/alirezadaghigh99/DL-Bench"
    main(repository)
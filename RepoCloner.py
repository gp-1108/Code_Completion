from git import Repo
import os
import json

class RepoCloner:
    PARSERS = {
        ".py": "handle_default",
        ".ipynb": "handle_ipynb",
        ".cpp": "handle_default",
        ".hpp": "handle_default",
    }

    def __init__(self, repo_url: str, repo_dir: str = "./temp") -> None:
        self.repo_url = repo_url
        self.repo_dir = repo_dir
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
        else:
            os.system(f"rm -rf {self.repo_dir}")
            os.makedirs(self.repo_dir)
        self.files = self._get_files()

    def _get_files(self) -> list[str]:
        # Clone the repository into the directory
        repo = Repo.clone_from(self.repo_url, self.repo_dir)

        # Initialize an empty list to store the contents of allowed files
        files_content = []

        # Walk through the repo_dir to find all files
        for root, _, files in os.walk(self.repo_dir):
            for file in files:
                try:
                    # Get the file path
                    file_path = os.path.join(root, file)

                    # Get the file extension
                    file_ext = os.path.splitext(file_path)[1]

                    # Check if the file extension is allowed
                    if file_ext in self.PARSERS.keys():
                        # Read the file content
                        with open(file_path, "r") as f:
                            file_content = f.read()

                        # Get the handler for the file extension
                        handler = getattr(self, self.PARSERS[file_ext])
                        handled_content = handler(file_content)

                        if handled_content:
                            files_content.append(handled_content)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        # Return the list of files' contents
        return files_content

    def get_files(self) -> list[str]:
        return self.files
    
    def handle_default(self, file_content: str) -> str:
        return file_content
    
    def handle_ipynb(self, file_content: str) -> str:
        # Extracting only the code cells from the notebook
        notebook = json.loads(file_content)

        # Initialize an empty string to store the code cells
        code_cells = []

        # Loop through the cells in the notebook
        for cell in notebook["cells"]:
            # Check if the cell is a code cell
            if cell["cell_type"] == "code":
                # Extract the source code from the cell
                code_cells.append("\n".join(cell["source"]))
        
        return "".join(code_cells)


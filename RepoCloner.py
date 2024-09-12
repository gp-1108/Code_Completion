"""
Author: Pietro Girotto
Date: 12/07/2024
Description: This module contains the RepoCloner class, which is designed to clone a repository from a given URL,
    process files with specific extensions, and retrieve their contents.
"""
from git import Repo
import os
import json

class RepoCloner:
    """
    RepoCloner is a class designed to clone a repository from a given URL,
    process files with specific extensions, and retrieve their contents.
    Attributes:
        PARSERS (dict): A dictionary mapping file extensions to their respective handler methods.
    Methods:
        __init__(repo_url: str, repo_dir: str = "./temp") -> None:
            Initializes the RepoCloner instance with the repository URL and directory.
        _get_files() -> list[str]:
            Clones the repository, processes files with allowed extensions, and returns their contents.
        get_files() -> list[str]:
            Retrieves the list of all files' content.
        handle_default(file_content: str) -> str:
        handle_ipynb(file_content: str) -> str:
    """
    PARSERS = {
        ".py": "handle_default",
        ".ipynb": "handle_ipynb",
        ".cpp": "handle_default",
        ".hpp": "handle_default",
    }

    def __init__(self, repo_url: str, repo_dir: str = "./temp") -> None:
        """
        Initializes the RepoCloner instance.

        Args:
            repo_url (str): The URL of the repository to clone.
            repo_dir (str, optional): The directory where the repository will be cloned. Defaults to "./temp".

        Raises:
            OSError: If the directory cannot be created or removed.
        """
        self.repo_url = repo_url
        self.repo_dir = repo_dir
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
        else:
            os.system(f"rm -rf {self.repo_dir}")
            os.makedirs(self.repo_dir)
        self.files = self._get_files()

    def _get_files(self) -> list[str]:
        """
        Clones the repository from the specified URL into the specified directory,
        walks through the directory to find all files, and processes the contents
        of files with allowed extensions using their respective handlers.

        Returns:
            list[str]: A list containing the processed contents of the allowed files.

        Raises:
            Exception: If there is an error reading any file, it will be caught and
                       printed, but the function will continue processing other files.
        """
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
        """
        Retrieve the list of all files' content.

        Returns:
            list[str]: A list of strings containing the content of all files.
        """
        return self.files
    
    def handle_default(self, file_content: str) -> str:
        """
        Handles the default case by returning the provided file content unchanged.

        Args:
            file_content (str): The content of the file to be processed.

        Returns:
            str: The unchanged file content.
        """
        return file_content
    
    def handle_ipynb(self, file_content: str) -> str:
        """
        Extracts and concatenates the source code from all code cells in a Jupyter notebook.
        Args:
            file_content (str): The JSON content of the Jupyter notebook as a string.
        Returns:
            str: A single string containing the concatenated source code from all code cells.
        """
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


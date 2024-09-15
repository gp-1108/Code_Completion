from torch.utils.data import Dataset
import random

class CodeDataset(Dataset):
    def __init__(self, file_contents: list[str], num_samples: int = 50, 
                 min_lengths: tuple = (20, 10, 20), max_lengths: tuple = (200, 50, 200)):
        """
        Args:
            file_contents (list[str]): A list of strings, where each string is the content of a code file.
            num_samples (int): The number of code completion examples to generate.
            min_lengths (tuple): A tuple (x, y, z) where x is the min prefix length, y is the min middle length, and z is the min suffix length.
            max_lengths (tuple): A tuple (x, y, z) where x is the max prefix length, y is the max middle length, and z is the max suffix length.
        """
        self.examples = []
        
        # Unpack the min and max lengths for prefix, middle, and suffix
        self.min_prefix_length, self.min_middle_length, self.min_suffix_length = min_lengths
        self.max_prefix_length, self.max_middle_length, self.max_suffix_length = max_lengths
        
        # Generate code completion examples
        self._generate_examples(file_contents, num_samples)
    
    def _generate_examples(self, file_contents: list[str], num_samples: int):
        """
        Generates examples from the provided file contents.
        This method processes each content in the `file_contents` list to generate
        a specified number of samples. Each sample consists of a prefix, middle, 
        and suffix segment extracted from the content based on random lengths and 
        positions within specified constraints.
        Args:
            file_contents (list[str]): A list of strings, each representing the content 
                                       from which examples will be generated.
            num_samples (int): The number of samples to generate.
        Returns:
            None: The generated examples are stored in the `self.examples` attribute.
        """
        for content in file_contents:
            content_length = len(content)

            # Ensure the content is long enough to generate examples with min lengths
            if content_length < self.min_prefix_length + self.min_middle_length + self.min_suffix_length:
                continue
            
            for _ in range(num_samples):
                # Randomly select the middle length within the specified range
                middle_length = random.randint(self.min_middle_length, self.max_middle_length)
                
                # Randomly select the cursor position ensuring space for middle and suffix
                max_cursor_position = content_length - middle_length - self.min_suffix_length
                if max_cursor_position <= self.min_prefix_length:
                    continue

                cursor_position = random.randint(self.min_prefix_length, max_cursor_position)
                
                # Randomly determine prefix and suffix lengths based on the cursor position and available space
                prefix_length = random.randint(self.min_prefix_length, min(cursor_position, self.max_prefix_length))
                suffix_length = random.randint(self.min_suffix_length, 
                                               min(content_length - cursor_position - middle_length, self.max_suffix_length))

                # Define the prefix, middle, and suffix
                prefix = content[cursor_position - prefix_length:cursor_position]
                middle = content[cursor_position:cursor_position + middle_length]
                suffix = content[cursor_position + middle_length:cursor_position + middle_length + suffix_length]
                
                # Create a sample and add to the dataset
                self.examples.append((prefix, middle, suffix))
        
        # Restrict the dataset to num_samples by randomly selecting if necessary
        if len(self.examples) > num_samples:
            self.examples = random.sample(self.examples, num_samples)

    def __len__(self) -> int:
        """
        Returns the total number of examples in the dataset.
        Returns:
            int: The number of examples in the dataset.
        """
        return len(self.examples)
    
    def __getitem__(self, idx) -> dict:
        """
        Retrieves the example at the specified index.
        Args:
            idx (int): The index of the example to retrieve.
        Returns:
            tuple: A tuple containing the prefix, middle, and suffix segments of the example.
        """
        return self.examples[idx]

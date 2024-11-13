##
def get_instructions() -> str:
    """Function to load the instructions from `instruction.txt`

    Returns:
        str: The contents of the `instruction.txt` file as a string

    Raises:
        IOError: If there are issues reading the file
        FileNotFoundError: If `instruction.txt` does not exist in the parent directory
    """
    with open("../instruction.txt", "r") as f:
        instruction_prompt = f.read()
    return instruction_prompt


def format_query(query_data) -> str:
    """Formats and combines different sections of search query data into a single string.

    Args:
        query_data (dict): Dictionary containing search results

    Returns:
        str: Concatenated string of all available search result sections
    """
    extracted_data = """"""
    if "knowledgeGraph" in query_data:
        extracted_data += str(query_data["knowledgeGraph"])
    if "answerBox" in query_data:
        extracted_data += str(query_data["answerBox"])
    extracted_data += str(query_data["organic"])
    return extracted_data

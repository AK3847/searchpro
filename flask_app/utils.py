##
def get_instructions():
    with open("../instruction.txt", "r") as f:
        instruction_prompt = f.read()
    return instruction_prompt


def format_query(query_data):
    extracted_data = """"""
    if "knowledgeGraph" in query_data:
        extracted_data += str(query_data["knowledgeGraph"])
    if "answerBox" in query_data:
        extracted_data += str(query_data["answerBox"])
    extracted_data += str(query_data["organic"])
    return extracted_data

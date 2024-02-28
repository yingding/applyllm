import re

def parse_response_str(response: str) -> str:
    # The (?s) is a mode modifier for regular expressions in Python. It's also known as a flag. 
    # This specific flag, (?s), is short for DOTALL, which is a mode that allows . to match any character 
    # including newline characters.
    # the dot . matches any character except a newline. You can use the DOTALL mode to match new line.
    # replace // patient weight in kilograms\n} with \n}
    # return re.sub(r"(?s)//.*}", "}", response) is a short form of the following
    return re.sub(r"//.*}", "\n}", response, flags=re.DOTALL)
    

if __name__ == '__main__':
    response_1 = 'json { "patient_weight": "43.2" // patient weight in kilogram }'
    response_2 = 'json { "patient_weight": "45.2" }'
    response_3 = 'json\n{\n\t"patient_weight": "43.2"  // patient weight in kilograms\n}\n'

    responses = [response_1, response_2, response_3]    
    for response in responses:
        processed_response = parse_response_str(response)
        print(processed_response)  # json { "patient_weight": "43.2" }
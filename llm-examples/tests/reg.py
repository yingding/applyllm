import re

def parse_response_str(response: str) -> str:
    # replace // patient weight in kilogram } with }
    return re.sub(r"//.*}", "}", response)
    

if __name__ == '__main__':
    response_1 = """json { "patient_weight": "43.2" // patient weight in kilogram }"""
    response_2 = """json { "patient_weight": "45.2" }"""

    responses = [response_1, response_2]    
    for response in responses:
        processed_response = parse_response_str(response)
        print(processed_response)  # json { "patient_weight": "43.2" }
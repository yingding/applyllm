import re

def parse_response_str(response: str) -> str:
    # The (?s) is a mode modifier for regular expressions in Python. It's also known as a flag. 
    # This specific flag, (?s), is short for DOTALL, which is a mode that allows . to match any character 
    # including newline characters.
    # the dot . matches any character except a newline. You can use the DOTALL mode to match new line.
    # replace // patient weight in kilograms\n} with \n}
    # return re.sub(r"(?s)//.*}", "}", response) is a short form of the following
    return re.sub(r"//.*}", "\n}", response, flags=re.DOTALL)

def search_response_str(response: str) -> str:
    if not re.search(r"}.*```", response, flags=re.DOTALL):
        post_proccessed_response = response + "}\n```"
    else:
        post_proccessed_response = response

    # remove the leading and tailing text outside the ``` ```
    post_proccessed_response = re.search(
        r"```[\s\S]+```", post_proccessed_response
    ).group(0)

    # remove the comment // patient weight in kilogram \n} and keep the \n}
    # re.DOTALL is a flag that makes . match newlines as well, since default . doesn't match newline characters
    post_proccessed_response = re.sub(r"//.*}", "\n}", post_proccessed_response, flags=re.DOTALL)
    return post_proccessed_response


def exp_1():
    print("exp_1")
    response_1 = '```json { "patient_weight": "43.2" // patient weight in kilogram }'
    response_2 = '```json { "patient_weight": "45.2" }'
    response_3 = '```json\n{\n\t"patient_weight": "43.2"  // patient weight in kilograms\n}\n'

    responses = [response_1, response_2, response_3]    
    for response in responses:
        processed_response = parse_response_str(response)
        print(repr(processed_response))  # json { "patient_weight": "43.2" }


def exp_2():
    print("exp_2")
    response_1 = '```json { "patient_weight": "43.2"'
    response_2 = '```json { "patient_weight": "45.2" '
    response_3 = '```json\n{\n\t"patient_weight": "43.2" \n'
    response_4 = '```json { "patient_weight": "45.2" }\n```'
    response_5 = '```json { "patient_weight": "45.2"\n}\n```'
    response_6 = '```json { "patient_weight": "45.2" }```'

    responses = [response_1, response_2, response_3, response_4, response_5, response_6 ]    
    for response in responses:
        processed_response = search_response_str(response)
        print(repr(processed_response))

if __name__ == '__main__':
    exp_1()
    exp_2()
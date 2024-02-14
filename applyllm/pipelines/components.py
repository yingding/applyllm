import re
from langchain.output_parsers.structured import StructuredOutputParser

class StructuredOutputParserHelper:
    @classmethod
    def parse_response_str(
        clz, parser_response: str, output_parser: StructuredOutputParser, verbose: bool = False
    ) -> dict:
        # https://stackoverflow.com/questions/24667065/python-regex-difference-between-and/24667099#24667099
        # https://stackoverflow.com/questions/33312175/matching-any-character-including-newlines-in-a-python-regex-subexpression-not-g/33312193#33312193
        # (.+) is greedy, (.+?) stops at the first match
        try:
            post_proccessed_response = re.search(
                r"```[\s\S]+```", parser_response
            ).group(0)
            if verbose:
                print(post_proccessed_response)
            output_dict = output_parser.parse(post_proccessed_response)
            key = output_parser.response_schemas[0].name
            if output_dict.get(key) is None:
                output_dict[key] = ""
        except Exception as e:
            print(e)
            output_dict = {}
        return output_dict

    @classmethod
    def parse_response_dict(
        clz,
        parser_response: dict,
        output_parser: StructuredOutputParser,
        text_key: str = "text",
        verbose: bool = False,
    ) -> dict:
        parser_response_str = parser_response.get(text_key, "")
        return clz.parse_response_str(
            parser_response=parser_response_str,
            output_parser=output_parser,
            verbose=verbose,
        )

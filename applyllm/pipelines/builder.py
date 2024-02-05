class KwargsBuilder:
    """
    merge the kwargs from the list of kwargs for the Transformer model or pipeline
    """
    def __init__(self, args_list: list = []):
        self.kwargs = {}
        self.args_list = args_list


    def append(self, kwargs: dict):
        self.args_list.append(kwargs)
        return self


    def build(self):
        # https://peps.python.org/pep-0584/
        # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python
        # merge dictionary python 3.9 |= operator, python 3.8 {**d1, **d2}
        for kwargs in self.args_list:
            self.kwargs = {**self.kwargs, **kwargs}
        return self.kwargs


    def __repr__(self) -> str:
        return self.kwargs 
    

    def __str__(self) -> str:
        return self.__repr__()
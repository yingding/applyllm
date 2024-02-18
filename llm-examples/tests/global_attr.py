
global_1 = 1

def f(attrs):
    name = 'global_1'
    return {name: getattr(attrs, name, None)}
    
if __name__ == "__main__":
    global_1 = 1
    print(__dict__)
    print(f())

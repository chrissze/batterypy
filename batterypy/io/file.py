import os

def writefile(path, content, mode='w'):
    try:
        filepath = os.path.expanduser(path)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)        
        with open(filepath, mode) as f:
            f.write(content)
    except:
        with open(path, mode) as f:
            f.write(content)

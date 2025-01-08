def remove_extra_whitespace(s: str) -> str:
    if s is None or s == "":
        return s
    return " ".join(s.split())

def read_from_file(filename : str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == "__main__":
    print(read_from_file(r"D:\Projects\final-project\app\prompt-template.txt"))
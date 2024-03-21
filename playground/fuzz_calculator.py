from pathlib import Path

def main():
    file_path = Path("src/debugging_benchmark/database.py")
    print(file_path)
    fp = file_path.resolve()
    print(fp)

if __name__ == "__main__":
    main()

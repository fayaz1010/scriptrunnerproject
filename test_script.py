import sys

def main():
    if len(sys.argv) > 1:
        print(f"Received argument: {sys.argv[1]}")
    else:
        print("No arguments received")

if __name__ == "__main__":
    main()

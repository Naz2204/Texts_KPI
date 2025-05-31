import subprocess

if __name__ == "__main__":
    subprocess.run("granian --interface asgi API:app --reload")




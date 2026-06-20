import requests
import zipfile
import shutil
import os, sys

download_dict = {
    "npp": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.9.6.4/npp.8.9.6.4.portable.x64.zip",
    "dotnet": "https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.200/dotnet-sdk-10.0.200-win-x64.zip",
    "code": "https://update.code.visualstudio.com/latest/win32-x64-archive/stable"
}

def download(url, output_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def extract(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            member_path = os.path.join(extract_to, member.filename)

            if not os.path.realpath(member_path).startswith(os.path.realpath(extract_to)):
                raise Exception("Path traversal detected!")
        
        zip_ref.extractall(extract_to)

def main():
    command = sys.argv[1]

    if command == "download":
        arg = sys.argv[2]

        if arg in download_dict:
            target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{arg}\\")
            
            os.makedirs(target_path)

            download(download_dict[arg], os.path.join(target_path, f"{arg}_package.zip"))

            if os.path.exists(os.path.join(target_path, f"{arg}_package.zip")):
                extract(os.path.join(target_path, f"{arg}_package.zip"), target_path)

            else:
                raise FileNotFoundError("Installation package file not found.")
            
        else:
            raise Exception(f"'{arg}' app not found.")
    
    elif command == "remove_app":
        if sys.argv[2] in download_dict:
            target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{sys.argv[2]}\\")

            if os.path.exists(target_path):
                shutil.rmtree(target_path)
        
        else:
            raise Exception(f"'{sys.argv[2]}' app not found.")

    elif command == "make_shortcut":
        target_path = sys.argv[2]

        if os.path.exists(target_path):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{sys.argv[3]}.bat"), "w") as file:
                file.write(f"@echo off & {target_path} %1 %2 %3 %4 %5 %6 %7 %8 %9 %10")

        else:
            raise FileExistsError(f"File '{target_path}' not exists.")

    elif command == "remove_shortcut":
        shortcut = sys.argv[2]

        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{shortcut}.bat")):
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{shortcut}.bat"))

        else:
            raise FileExistsError(f"Shortcut '{shortcut}' not exists.")

    else:
        raise ValueError(f"Unknown command: '{command}'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
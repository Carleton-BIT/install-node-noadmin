import os
import zipfile
import urllib.request
import shutil
import sys
import re
from xml.etree import ElementTree
import winreg

BASE_URL = "https://nodejs.org/dist/latest/"
USER_HOME = os.environ["USERPROFILE"]
INSTALL_PARENT = os.path.join(USER_HOME, "nodejs-latest")
ZIP_PATH = os.path.join(os.environ["TEMP"], "node-latest-win-x64.zip")

def get_latest_win_x64_url():
    print("🌐 Fetching Node.js latest directory listing...")
    with urllib.request.urlopen(BASE_URL) as resp:
        html = resp.read().decode('utf-8')

    # Match any line containing the zip file for Windows x64
    # It looks like: node-v24.7.0-win-x64.zip
    matches = re.findall(r'(node-v[\d\.]+-win-x64\.zip)', html)
    if not matches:
        print("❌ Couldn't find the Windows x64 zip in the latest directory.")
        exit(1)

    # The first match is the latest version
    filename = matches[0]
    full_url = BASE_URL + filename
    return full_url, filename

def download_node(zip_url):
    print(f"📥 Downloading {zip_url}...")
    urllib.request.urlretrieve(zip_url, ZIP_PATH)
    print("✅ Download complete.")

def extract_node(filename):
    print(f"🗂 Extracting {filename} to {INSTALL_PARENT}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(INSTALL_PARENT)
    os.remove(ZIP_PATH)
    print("✅ Extraction complete.")

    subdirs = [d for d in os.listdir(INSTALL_PARENT) if os.path.isdir(os.path.join(INSTALL_PARENT, d))]
    if not subdirs:
        print("❌ Extraction failed: no subdirectory found.")
        sys.exit(1)
    node_path = os.path.abspath(os.path.join(INSTALL_PARENT, subdirs[0]))
    return node_path

def update_user_path(node_path):
    print(f"🔧 Adding {node_path} to user PATH...")
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS) as env_key:
        try:
            current_path, _ = winreg.QueryValueEx(env_key, "PATH")
        except FileNotFoundError:
            current_path = ""
        if node_path.lower() in current_path.lower():
            print("ℹ Already in user PATH.")
            return
        new_path = f"{node_path};{current_path}" if current_path else node_path
        winreg.SetValueEx(env_key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        print("✅ Updated registry PATH.")

def print_refresh_commands(node_path):
    print("\n⚡ To use Node.js **right now** in this shell, run:\n")
    print(" PowerShell:")
    print(f'$env:Path = "{node_path};" + $env:Path\n')
    print(" Also run:")
    print("Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
    print(" CMD:")
    print(f'set PATH={node_path};%PATH%\n')
    print("Then test by running:\n   node -v\n   npm -v\n   npx --version\n")

def main():
    if os.name != "nt":
        print("❌ Windows only.")
        sys.exit(1)

    zip_url, filename = get_latest_win_x64_url()
    download_node(zip_url)
    node_path = extract_node(filename)
    update_user_path(node_path)
    print_refresh_commands(node_path)
    print("🎉 Installation complete — future terminals will recognize Node.js automatically!")

if __name__ == "__main__":
    main()

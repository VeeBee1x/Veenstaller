import os
import sys
import subprocess
import ctypes
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox

# Check for admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to restart the script with admin rights if not already elevated
def restart_with_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Function to download a file
def download_file(url, file_path):
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded {file_path}")
    except Exception as e:
        print(f"Error downloading {file_path}: {e}")
        raise

# Function to install an application
def install_app(file_path, silent_flag):
    try:
        if file_path.endswith(".msi"):
            subprocess.run(["msiexec", "/i", file_path] + silent_flag.split(), check=True)
        else:
            subprocess.run([file_path] + silent_flag.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing {file_path}: {e}")
        raise

# Function to download and install applications
def download_and_install(app, progress, status_label):
    file_path = os.path.join(download_dir, app["file_name"])
    
    # Check if already downloaded
    if not os.path.exists(file_path):
        try:
            status_label.config(text=f"Downloading {app['name']}...")
            download_file(app["url"], file_path)
        except Exception as e:
            status_label.config(text=f"Failed to download {app['name']}")
            return False
    
    # Extract if zip file
    if file_path.endswith(".zip"):
        try:
            status_label.config(text=f"Extracting {app['name']}...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            file_path = os.path.join(download_dir, app["file_name"].replace(".zip", ".exe"))
        except Exception as e:
            status_label.config(text=f"Failed to extract {app['name']}")
            return False
    
    try:
        status_label.config(text=f"Installing {app['name']}...")
        if app["name"] == "Spotify":
            subprocess.run([file_path, "--silent"], check=True)
        elif app["name"] == "Brave Browser":
            subprocess.run([file_path, "/install", "/quiet", "/norestart"], check=True)
        elif app["name"] == "Steam":
            subprocess.run([file_path, "/S"], check=True)
        else:
            install_app(file_path, app["silent_flag"])
        return True
    except Exception as e:
        status_label.config(text=f"Failed to install {app['name']}")
        return False

# GUI setup
class AppInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch Application Installer")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.checkbuttons = []
        self.selected_apps = []

        for app in apps:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.scrollable_frame, text=app["name"], variable=var)
            chk.var = var
            chk.pack(anchor='w')
            self.checkbuttons.append(chk)

        self.confirm_button = tk.Button(self.scrollable_frame, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

        self.progress = ttk.Progressbar(self.scrollable_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.scrollable_frame, text="Status: Waiting to start", anchor="w")
        self.status_label.pack(fill="x", padx=20)

        self.start_button = tk.Button(self.scrollable_frame, text="Start Installation", command=self.start_installation)
        self.start_button.pack(pady=10)
        self.start_button.config(state="disabled")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def confirm_selection(self):
        self.selected_apps = [apps[i] for i, chk in enumerate(self.checkbuttons) if chk.var.get()]
        if self.selected_apps:
            self.start_button.config(state="normal")
        else:
            messagebox.showwarning("No Selection", "Please select at least one application.")

    def start_installation(self):
        self.start_button.config(state="disabled")
        total_apps = len(self.selected_apps)
        success_count = 0

        for i, app in enumerate(self.selected_apps):
            if download_and_install(app, self.progress, self.status_label):
                success_count += 1
            self.progress["value"] = (i + 1) / total_apps * 100
            self.update()

        self.status_label.config(text=f"Installation complete: {success_count}/{total_apps} succeeded.")
        messagebox.showinfo("Installation Complete", f"Installation complete: {success_count}/{total_apps} succeeded.")
        self.start_button.config(state="normal")

# Directory to store downloaded files
download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "app_installs")
os.makedirs(download_dir, exist_ok=True)

# Application list with fixed URLs and installation commands
apps = [
    {"name": "Windows .NET Runtime", "url": "https://download.visualstudio.microsoft.com/download/pr/b14af665-ca5f-40a5-b0a9-4c7ca9ff1072/dfc3ab88e4dfbcece4fb7ee5246c406b/windowsdesktop-runtime-6.0.30-win-x64.exe", "file_name": "windowsnet.exe", "silent_flag": "/silent"},
    {"name": "Google Chrome", "url": "https://dl.google.com/chrome/install/375.126/chrome_installer.exe", "file_name": "chrome_installer.exe", "silent_flag": "/silent /install"},
    {"name": "SuperF4", "url": "https://github.com/stefansundin/superf4/releases/download/v1.4/SuperF4-1.4.exe", "file_name": "superf4.exe", "silent_flag": "/S"},
    {"name": "Discord", "url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64", "file_name": "discord.exe", "silent_flag": "/S"},
    {"name": "Spotify", "url": "https://download.scdn.co/SpotifySetup.exe", "file_name": "spotify.exe", "silent_flag": "--silent"},
    {"name": "Brave Browser", "url": "https://laptop-updates.brave.com/latest/winx64", "file_name": "brave.exe", "silent_flag": "/install /quiet /norestart"},
    {"name": "Razer Synapse", "url": "https://rzr.to/synapse-3-pc-download", "file_name": "razer.exe", "silent_flag": "/silent /install"},
    {"name": "Steam", "url": "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe", "file_name": "steam.exe", "silent_flag": "/S"},
    {"name": "Epic Games Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "file_name": "epicgames.msi", "silent_flag": "/quiet"},
    {"name": "Vencord Installer", "url": "https://github.com/Vencord/Installer/releases/latest/download/VencordInstallerCli.exe", "file_name": "vencord.exe", "silent_flag": "/S"},
    {"name": "Visual Studio Code", "url": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", "file_name": "vscode.exe", "silent_flag": "/silent /mergetasks=runcode"},
    {"name": "Python", "url": "https://www.python.org/ftp/python/3.12.0/python-3.12.0b3-amd64.exe", "file_name": "python-setup.exe", "silent_flag": "/quiet InstallAllUsers=1 PrependPath=1"},
    {"name": "NVIDIA GeForce Experience", "url": "https://us.download.nvidia.com/GFE/GFEClient/3.27.0.112/GeForce_Experience_v3.27.0.112.exe", "file_name": "geforce.exe", "silent_flag": "/silent"},
    {"name": "Google Drive", "url": "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe", "file_name": "googledrive.exe", "silent_flag": "/silent"},
    {"name": "Zoom", "url": "https://zoom.us/client/latest/ZoomInstaller.exe", "file_name": "zoom.exe", "silent_flag": "/silent"},
    {"name": "MSI Afterburner", "url": "https://download.msi.com/uti_exe/vga/MSIAfterburnerSetup.zip", "file_name": "afterburner.zip", "silent_flag": "/S"},
    {"name": "Rufus", "url": "https://github.com/pbatard/rufus/releases/download/v4.1/rufus-4.1.exe", "file_name": "rufus.exe", "silent_flag": "/quiet"},
    {"name": "Python 3.12", "url": "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe", "file_name": "python312.exe", "silent_flag": "/quiet InstallAllUsers=1 PrependPath=1"},
    {"name": "Firefox", "url": "https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US", "file_name": "firefoxsetup.exe", "silent_flag": "/S"},
    {"name": "Wireshark", "url": "https://1.as.dl.wireshark.org/win64/Wireshark-win64-4.0.0.exe", "file_name": "wireshark.exe", "silent_flag": "/silent"},
    {"name": "Visual Studio Code Insiders", "url": "https://update.code.visualstudio.com/latest/win32-x64-user/insider", "file_name": "vscode-insiders.exe", "silent_flag": "/silent /mergetasks=runcode"},
    {"name": "Edge Dev", "url": "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?channel=Dev&platform=Windows_10_x64", "file_name": "edge-dev.exe", "silent_flag": "/silent"},
    {"name": "Edge Beta", "url": "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?channel=Beta&platform=Windows_10_x64", "file_name": "edge-beta.exe", "silent_flag": "/silent"},
    {"name": "Edge Canary", "url": "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?channel=Canary&platform=Windows_10_x64", "file_name": "edge-canary.exe", "silent_flag": "/silent"},
    {"name": "Firefox Nightly", "url": "https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=win64&lang=en-US", "file_name": "firefox-nightly.exe", "silent_flag": "/silent"},
    {"name": "Brave Nightly", "url": "https://laptop-updates.brave.com/latest/winx64-nightly", "file_name": "brave-nightly.exe", "silent_flag": "/silent"},
    {"name": "Brave Dev", "url": "https://laptop-updates.brave.com/latest/winx64-dev", "file_name": "brave-dev.exe", "silent_flag": "/silent"},
    {"name": "Brave Beta", "url": "https://laptop-updates.brave.com/latest/winx64-beta", "file_name": "brave-beta.exe", "silent_flag": "/silent"},
    {"name": "Tor Browser", "url": "https://www.torproject.org/dist/torbrowser/12.0.1/torbrowser-install-win64-12.0.1_ALL.exe", "file_name": "torbrowser.exe", "silent_flag": "/S"},
    {"name": "OBS Studio", "url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.2-Full-Installer-x64.exe", "file_name": "obs-studio.exe", "silent_flag": "/silent"},
    {"name": "Roblox", "url": "https://www.roblox.com/download/client?os=win", "file_name": "roblox.exe", "silent_flag": "/silent"},
    {"name": "Bloxstrap", "url": "https://github.com/pizzaboxer/bloxstrap/releases/download/v2.5.4/Bloxstrap-v2.5.4.exe", "file_name": "bloxstrap.exe", "silent_flag": "/silent"},
    {"name": "Discord Theme | TOKYO NIGHT", "url": "https://betterdiscord.app/Download?id=439", "file_name": "tokyo-night.theme.css", "silent_flag": "/silent"},
    {"name": "Notion", "url": "https://www.notion.so/desktop/windows/download", "file_name": "notion-setup.exe", "silent_flag": "/silent"},
    {"name": "WinRAR", "url": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-701.exe", "file_name": "winrar-setup.exe", "silent_flag": "/silent"},
    {"name": "7-Zip", "url": "https://www.7-zip.org/a/7z2407-x64.exe", "file_name": "7-Zip-setup.exe", "silent_flag": "/silent"},
    {"name": "VLC", "url": "https://mirror.bahnhof.net/pub/videolan/vlc/3.0.21/win32/vlc-3.0.21-win32.exe", "file_name": "VLC-setup.exe", "silent_flag": "/silent"},
    {"name": "AnyDesk", "url": "https://anydesk.com/en/downloads/thank-you?dv=win_exe", "file_name": "AnyDesk-setup.exe", "silent_flag": "/silent"},
    {"name": "WizTree", "url": "https://diskanalyzer.com/files/wiztree_4_19_setup.exe", "file_name": "WizTree-setup.exe", "silent_flag": "/silent"},
    {"name": "RevoUninstaller", "url": "https://www.revouninstaller.com/start-freeware-download/", "file_name": "Revo-setup.exe", "silent_flag": "/silent"},
    {"name": "Malwarebytes", "url": "https://www.malwarebytes.com/mwb-download/thankyou", "file_name": "Malwarebytes-setup.exe", "silent_flag": "/silent"},
    {"name": "Oracle VirtualBox", "url": "https://download.virtualbox.org/virtualbox/6.1.26/VirtualBox-6.1.26-145957-Win.exe", "file_name": "VirtualBox-setup.exe", "silent_flag": "--silent"}

]

# Ensure the script runs with admin rights
restart_with_admin()

# Run the GUI application
if __name__ == "__main__":
    app = AppInstaller()
    app.mainloop()

import os
import requests
import subprocess

def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    print(f"Downloaded {url} to {destination}")

def install_application(installer_path, silent_flag):
    if not os.path.exists(installer_path):
        print(f"Installer not found at {installer_path}")
        return
    if not os.path.isfile(installer_path):
        print(f"The path {installer_path} is not a file")
        return

    try: 
        subprocess.run([installer_path, silent_flag], check=True)  
        print(f"Successfully installed {installer_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {installer_path}. Error: {e}")
    except OSError as e:
        print(f"OS error occurred while installing {installer_path}. Error: {e}")

applications = [


    {"url": "https://download.visualstudio.microsoft.com/download/pr/b14af665-ca5f-40a5-b0a9-4c7ca9ff1072/dfc3ab88e4dfbcece4fb7ee5246c406b/windowsdesktop-runtime-6.0.30-win-x64.exe", "file_name": "windowsnet.exe", "silent_flag": "/silent"},
    {"url": "https://www.actatekusa.com/downloads/ChromeSetup.exe", "file_name": "chromesetup.exe", "silent_flag": "/silent"},
    {"url": "https://github.com/stefansundin/superf4/releases/download/v1.4/SuperF4-1.4.exe", "file_name": "superf4.exe", "silent_flag": "/S"},
    {"url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64", "file_name": "discord.exe", "silent_flag": "/S"},
    {"url": "https://download.scdn.co/SpotifySetup.exe", "file_name": "spotify.exe", "silent_flag": "/S"},
    {"url": "https://laptop-updates.brave.com/latest/winx64", "file_name": "brave.exe", "silent_flag": "/S"},
    {"url": "https://rzr.to/synapse-3-pc-download", "file_name": "razer.exe", "silent_flag": "/silent /install"},
    {"url": "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe", "file_name": "steam.exe", "silent_flag": "/S"},
    {"url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "file_name": "epicgames.msi", "silent_flag": "/quiet"},
    {"url": "https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe", "file_name": "vencord.exe", "silent_flag": "/S"},
    {"url": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", "file_name": "vscode.exe", "silent_flag": "/silent /mergetasks=runcode"},
    {"url": "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe", "file_name": "python.exe", "silent_flag": "/silent /mergetasks=runcode"},
    {"url": "https://app.prntscr.com/build/setup-lightshot.exe", "file_name": "lightshot.exe", "silent_flag": "/silent"},
    {"url": "https://download01.logi.com/web/ftp/pub/techsupport/gaming/lghub_installer.exe", "file_name": "ghub.exe", "silent_flag": "/silent"},
    {"url": "https://rzr.to/synapse-3-pc-download", "file_name": "synapse.exe", "silent_flag": "/silent"},
    {"url": "https://download.overwolf.com/install/Download?PartnerId=3986", "file_name": "r6tracker.exe", "silent_flag": "/silent"},
    {"url": "https://raw.githubusercontent.com/VeeBee1x/Veenstaller/main/bookmarks_22_05_2024.html?token=GHSAT0AAAAAACSU4PQ2UKSLF4USPKL55TZYZSQUDAA", "file_name": "bookmarks.html", "silent_flag": "/silent"},
    {"url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.2-Full-Installer-x64.exe", "file_name": "obs-studio.exe", "silent_flag": "/silent"},
    {"url": "https://www.roblox.com/download/client?os=win", "file_name": "roblox.exe", "silent_flag": "/silent"},
    {"url": "https://github.com/pizzaboxer/bloxstrap/releases/download/v2.5.4/Bloxstrap-v2.5.4.exe", "file_name": "bloxstrap.exe", "silent_flag": "/silent"}
    
   
]


for app in applications:
    download_url = app["url"]
    installer_path = app["file_name"]
    silent_flag = app["silent_flag"]
    
    download_file(download_url, installer_path)
    
    install_application(installer_path, silent_flag)

import sys
import os

# CRITIQUE: Patcher AVANT tout import de streamlit
if getattr(sys, 'frozen', False):
    import importlib.metadata
    
    _original_version = importlib.metadata.version
    _original_metadata = importlib.metadata.metadata
    
    def _patched_version(distribution_name):
        try:
            return _original_version(distribution_name)
        except importlib.metadata.PackageNotFoundError:
            if distribution_name.lower() in ['streamlit', 'altair', 'pandas', 'numpy', 'pyarrow']:
                return '1.0.0'
            raise
    
    def _patched_metadata(distribution_name):
        try:
            return _original_metadata(distribution_name)
        except importlib.metadata.PackageNotFoundError:
            if distribution_name.lower() in ['streamlit', 'altair', 'pandas', 'numpy', 'pyarrow']:
                from email.message import EmailMessage
                msg = EmailMessage()
                msg['Name'] = distribution_name
                msg['Version'] = '1.0.0'
                return msg
            raise
    
    importlib.metadata.version = _patched_version
    importlib.metadata.metadata = _patched_metadata

import time
import threading
import webbrowser
import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import streamlit.web.cli as stcli

def get_free_port():
    """Trouve un port disponible"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def get_resource_path(relative_path):
    """Obtient le chemin absolu vers une ressource"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ISO 27001 Audit Manager")
        
        splash_width = 500
        splash_height = 300
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        
        self.root.geometry(f'{splash_width}x{splash_height}+{x}+{y}')
        self.root.overrideredirect(True)
        self.root.configure(bg='#FFFFFF')
        
        main_frame = tk.Frame(self.root, bg='#FFFFFF', relief='solid', borderwidth=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        try:
            icon_path = get_resource_path('icone.ico')
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(main_frame, image=photo, bg='#FFFFFF')
                logo_label.image = photo
                logo_label.pack(pady=(40, 20))
        except Exception:
            pass
        
        title_label = tk.Label(
            main_frame,
            text="ISO 27001 Audit Manager",
            font=('Segoe UI', 20, 'bold'),
            bg='#FFFFFF',
            fg='#1f1f1f'
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Système de Gestion de la Sécurité de l'Information",
            font=('Segoe UI', 10),
            bg='#FFFFFF',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 30))
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=300)
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(
            main_frame,
            text="Initialisation de l'application...",
            font=('Segoe UI', 9),
            bg='#FFFFFF',
            fg='#888888'
        )
        self.status_label.pack(pady=(0, 20))
        
        self.progress.start(10)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
        
    def close(self):
        self.progress.stop()
        self.root.destroy()

def launch_streamlit(port):
    """Lance l'application Streamlit"""
    app_path = get_resource_path('app.py')
    
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        f"--server.port={port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--server.fileWatcherType=none"
    ]
    
    sys.exit(stcli.main())

def open_browser(url, splash):
    """Ouvre le navigateur en mode application"""
    splash.update_status("Démarrage du serveur...")
    time.sleep(3)
    
    max_retries = 30
    for i in range(max_retries):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=1)
            break
        except:
            splash.update_status(f"Connexion au serveur... ({i+1}/{max_retries})")
            time.sleep(1)
    
    splash.update_status("Ouverture de l'application...")
    time.sleep(0.5)
    
    chrome_path = None
    edge_path = None
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            edge_path = path
            break
    
    if chrome_path:
        os.system(f'"{chrome_path}" --app="{url}" --start-maximized')
    elif edge_path:
        os.system(f'"{edge_path}" --app="{url}" --start-maximized')
    else:
        webbrowser.open(url)
    
    splash.close()

def main():
    splash = SplashScreen()
    splash.update_status("Configuration de l'environnement...")
    splash.root.update()
    
    port = get_free_port()
    url = f"http://localhost:{port}"
    
    browser_thread = threading.Thread(target=open_browser, args=(url, splash))
    browser_thread.daemon = True
    browser_thread.start()
    
    launch_streamlit(port)

if __name__ == "__main__":
    main()
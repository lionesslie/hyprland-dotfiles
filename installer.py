#!/usr/bin/env python3
"""
hypr_dotfiles installer
Paketleri yükler ve config dosyalarını ~/.config altına kopyalar.
Kaynak: https://github.com/lionesslie/hypr_dotfiles
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

# ── Renkler ──────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def info(msg):    print(f"{CYAN}[*]{RESET} {msg}")
def ok(msg):      print(f"{GREEN}[✓]{RESET} {msg}")
def warn(msg):    print(f"{YELLOW}[!]{RESET} {msg}")
def error(msg):   print(f"{RED}[✗]{RESET} {msg}")
def header(msg):  print(f"\n{BOLD}{CYAN}{'─'*50}{RESET}\n{BOLD}  {msg}{RESET}\n{BOLD}{CYAN}{'─'*50}{RESET}")

# ── Paket listesi ─────────────────────────────────────────────────────────────
PACMAN_PACKAGES = [
    "hyprland",
    "hyprpaper",
    "awww",
    "waybar",
    "kitty",
    "rofi-wayland",
    "dolphin",
    "flameshot",
    "pipewire",
    "wireplumber",
    "pavucontrol",
    "fish",
    "ttf-jetbrains-mono-nerd",
    "papirus-icon-theme",
    "playerctl",
    "brightnessctl",
    "udisks2",
    "xdg-desktop-portal-hyprland",
    "nvim",
]

# ── Repo ──────────────────────────────────────────────────────────────────────
REPO_URL    = "https://github.com/lionesslie/hyprland-dotfiles"
DOTFILES_SUBDIR = ""   # config klasörleri direkt repo root'unda

# Config klasörleri: (repodaki_klasör → ~/.config/hedef_klasör)
CONFIG_MAP = {
    "hypr":   "hypr",
    "waybar": "waybar",
    "kitty":  "kitty",
    "rofi":   "rofi",
}

# ─────────────────────────────────────────────────────────────────────────────

def run(cmd, check=True, capture=False):
    """Kabuk komutu çalıştır."""
    return subprocess.run(
        cmd, shell=True, check=check,
        capture_output=capture, text=True
    )

def is_arch():
    return shutil.which("pacman") is not None

def install_packages():
    header("Paketler Yükleniyor")

    if not is_arch():
        error("Bu installer sadece Arch Linux (pacman) destekler.")
        sys.exit(1)

    # Zaten yüklü olanları tespit et
    already, missing = [], []
    for pkg in PACMAN_PACKAGES:
        result = run(f"pacman -Qi {pkg}", check=False, capture=True)
        if result.returncode == 0:
            already.append(pkg)
        else:
            missing.append(pkg)

    if already:
        ok(f"Zaten yüklü ({len(already)} paket): {', '.join(already)}")

    if not missing:
        ok("Tüm paketler zaten yüklü, atlanıyor.")
        return

    info(f"Yüklenecek {len(missing)} paket: {', '.join(missing)}")
    try:
        run(f"sudo pacman -S --needed --noconfirm {' '.join(missing)}")
        ok("Paketler başarıyla yüklendi.")
    except subprocess.CalledProcessError:
        error("Paket kurulumu başarısız. Lütfen internet bağlantını ve paket adlarını kontrol et.")
        sys.exit(1)

def clone_repo(tmpdir: str) -> str:
    """Repoyu geçici klasöre klonla, dotfiles yolunu döndür."""
    header("Repo İndiriliyor")
    dest = os.path.join(tmpdir, "hypr_dotfiles")
    info(f"Klonlanıyor: {REPO_URL}")
    try:
        run(f"git clone --depth=1 {REPO_URL} {dest}")
        ok("Repo başarıyla indirildi.")
    except subprocess.CalledProcessError:
        error("git clone başarısız. İnternet bağlantını kontrol et.")
        sys.exit(1)
    return os.path.join(dest, DOTFILES_SUBDIR) if DOTFILES_SUBDIR else dest

def copy_configs(dotfiles_path: str):
    header("Config Dosyaları Kopyalanıyor")
    config_home = Path.home() / ".config"
    config_home.mkdir(parents=True, exist_ok=True)

    for src_name, dst_name in CONFIG_MAP.items():
        src = Path(dotfiles_path) / src_name
        dst = config_home / dst_name

        if not src.exists():
            warn(f"Kaynak bulunamadı, atlandı: {src}")
            continue

        # Mevcut config'i yedekle
        if dst.exists():
            backup = Path(str(dst) + ".bak")
            warn(f"Mevcut '{dst_name}' klasörü yedekleniyor → {backup}")
            if backup.exists():
                shutil.rmtree(backup)
            shutil.copytree(dst, backup) if dst.is_dir() else shutil.copy2(dst, backup)

        # Kopyala
        if dst.exists():
            shutil.rmtree(dst) if dst.is_dir() else dst.unlink()

        shutil.copytree(src, dst)
        ok(f"~/.config/{dst_name}  ←  {src_name}/")

def fish_shell_prompt():
    """Fish'i varsayılan shell yapmayı teklif et."""
    header("Fish Shell")
    fish_path = shutil.which("fish")
    if not fish_path:
        warn("fish bulunamadı, atlanıyor.")
        return

    current_shell = os.environ.get("SHELL", "")
    if "fish" in current_shell:
        ok("Varsayılan shell zaten fish.")
        return

    print(f"  Mevcut shell: {current_shell}")
    answer = input(f"  Fish'i varsayılan shell yapmak ister misin? [{BOLD}e{RESET}/h]: ").strip().lower()
    if answer in ("e", "evet", "y", "yes", ""):
        try:
            run(f"chsh -s {fish_path}")
            ok(f"Varsayılan shell {fish_path} olarak ayarlandı.")
            info("Değişikliğin etkili olması için tekrar giriş yapman gerekir.")
        except subprocess.CalledProcessError:
            warn("chsh başarısız. Manuel olarak 'chsh -s $(which fish)' çalıştırabilirsin.")
    else:
        info("Fish shell değişikliği atlandı.")

def print_summary():
    header("Kurulum Tamamlandı")
    ok("Tüm paketler yüklendi.")
    ok("Config dosyaları ~/.config altına kopyalandı.")
    print(f"""
  {BOLD}Sonraki adımlar:{RESET}
  1. Hyprland'ı başlatmak için:   {CYAN}Hyprland{RESET}
  2. Duvar kağıdı için kendi fotoğrafını ayarla:
       {CYAN}~/.config/hypr/hyprpaper.conf{RESET}  (preload + wallpaper)
       {CYAN}~/.config/hypr/hyprland.conf{RESET}   (swww img satırı)
  3. Monitor adını güncelle (şu an HDMI-A-1):
       {CYAN}~/.config/hypr/hyprland.conf{RESET}  → monitor = ...
  4. nvibrant (NVIDIA renk aracı) istiyorsan:
       {CYAN}yay -S nvibrant{RESET}
""")

def main():
    print(f"""
{BOLD}{CYAN}
  ██╗  ██╗██╗   ██╗██████╗ ██████╗        
  ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗       
  ███████║ ╚████╔╝ ██████╔╝██████╔╝       
  ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══██╗       
  ██║  ██║   ██║   ██║     ██║  ██║       
  ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝  dotfiles installer
{RESET}""")

    if not is_arch():
        error("Arch Linux (pacman) gereklidir.")
        sys.exit(1)

    # Paket kurulumu
    install_packages()

    # Repo indir & config kopyala
    with tempfile.TemporaryDirectory() as tmpdir:
        dotfiles_path = clone_repo(tmpdir)
        copy_configs(dotfiles_path)
    # tmpdir burada silindi, ama config'ler ~/.config'e kopyalandı

    # Fish shell teklifi
    fish_shell_prompt()

    print_summary()

if __name__ == "__main__":
    main()

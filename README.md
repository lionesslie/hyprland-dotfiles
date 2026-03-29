<div align="center">

# 🌿 hyprland-dotfiles

**Hyprland** tabanlı minimal ve modern bir Arch Linux masaüstü kurulumu.

![Hyprland](https://img.shields.io/badge/WM-Hyprland-blue?style=for-the-badge&logo=linux)
![Arch](https://img.shields.io/badge/OS-Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📦 İçerik

| Klasör | Araç | Açıklama |
|--------|------|----------|
| `hypr/` | [Hyprland](https://hyprland.org) | Pencere yöneticisi + hyprpaper |
| `waybar/` | [Waybar](https://github.com/Alexays/Waybar) | Status bar |
| `kitty/` | [Kitty](https://sw.kovidgoyal.net/kitty/) | Terminal (Cosmic tema) |
| `rofi/` | [Rofi](https://github.com/lbonn/rofi) | Uygulama başlatıcı (Catppuccin tema) |

---

## ✨ Özellikler

- Rounded köşeler, blur ve animasyonlarla şık bir görünüm
- **Catppuccin** tabanlı rofi ve **Cosmic** temalı kitty
- Türkçe + Rusça klavye desteği (`Alt+Shift` ile geçiş)
- `swww` ile duvar kağıdı desteği
- Waybar'da saat, tarih, ses ve workspace göstergesi
- `JetBrainsMono Nerd Font` ile ikonlu arayüz
- Fish shell

---

## 🚀 Kurulum

### Gereksinimler

- Arch Linux
- `git` ve `python`

### Tek Komutla Kur

```bash
git clone https://github.com/lionesslie/hyprland-dotfiles
cd hyprland-dotfiles
python installer.py
```

`installer.py` otomatik olarak şunları yapar:

1. Gerekli tüm paketleri `pacman` ile yükler
2. Mevcut configlerini `.bak` uzantısıyla yedekler
3. Config dosyalarını `~/.config/` altına kopyalar
4. Fish'i varsayılan shell yapıp yapmamayı sorar

---

## 📋 Yüklenen Paketler

```
hyprland  hyprpaper  swww  waybar  kitty  rofi-wayland
dolphin  flameshot  pipewire  wireplumber  pavucontrol
fish  ttf-jetbrains-mono-nerd  papirus-icon-theme
playerctl  brightnessctl  udisks2  xdg-desktop-portal-hyprland
```

---

## ⚙️ Kurulum Sonrası

### Monitor ayarı
`~/.config/hypr/hyprland.conf` dosyasında monitor adını kendi sistemine göre güncelle:
```bash
# Mevcut monitörleri görmek için:
hyprctl monitors

# Ardından düzenle:
monitor = HDMI-A-1,1920x1080@180,0x0,1
#          ↑ burası senin monitor adın olmalı
```

### Duvar kağıdı
```bash
# ~/.config/hypr/hyprpaper.conf
preload = /home/KULLANICI/Resimler/wallpaper.jpg
wallpaper = HDMI-A-1,/home/KULLANICI/Resimler/wallpaper.jpg
```

### Klavye düzeni
Varsayılan olarak **Türkçe Q** ve **Rusça (fonetik)** yüklü gelir, `Alt+Shift` ile geçiş yapılır. Değiştirmek için `~/.config/hypr/hyprland.conf`:
```
kb_layout = tr, ru
kb_options = grp:alt_shift_toggle
```

---

## ⌨️ Kısayollar

| Kısayol | Eylem |
|---------|-------|
| `Super + Enter` | Terminal (kitty) |
| `Super + D` | Uygulama başlatıcı (rofi) |
| `Super + E` | Dosya yöneticisi (dolphin) |
| `Super + F` | Ekran görüntüsü (flameshot) |
| `Super + C` | Pencereyi kapat |
| `Super + V` | Pencereyi yüzdür |
| `Super + M` | Oturumu kapat |
| `Super + 1-9` | Workspace değiştir |
| `Super + Shift + 1-9` | Pencereyi workspace'e taşı |
| `Super + Sol/Sağ/Yukarı/Aşağı` | Odak değiştir |

---

## 📁 Dosya Yapısı

```
hyprland-dotfiles/
├── hypr/
│   ├── hyprland.conf
│   └── hyprpaper.conf
├── waybar/
│   ├── config
│   └── style.css
├── kitty/
│   └── kitty.conf
├── rofi/
│   ├── config.rasi
│   └── catppuccin.rasi
└── installer.py
```

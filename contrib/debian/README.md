
Debian
====================
This directory contains files used to package btc69d/btc69-qt
for Debian-based Linux systems. If you compile btc69d/btc69-qt yourself, there are some useful files here.

## btc69: URI support ##


btc69-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install btc69-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your btc69-qt binary to `/usr/bin`
and the `../../share/pixmaps/btc69128.png` to `/usr/share/pixmaps`

btc69-qt.protocol (KDE)


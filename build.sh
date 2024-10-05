pyinstaller --strip --noconfirm rpnc.py
DEST=~/.local/bin/rp
rm "$DEST"
ln -s $(pwd)/dist/rpnc/rpnc "$DEST"


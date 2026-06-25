#!/bin/sh

export DESKTOP_SESSION=plasma
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=KDE
export XDG_RUNTIME_DIR=/tmp/runtime-1999
export KDE_FULL_SESSION=true
export QT_QPA_PLATFORMTHEME=qt5ct
export BROWSER=/usr/bin/firefox

# Create desktop shortcuts
mkdir -p $HOME/Desktop
ln -sf /investigation-data $HOME/Desktop/investigation-data
ln -sf /scratch $HOME/Desktop/scratch
ln -sf /usr/share/applications/firefox-esr.desktop $HOME/Desktop/firefox-esr.desktop
ln -sf /usr/share/applications/org.kde.konsole.desktop $HOME/Desktop/org.kde.konsole.desktop

# Disable screen autolock
kwriteconfig5 --file kscreenlockerrc --group Daemon --key Autolock false
kwriteconfig5 --file kscreenlockerrc --group Daemon --key LockOnResume false

# Iniciar KDE Plasma
dbus-launch --exit-with-session bash -c "kwin_x11 --replace & startplasma-x11" &

# Eliminar Remote, Devices i Recent del Dolphin
FILE="$HOME/.local/share/user-places.xbel"
for i in $(seq 1 30); do
    if [ -f "$FILE" ]; then
        sed -i 's/<GroupState-Remote-IsHidden>false<\/GroupState-Remote-IsHidden>/<GroupState-Remote-IsHidden>true<\/GroupState-Remote-IsHidden>/' "$FILE"
        sed -i 's/<GroupState-Devices-IsHidden>false<\/GroupState-Devices-IsHidden>/<GroupState-Devices-IsHidden>true<\/GroupState-Devices-IsHidden>/' "$FILE"
        sed -i 's/<GroupState-RecentlySaved-IsHidden>false<\/GroupState-RecentlySaved-IsHidden>/<GroupState-RecentlySaved-IsHidden>true<\/GroupState-RecentlySaved-IsHidden>/' "$FILE"
        break
    fi
    sleep 1
done
killall dolphin 2>/dev/null

wait

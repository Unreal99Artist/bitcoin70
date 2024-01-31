 #!/usr/bin/env bash

 # Execute this file to install the btc69 cli tools into your path on OS X

 CURRENT_LOC="$( cd "$(dirname "$0")" ; pwd -P )"
 LOCATION=${CURRENT_LOC%Bitcoin69-Qt.app*}

 # Ensure that the directory to symlink to exists
 sudo mkdir -p /usr/local/bin

 # Create symlinks to the cli tools
 sudo ln -s ${LOCATION}/Bitcoin69-Qt.app/Contents/MacOS/btc69d /usr/local/bin/btc69d
 sudo ln -s ${LOCATION}/Bitcoin69-Qt.app/Contents/MacOS/btc69-cli /usr/local/bin/btc69-cli

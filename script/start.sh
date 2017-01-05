#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

DIR=$(dirname $(readlink -f "$0"))

TTY=$(tty)
TTY=${TTY:5}

if [ "$TTY" == "tty1" ]; then
  expect "$DIR/server.expect" "$DIR/../server/btk_server.py" "$DIR/../keyboard/kb_client.py"
  shutdown -h now
elif [ "$TTY" == "tty2" ]; then
  shutdown -h now
elif [ "$TTY" == "tty3" ]; then
  reboot
elif [ "$TTY" == "tty4" ]; then
  expect "$DIR/pair.expect"
  reboot
fi


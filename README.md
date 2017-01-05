# neo-bluetooth-keyboard

Simulates a bluetooth-keyboard on a linux computer to connect an external device (for example an iOS device). It changes the keycodes send to the device, which allows you to type with the [neo-layout](http://neo-layout.org/) on a device, that does not support the neo-layout.

## References

This project is based on an [article](http://yetanotherpointlesstechblog.blogspot.de/2016/04/emulating-bluetooth-keyboard-with.html) by keef using the provided [source](https://github.com/yaptb/BlogCode) and on an [article](https://www.gadgetdaily.xyz/emulate-a-bluetooth-keyboard-with-the-raspberry-pi) by Gavin Thomas.

## Installation

I tested this on a Raspberry Pi Zero with the RedBear IoT pHAT running Raspbian Jessie. It should also work on an Raspberry Pi 3 or any other Debian Jessie based computer with bluetooth support. The python code itself should also run on any other linux system, but the required packages may differ.

### 1. Update and install required packages

Start by upgrading your system:
```
sudo apt-get update
sudo apt-get upgrade
```

Then install the following packages:
```
sudo apt-get install python-gobject bluez bluez-tools bluez-firmware python-bluez python-dev python-pip python-dbus python-gtk2 git
sudo pip install evdev
```

### 2. Run the bluetooth daemon

You need to run the bluetooth daemon with the time plug-in only (as some plug-ins may interfer with the keyboard emulator). There are two possibilities to do this:

A: Edit `/etc/systemd/system/dbus-org.bluez.service` and replace the ExecStart by: `ExecStart=/usr/sbin/bluetoothd --nodetach --debug -p time`. Then restart the service. This method is persistant over reboot, but might cause problems if you try to do other things with your bluetooth adapter.

B: Stop the bluetooth deamon (`sudo systemctl stop bluetooth.service`) and start it manually (`sudo /usr/sbin/bluetoothd --nodetach --debug -p time`). This is not persistance over reboot. After starting the deamon you need a new (virtual) terminal to follow on.

### 3. Download the Code

Clone the repository to your device:
```
git clone https://github.com/jascosius/neo-bluetooth-keyboard.git
```
There are four subfolder:
* `dbus`: contains a DBUS system bus configuraton for the server
* `server`: contains the bluetooth keyboard emulator code
* `keyboard`: contains the client application to send local keystrokes to the emulator
* `script`: contains scripts to automate the setup after reboot

### 4. Configure DBUS

Copy the configuration file into the `/etc/dbus-1/system.d` folder:
```
cd neo-bluetooth-keyboard/dbus
sudo cp org.yaptb.btkkbservice.conf /etc/dbus-1/system.d
```

### 5. Configure the server

You first need the mac address of the bluetooth device. To get this run `sudo hciconfig hcio`. If the status is UP and RUNNING then all in well, otherwise run: `sudo hciconfig hcio up`

Change the value of the constant MY_ADDRESS in `server/btk_server.py` to the mac address of your bluetooth device.


### 6. Run the server
Now you can start the server by typing:
```
sudo python neo-bluetooth-keyboard/server/btk_server.py
```

Open an new (virtual) terminal to follow on.

### 7. Pairing a device

Run the `bluetoothctl` utility (`sudo bluetoothctl`) and type the following
```
discoverable on
pairable on
agent on
default-agent
```

Go to the bluetooth settings of your other device try to pair to `Neo-Bluetooth-Keyboard`. You should see a dialog with a passcode. Before pressing anything go back to the terminal on your keyboard device. You should see the same passcode there. Type yes and Enter and switch back to your other device. Now complete the pairing on this device as well.

### 8. Running the keyboard client

You need to run the keyboard client to mirror the keyboard inputs to your connected device.
```
sudo python neo-bluetooth-keyboard/keyboard/kb_client.py
```

If you press 'a' on the keyboard the script will send 'u' to your client. This i because the 'a' is 'u' in the neo2-layout. This allows you to type Neo2 on a device, that did not support the Neo2 layout (for example an iOS device). The script assumes the German Apple-Keyboard-Layout on the client (otherwise some special character do not work as expected).

## Setting up a Raspberry Pi (with bluetooth) to work as a Neo-Bluetooth-Keyboard

To make the work with the bluetooth keyboard easier i decided to configure the Raspberry Pi in a way, that everything runs after it started. This means I can start the Pi, connect the external device and I'm done. To achieve this, I did the following.

### Setting up the Raspberry Pi

Download, install and run [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian) (without graphical environment) on the Pi.

Now follow Step 1 to 5 from above. Use method A in step 2. Beside this you need the package `expect` (`sudo apt-get install expect`).

### Auto-login

After booting the Pi should auto-login the user pi. To achieve this edit `/lib/systemd/system/getty@.service` and replace the ExecStart by: `ExecStart=-/sbin/agetty --noclear -a pi %I $TERM`. 

### Change permissions

Set run permissions for the scripts:
```
cd neo-bluetooth-keyboard
chmod +x server/btk_server.py keyboard/kb_client.py script/*
```

### Start bluetooth on login

Execute the `start.sh` script on login. (For example append `sudo /home/pi/neo-bluetooth-keyboard/script/start.sh` to `/home/pi/.profile`).

### Use your Neo-Bluetooth-Keyboad

After booting your Pi the bluetooth server is waiting for a connection. You can connect (a already paired) device in the device bluetooth settings. After connecting the keyboard client is startet and you can just start typing.

To pair a new device change to tty4 (by pressing Ctrl+Alt+F4). Now go to your device, select `Neo-Bluetooth-Keyboard` and press pair. The device should now be paired. The Pi will reboot and you can connect your device as descibed above.

You can manually shutdown or reboot the Pi by pressing Ctrl+Alt+F2 (shutdown) or Ctrl+Alt+F3 (reboot).

### Optional settings

If you do not want to allow the user pi to become root without password edit `/etc/sudoers.d/010_pi-nopasswd` and replace the last `ALL` by the path to the `start.sh` script (for example `pi ALL=(ALL) NOPASSWD:/home/pi/neo-bluetooth-keyboard/script/start.sh`).
You should then change the owner of all scripts to root: `chown root:root -R neo-bluetooth-keyboard`.

To disable wifi network (and speed up boot time a little bit) disable dhcpcd and networking service:
```
sudo systemctl disable dhcpcd.service
sudo systemctl disable networking.service
```

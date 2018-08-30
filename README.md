# The Photobooth 

This is an application I created for a friend's wedding. The basic setup I had was a laptop connected to a DSLR camera via usb, within range of an internet connection. Once the application is running, the user approaches the screen laptop, clicks the "take snapshot" button, then poses for the photo. If satisfied with the photo, the user is prompted to enter their email address. Then the application will send the photo as an email attachment to that address immediately using the Gmail API. The DSLR camera is controlled via the gphoto2 library. The UI was created using PyQt5. I developed this application on Ubuntu 16.04 LTS with Python 3, and as such my instructions will assume you are using something similar.

## Prerequisites

First you need a DSLR that's compatible with the gphoto2 library. Second, you will need a USB connection of satisfactory length.
### Gphoto
You will need to install gphoto2 via the command line:
```
sudo apt install gphoto2 libgphoto2*
```
### PyQt
You'll also need to install PyQt5:
```
pip3 install pyqt5
```
### Gmail 
You will need to figure out how to get the Gmail API working. I'll add this too later.

<h1 align="center">
  <img src="https://github.com/kleidis/Troppical/blob/9683c790f5f0ad58e5cd7854f2474369061e4f0d/icons/logos/installer_logo.svg" alt="Placeholder" width="188"/>
</p>
<p align="center" style="font-size:144px;">
  <strong>Troppical</strong>
</h1>

<p align="center">
  <img src="https://img.shields.io/github/downloads/kleidis/Troppical/total" alt="GitHub all releases"/>
  <a href="https://github.com/kleidis/Troppical/releases/latest">
    <img src="https://img.shields.io/badge/Download-Latest_Release-2ea44f?logo=github&logoColor=white" alt="Download - Latest Release"/>
  </a>
  <br>
</p>

# What is this?

Troppical is a simple app that lets you manage your emulators with an easy installation and updating process.

**For now, we have these emulators**

- Sudachi (Y**u fork)
- Lime3DS
- Citra Enhanced
- PabloMK7's Citra fork
- Panda3DS
- Torzu (Soon)

If you'd like an emulator to be added, feel free to open a feature request issue. **Keep in mind that:**

- The emulator needs to not have a built-in way to update itself, there is no point in adding emulators that already have updaters
- The emulator needs to be distributed on GitHub

# Downloading
- Go to releases and download the latest release `troppical.exe` for Windows or `troppical.apk` for Android

# Usage

 To use this app, select the emulator you want to install and follow the setup options.
**You can have multiple emulators installed at the same time**

**NOTES for the Windows version:**

- **Windows Defender might detect this application as a trojan/malware. This is not true at all, you can look at the source code and determine that it is not a valid claim,  the app isn't that complex.**
**Please don't open an issue for this since there is nothing I can do apart from signing the app which I won't do**


- The app is a portable executable so feel free to run it from any directory you wish

- Although Troppical is portable that doesn't mean the emulators are. For now, there is no way to move an emulator directory once it is installed. If you do so, Troppical will just install updates on the directory that you initially chose to install the respective emulator on. The Uninstall button will error out and prompt you to reinstall as well

**REMEMBER:**
- Troppical is in the beta stages of development. Things may break so please report any bugs you encounter and I;ll try my best to fix them. Note that this is my first project and I'm a beginner so please be patient

# Screenshot
<img src="https://github.com/kleidis/Troppical/assets/167202775/4fefa8c3-a70d-4c91-9c7c-a8d59faf5753" width="500">

# Building for Windows

### Dependencies

- Python 3.12 (preferably not installed from the Microsoft Store)
- pyqt6
- pywin32
- requests
- pyinstaller (for compiling the app)

### Install dependencies:

`pip install pyqt6 pyinstaller pywin32 requests`

### Clone the repo:

`git clone https://github.com/kleidis/Troppical.git && cd Troppical`

### Generate image data using base64:

`python image-base64data-generator.py`

### Compile:

`pyinstaller --clean --onefile --icon=icon.ico --windowed troppical.py`


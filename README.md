<h1 align="center">
  <img src="https://raw.githubusercontent.com/kleidis/Troppical/refs/heads/master/icons/assets/Troppical.svg" alt="Troppical" width="188"/>
</p>
<p align="center" style="font-size:144px;">
  <strong>Troppical</strong>
</h1>

## About

Troppical is a simple Windows program that lets you manage your emulators with an easy installation and updating process.

> [!WARNING]
> Windows Defender might detect this application as a trojan/malware. This is not true at all, you can look at the source code and determine that it is not a valid claim,  the app isn't that complex.**
> Please don't open an issue for this since there is nothing I can do apart from signing the app which I won't do

## Usage

Download and open `Troppical.exe` :3 
   - **The app has an updater which should update and replace the exe with new versions**


```Although Troppical is portable that doesn't mean the emulators are. For now, there is no way to move an emulator directory once it is installed. If you do so, Troppical will just install updates on the directory that you initially chose to install the respective emulator on. The Uninstall button will error out and prompt you to reinstall as well```

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/2a8e078b-b432-4e9e-a729-657b73d2e48b" alt="Screenshot 1" width="300"/>
  <img src="https://github.com/user-attachments/assets/340b6412-8006-461c-8730-4bf6b86e6666" alt="Screenshot 2" width="300"/>
</p>


# Building for Windows

### Clone the repo

```
git clone https://github.com/kleidis/Troppical.git
```
### Install dependencies:

```
pip install  -r requirements.txt
```
### Compile:
```
pyinstaller Troppical.spec
```
## Contributors 

**We welcome anyone to contribute to this project as long as you know **some** Python and test your changes properly**

- For any ideas on what to do, you can ask over on discussions or check th milestones




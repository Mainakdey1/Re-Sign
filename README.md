# Image-Encryption-using-Cellular-Automata-Draft


This project is an attempt to encrypt data using a combination of rules including cellular automata, sbox and other chaotic systems. It is purely based on python and has been tested to work within very light system requirements. In addition to encryption it also features a storage system for containing the encrypted data, that is also encrypted.
The project offers three options: 
1. Plain Text encryption
2. Image encrption
3. Signature encryption

All of these methods have been tested and have shown very satisfactory entropy in the resulting encrypted data, making it very hard for attackers to decrypt said data without keys. And of keys, it offers two: A public key and a private key.
The application is available in the raw script format and also available as a standalone package as an executable application. In order to install and run the application(recommended), go to executable/Primary_executable/ and select lc_primary_executable.exe. Download the file by clicking on 'view raw file' option.

---
To run the script from your code editor(recommended for developers), ensure python is installed and updated to the latest version by running the following code:
```bash
python --version
```
You must also have pip installed on your system. Check if pip is installed and updated to the latest version by running the following code:
```bash
pip --version
```
You must install the following python packages on your system using pip:
```bash
pip install urllib3, imageio, numpy, opencv-python, pysimplegui, pyotp, qrcode, tensorflow, bcrypt, pyrebase, firebase-admin, requests, sockets
```

When setting up the code for the first time, you are required to acquire a developer key for your use from pysimplegui's website. After getting the key, paste it into the pysimplegui dialog box that appears when running the code for the first time.(This step is for setup-only, you will not be required to do this again.)

When prompted with the option to run AI based CNN model, you will be required to use an qr based authenticator application on your phone to access the database for the signatures.
Please use only .pxe or .txt files to store encryption keys. Please use only the provided decrypter to decrypt the .pxe files on your system.
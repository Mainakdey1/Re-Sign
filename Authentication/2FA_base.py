import pyotp
import qrcode


secret = pyotp.random_base32()
print(f"Secret Key: {secret}")


totp = pyotp.TOTP(secret)


qr_url = totp.provisioning_uri(name="Sirsimonjerkalot", issuer_name="ssenc")
qr = qrcode.make(qr_url)
qr.save("qrcode.png")
qr.show()
print("QR code saved as 'qrcode.png'. Scan this with your 2FA app.")


user_otp = input("Enter the OTP: ")
if totp.verify(user_otp):
    print("OTP is valid!")
else:
    print("Invalid OTP. Please try again.")

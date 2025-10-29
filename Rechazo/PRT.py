import qrcode

# Para crear un QR que abra un cliente de correo, usamos "mailto:"
email_link = "mailto:prtcoyhaique@denham.cl"

# Usamos la misma configuración que preferiste
qr = qrcode.QRCode(
    version=1,
    box_size=25,
    border=5
)

# Añadimos el enlace de correo
qr.add_data(email_link)
qr.make(fit=True)

# Creamos la imagen y la guardamos
imagen = qr.make_image(fill_color="black", back_color="white")
imagen.save("QR_Email_prtcoyhaique.png")

print("¡Se ha generado el QR para el email 'prtcoyhaique@denhan.cl' y se guardó como 'QR_Email_prtcoyhaique.png'!")

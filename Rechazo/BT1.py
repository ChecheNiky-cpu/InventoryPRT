import qrcode

link = "https://honeywhale.com.mx/tienda/scooters/x2/scooter-electrico-honey-whale-x2-negro/"

qr = qrcode.QRCode(
    version=1,
    box_size=25,
    border=5
)

qr.add_data(link)
qr.make(fit=True)

imagen = qr.make_image()
imagen.save("Scooter.png")

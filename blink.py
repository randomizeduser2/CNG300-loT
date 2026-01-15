import utime
from machine import Pin
from machine import UART
from utime import sleep

uart = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))

onboarding_led = Pin(25, Pin.OUT)

# Durum ışıkları
red = Pin(2, Pin.OUT)
green = Pin(4, Pin.OUT)

buzzer = Pin(10, Pin.OUT)
print("Program başlatıldı.")
onboarding_led.on()
while True:
    try:
        # Programın business logici burada gerçekleştirilecek.

        if uart.any(): # Veri geldiyse
            red.off()
            green.on()
            data = uart.read() # Gelen veriyi oku

            if data is not None:
                try:
                    message = data.decode("utf-8").strip()

                    if message == "on":
                        buzzer.on()
                        print("Mesaj alındı.")
                        uart.write("Led başarıyla açıldı\r\n")
                    elif message == "off":
                        buzzer.off()
                        print("Mesaj alındı.")
                        uart.write("Led başarıyla kapatıldı\r\n")


                except UnicodeDecodeError:
                    print("Hata: Veri işlenemedi.")

            utime.sleep(0.1)
        else :
            red.on()
            green.off()
    except KeyboardInterrupt:
        break
onboarding_led.off()

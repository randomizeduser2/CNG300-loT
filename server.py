from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import serial
from fastapi.middleware.cors import CORSMiddleware
import threading
import time

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")

# Seri Port Yapılandırması
PORT = "/dev/rfcomm0"
BAUD = 9600
ser = None

# Pico'dan gelen son mesajı tutmak için
last_pico_message = "Henüz veri yok"

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Bağlantı başarılı: {PORT}")
except Exception as e:
    print(f"Hata: Seri port açılamadı! {e}")

# Arka Planda Pico'yu Dinleme
def read_from_pico():
    global last_pico_message
    while True:
        if ser and ser.is_open:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    last_pico_message = line
                    print(f"Pico'dan Gelen: {line}")
        time.sleep(0.1)

# Dinleme işlemini ayrı bir thread'de başlat
thread = threading.Thread(target=read_from_pico, daemon=True)
thread.start()

# Endpointler

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pico-status")
async def get_status():
    return {"message": last_pico_message}

@app.post("/send/{command}")
async def send_command(command: str):
    if ser and ser.is_open:
        ser.write(command.encode('utf-8'))
        return {"status": "sent", "command": command}
    return {"status": "error", "message": "Serial not connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import os, time
from datetime import datetime

import psutil
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import wmi

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "System Monitoring Data"
WS_TIMESERIES = "TimeSeries"
WS_LASTONLY = "Last Only"

HEADERS = ["Timestamp","CPU%","RAM%","Disk%","Swap%","Temp CPU","Net Sent","Net Received","Process Count"]

def get_client():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return gspread.authorize(creds)

def get_cpu_temp():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        
        for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and "CPU" in sensor.Name:
                return sensor.Value
    except:
        return "Not Available"
    
    return "Not Available"
def collect_metrics(prev_net):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    swap = psutil.swap_memory().percent if hasattr(psutil, "swap_memory") else ""
    temp = get_cpu_temp()

    net = psutil.net_io_counters()
    sent = net.bytes_sent - prev_net.bytes_sent
    recv = net.bytes_recv - prev_net.bytes_recv

    proc_count = len(psutil.pids())

    row = [ts, cpu, ram, disk, swap, temp, sent, recv, proc_count]
    return row, net

def main(interval_seconds=10):
    client = get_client()
    sh = client.open(SHEET_NAME)
    ts_ws = sh.worksheet(WS_TIMESERIES)
    last_ws = sh.worksheet(WS_LASTONLY)

    last_ws.clear()
    last_ws.append_row(HEADERS)

    prev_net = psutil.net_io_counters()

    print("🚀 Monitoring started... Ctrl+C باش توقف")
    while True:
        row, prev_net = collect_metrics(prev_net)

        ts_ws.append_row(row)

        # update last only: header + last row
        last_ws.resize(rows=2, cols=len(HEADERS))
        last_ws.update("A2:I2", [row])

        print("✅ wrote:", row)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main(interval_seconds=10) 

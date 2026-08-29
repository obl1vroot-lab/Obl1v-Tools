"""Service Identifier - Identify services running on a host by scanning common ports."""

import customtkinter as ctk
import threading
import socket
import requests

SERVICE_MAP = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPCbind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    465: "SMTPS", 514: "Syslog", 554: "RTSP", 587: "Submission",
    631: "IPP", 636: "LDAPS", 993: "IMAPS", 995: "POP3S",
    1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle", 1723: "PPTP",
    2049: "NFS", 2181: "ZooKeeper", 3306: "MySQL", 3389: "RDP",
    4443: "HTTPS-Alt", 5432: "PostgreSQL", 5672: "RabbitMQ",
    5900: "VNC", 6379: "Redis", 6443: "Kubernetes", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt", 8888: "HTTP-Alt2", 9090: "Web-Console",
    9200: "Elasticsearch", 9418: "Git", 11211: "Memcached",
    27017: "MongoDB", 27018: "MongoDB", 50000: "SAP",
    50070: "HDFS", 61616: "ActiveMQ",
}

PRESETS = {
    "Common Web": [80, 443, 8080, 8443, 8888, 9090],
    "Database": [3306, 5432, 1433, 1521, 6379, 27017, 9200, 11211],
    "Remote Access": [22, 23, 3389, 5900, 5901],
    "Email": [25, 110, 143, 465, 587, 993, 995],
    "Infrastructure": [53, 111, 135, 139, 445, 2049, 5672, 61616],
    "All Common": sorted(SERVICE_MAP.keys()),
}


def create_ui(frame, COLORS, FONTS):
    host_entry = None
    port_entry = None
    output_text = None
    status_label = None
    progress_bar = None
    scan_btn = None
    is_scanning = False

    def set_scan_state(scanning):
        nonlocal is_scanning
        is_scanning = scanning
        if scanning:
            scan_btn.configure(state="disabled", text="Identifying...")
            status_label.configure(text="Scanning...", text_color=COLORS["yellow"])
        else:
            scan_btn.configure(state="normal", text="Identify")
            progress_bar.set(0)

    def _set_result(text, color=None):
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.configure(state="disabled")
        if color:
            status_label.configure(text="Done", text_color=color)

    def _append_text(text):
        output_text.configure(state="normal")
        output_text.insert("end", text)
        output_text.configure(state="disabled")
        output_text.see("end")

    def do_scan():
        host = host_entry.get().strip()
        if not host:
            _set_result("Please enter a target host.", COLORS["red"])
            return

        port_text = port_entry.get().strip()

        if port_text.lower() in ("all", "common"):
            ports = sorted(SERVICE_MAP.keys())
            port_desc = "All Common"
        elif port_text.lower() in ("web",):
            ports = PRESETS["Common Web"]
            port_desc = "Common Web"
        elif port_text.lower() in ("db", "database"):
            ports = PRESETS["Database"]
            port_desc = "Database"
        elif port_text.lower() in ("remote", "rdp", "ssh"):
            ports = PRESETS["Remote Access"]
            port_desc = "Remote Access"
        elif port_text.lower() in ("email", "mail"):
            ports = PRESETS["Email"]
            port_desc = "Email"
        elif port_text.lower() in ("infra", "infrastructure"):
            ports = PRESETS["Infrastructure"]
            port_desc = "Infrastructure"
        else:
            try:
                parts = port_text.split("-")
                if len(parts) == 2:
                    start_p = int(parts[0])
                    end_p = int(parts[1])
                    ports = list(range(start_p, end_p + 1))
                    port_desc = f"{start_p}-{end_p}"
                elif "," in port_text:
                    ports = [int(p.strip()) for p in port_text.split(",")]
                    port_desc = "Custom list"
                elif port_text:
                    ports = [int(port_text)]
                    port_desc = f"Port {port_text}"
                else:
                    ports = sorted(SERVICE_MAP.keys())
                    port_desc = "All Common"
            except ValueError:
                _set_result("Invalid port format. Use: number, range (1-1024), comma list, or preset name.", COLORS["red"])
                return

        set_scan_state(True)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Scanning {host} ({port_desc})...\n")
        output_text.configure(state="disabled")
        progress_bar.set(0)

        def worker():
            found = []
            total = len(ports)
            scanned = 0

            try:
                resolved = socket.gethostbyname(host)
                frame.after(0, lambda: _append_text(f"  Resolved: {resolved}\n\n"))
            except socket.gaierror:
                frame.after(0, lambda: _set_result(f"Could not resolve host: {host}", COLORS["red"]))
                frame.after(0, lambda: set_scan_state(False))
                return

            for port in ports:
                if not is_scanning:
                    break
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    result = s.connect_ex((resolved, port))
                    if result == 0:
                        service = SERVICE_MAP.get(port, "unknown")
                        banner = ""
                        try:
                            s.settimeout(1.0)
                            s.send(b"\r\n")
                            banner_data = s.recv(1024).decode("utf-8", errors="ignore").strip()
                            if banner_data:
                                banner = banner_data[:60]
                        except Exception:
                            pass
                        found.append((port, service, banner))
                        frame.after(0, lambda p=port, svc=service, b=banner:
                                    _append_text(f"  [OPEN]  {p:<6}  {svc:<20}  {b}\n"))
                    s.close()
                except Exception:
                    pass

                scanned += 1
                if scanned % 20 == 0 or scanned == total:
                    frame.after(0, lambda s=scanned, t=total: progress_bar.set(s / t))

            lines = [f"\n{'='*50}", f"IDENTIFICATION COMPLETE", f"{'='*50}",
                     f"  Host:   {host} ({resolved})",
                     f"  Scanned: {scanned} ports",
                     f"  Found:   {len(found)} open",
                     f"{'='*50}"]
            frame.after(0, lambda: _append_text("\n".join(lines)))
            color = COLORS["green"] if found else COLORS["text_dim"]
            frame.after(0, lambda: status_label.configure(
                text=f"Found {len(found)} open services", text_color=color))
            frame.after(0, lambda: set_scan_state(False))

        threading.Thread(target=worker, daemon=True).start()

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="Service Identifier", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Identify services on a host by scanning common ports.",
        font=FONTS["body"], text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 5))

    host_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Target host (IP or hostname)...",
        font=FONTS["mono"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    host_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    host_entry.bind("<Return>", lambda e: do_scan())

    port_frame = ctk.CTkFrame(frame, fg_color="transparent")
    port_frame.pack(fill="x", padx=15, pady=(0, 5))

    port_entry = ctk.CTkEntry(
        port_frame,
        placeholder_text="Ports (e.g. 80,8080 / 1-1024 / common,web,db,all)",
        font=FONTS["mono_small"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    port_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    scan_btn = ctk.CTkButton(
        port_frame,
        text="Identify",
        font=FONTS["button"],
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent"],
        text_color=COLORS["bg_dark"],
        command=do_scan,
    )
    scan_btn.pack(side="right")

    progress_bar = ctk.CTkProgressBar(
        frame, fg_color=COLORS["bg_card"], progress_color=COLORS["accent"]
    )
    progress_bar.pack(fill="x", padx=15, pady=(5, 5))
    progress_bar.set(0)

    status_label = ctk.CTkLabel(
        frame, text="", font=FONTS["body"], text_color=COLORS["text_dim"]
    )
    status_label.pack(anchor="w", padx=15, pady=(0, 5))

    output_text = ctk.CTkTextbox(
        frame,
        font=FONTS["mono"],
        fg_color=COLORS["bg_card"],
        border_color=COLORS["border"],
        border_width=1,
        text_color=COLORS["text"],
        state="disabled",
    )
    output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

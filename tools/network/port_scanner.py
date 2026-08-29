"""Port Scanner Tool - Scan target hosts for open ports."""

import customtkinter as ctk
import threading
import socket
import requests

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPCbind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle",
    2049: "NFS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt2", 9090: "Web-Console", 27017: "MongoDB",
}

TOP_100_PORTS = [
    7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106,
    110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427,
    443, 444, 445, 465, 513, 514, 515, 543, 544, 548, 554, 587,
    631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029,
    1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121,
    2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5001, 5003,
    5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800,
    5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081,
    8443, 8888, 9100, 9999, 10000, 32768, 32769, 32770, 49152,
    49153, 49154, 49155, 49156, 49157,
]

TOP_1000_PORTS = list(range(1, 1001))


def create_ui(frame, COLORS, FONTS):
    result_var = None
    host_entry = None
    start_port_entry = None
    end_port_entry = None
    output_text = None
    status_label = None
    progress_bar = None
    scan_btn = None
    is_scanning = False

    def set_scan_state(scanning):
        nonlocal is_scanning
        is_scanning = scanning
        if scanning:
            scan_btn.configure(state="disabled", text="Scanning...")
            status_label.configure(text="Scanning...", text_color=COLORS["yellow"])
        else:
            scan_btn.configure(state="normal", text="Scan")
            progress_bar.set(0)

    def do_scan():
        target = host_entry.get().strip()
        if not target:
            _set_result("Please enter a target host.", COLORS["red"])
            return

        start_text = start_port_entry.get().strip()
        end_text = end_port_entry.get().strip()

        if start_text.lower() == "top100":
            ports = TOP_100_PORTS
            port_desc = "Top 100"
        elif start_text.lower() == "top1000":
            ports = TOP_1000_PORTS
            port_desc = "Top 1000"
        else:
            try:
                start_port = int(start_text) if start_text else 1
                end_port = int(end_text) if end_text else 1024
            except ValueError:
                _set_result("Invalid port range.", COLORS["red"])
                return
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                _set_result("Port range must be 1-65535, start <= end.", COLORS["red"])
                return
            ports = list(range(start_port, end_port + 1))
            port_desc = f"{start_port}-{end_port}"

        set_scan_state(True)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Scanning {target} ({port_desc})...\n")
        output_text.configure(state="disabled")
        progress_bar.set(0)

        def worker():
            open_ports = []
            total = len(ports)
            scanned = 0

            try:
                resolved = socket.gethostbyname(target)
                frame.after(0, lambda: _append_text(f"  Resolved: {resolved}\n\n"))
            except socket.gaierror:
                frame.after(0, lambda: _set_result(f"Could not resolve {target}", COLORS["red"]))
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
                        service = COMMON_SERVICES.get(port, "unknown")
                        open_ports.append((port, service))
                        frame.after(0, lambda p=port, svc=service: _append_text(f"  [OPEN]  {p:<6}  {svc}\n"))
                    s.close()
                except Exception:
                    pass

                scanned += 1
                if scanned % 50 == 0 or scanned == total:
                    frame.after(0, lambda s=scanned, t=total: progress_bar.set(s / t))

            lines = [f"\n{'='*40}", f"SCAN COMPLETE", f"{'='*40}", f"  Target:   {target}", f"  Scanned:  {scanned} ports"]
            if open_ports:
                lines.append(f"  Open:     {len(open_ports)}")
            else:
                lines.append(f"  Open:     0")
            lines.append(f"{'='*40}")
            frame.after(0, lambda: _append_text("\n".join(lines)))
            color = COLORS["green"] if open_ports else COLORS["text_dim"]
            frame.after(0, lambda: status_label.configure(text=f"Found {len(open_ports)} open ports", text_color=color))
            frame.after(0, lambda: set_scan_state(False))

        threading.Thread(target=worker, daemon=True).start()

    def stop_scan():
        nonlocal is_scanning
        is_scanning = False

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

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="Port Scanner", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Scan target hosts for open ports and running services.",
        font=FONTS["body"],
        text_color=COLORS["text_dim"],
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

    start_port_entry = ctk.CTkEntry(
        port_frame,
        placeholder_text="Start (e.g. 1 or top100)",
        font=FONTS["mono_small"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
        width=160,
    )
    start_port_entry.pack(side="left", padx=(0, 10))

    end_port_entry = ctk.CTkEntry(
        port_frame,
        placeholder_text="End (e.g. 1024)",
        font=FONTS["mono_small"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
        width=160,
    )
    end_port_entry.pack(side="left", padx=(0, 10))

    scan_btn = ctk.CTkButton(
        port_frame,
        text="Scan",
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

"""Ping Tool - Test network connectivity and measure latency."""

import customtkinter as ctk
import threading
import socket
import subprocess
import platform


def create_ui(frame, COLORS, FONTS):
    input_entry = None
    output_text = None
    status_label = None
    ping_btn = None
    count_entry = None
    is_pinging = False

    def do_ping():
        target = input_entry.get().strip()
        if not target:
            _set_result("Please enter a hostname or IP address.", COLORS["red"])
            return

        count_str = count_entry.get().strip() or "4"
        try:
            count = int(count_str)
            if count < 1 or count > 100:
                count = 4
        except ValueError:
            count = 4

        is_pinging = True
        ping_btn.configure(state="disabled", text="Pinging...")
        status_label.configure(text="Pinging...", text_color=COLORS["yellow"])
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Pinging {target}...\n")
        output_text.configure(state="disabled")

        def worker():
            try:
                resolved_ip = socket.gethostbyname(target)
            except socket.gaierror:
                frame.after(0, lambda: _set_result(f"Could not resolve hostname: {target}", COLORS["red"]))
                frame.after(0, lambda: _set_ui_state(False))
                return

            param = "-n" if platform.system().lower() == "windows" else "-c"
            cmd = ["ping", param, str(count), target]

            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=count * 5 + 10,
                )
                output = proc.stdout

                lines = [
                    f"{'='*44}",
                    "PING RESULTS",
                    f"{'='*44}",
                    f"  Host:       {target}",
                    f"  IP:         {resolved_ip}",
                    "",
                ]

                loss = "0%"
                min_lat = avg_lat = max_lat = "N/A"

                if platform.system().lower() == "windows":
                    for line in output.splitlines():
                        line_s = line.strip()
                        if line_s.startswith("Packets:") or line_s.startswith(" Pakete"):
                            lines.append(f"  {line_s}")
                            parts = line_s.split(",")
                            for part in parts:
                                part = part.strip()
                                if "%" in part and "Verloren" in part or "lost" in part.lower():
                                    for token in part.split():
                                        if "%" in token:
                                            loss = token
                        if "Minimum" in line_s or "Minimum" in line_s:
                            lines.append(f"  {line_s}")
                            parts = line_s.split("=")
                            if len(parts) > 1:
                                vals = parts[1].strip().split("/") if "/" in parts[1] else []
                                if len(vals) >= 3:
                                    min_lat, avg_lat, max_lat = vals[0].strip(), vals[1].strip(), vals[2].strip()
                else:
                    for line in output.splitlines():
                        line_s = line.strip()
                        if "packets transmitted" in line_s or "received" in line_s:
                            lines.append(f"  {line_s}")
                            parts = line_s.split(",")
                            for part in parts:
                                part = part.strip()
                                if "%" in part:
                                    loss = part.split()[0]
                        if "rtt" in line_s or "round-trip" in line_s:
                            lines.append(f"  {line_s}")
                            parts = line_s.split("=")
                            if len(parts) > 1:
                                vals = parts[1].strip().split("/")
                                if len(vals) >= 3:
                                    min_lat, avg_lat, max_lat = vals[0], vals[1], vals[2]

                lines.extend([
                    "",
                    f"  Packet Loss: {loss}",
                    f"  Min Latency: {min_lat} ms",
                    f"  Avg Latency: {avg_lat} ms",
                    f"  Max Latency: {max_lat} ms",
                    "",
                    f"{'='*44}",
                ])

                if "timed out" in output.lower() or "timeout" in output.lower():
                    color = COLORS["yellow"]
                elif loss == "100%" or loss == "100.0%":
                    color = COLORS["red"]
                else:
                    color = COLORS["green"]

                frame.after(0, lambda: _set_result("\n".join(lines), color))

            except subprocess.TimeoutExpired:
                frame.after(0, lambda: _set_result("Ping timed out.", COLORS["red"]))
            except Exception as e:
                frame.after(0, lambda: _set_result(f"Error: {e}", COLORS["red"]))
            finally:
                frame.after(0, lambda: _set_ui_state(False))

        threading.Thread(target=worker, daemon=True).start()

    def _set_result(text, color=None):
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.configure(state="disabled")
        if color:
            status_label.configure(text="Done", text_color=color)

    def _set_ui_state(scanning):
        nonlocal is_pinging
        is_pinging = scanning
        if scanning:
            ping_btn.configure(state="disabled", text="Pinging...")
        else:
            ping_btn.configure(state="normal", text="Ping")

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="Ping Tool", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Test network connectivity and measure latency.",
        font=FONTS["body"],
        text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 10))

    input_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Hostname or IP address...",
        font=FONTS["mono"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    input_entry.bind("<Return>", lambda e: do_ping())

    count_label = ctk.CTkLabel(
        input_frame, text="Count:", font=FONTS["body"], text_color=COLORS["text_dim"]
    )
    count_label.pack(side="left", padx=(0, 5))

    count_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="4",
        font=FONTS["mono_small"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
        width=60,
    )
    count_entry.pack(side="left", padx=(0, 10))

    ping_btn = ctk.CTkButton(
        input_frame,
        text="Ping",
        font=FONTS["button"],
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent"],
        text_color=COLORS["bg_dark"],
        command=do_ping,
    )
    ping_btn.pack(side="right")

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

"""IP Lookup Tool - Resolve IP addresses and hostnames to geolocation information."""

import customtkinter as ctk
import threading
import socket
import requests


def create_ui(frame, COLORS, FONTS):
    result_var = None
    input_entry = None
    output_text = None
    status_label = None

    def do_lookup():
        target = input_entry.get().strip()
        if not target:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Please enter an IP address or hostname.")
            output_text.configure(state="disabled")
            return

        status_label.configure(text="Looking up...", text_color=COLORS["yellow"])
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "Querying ip-api.com...")
        output_text.configure(state="disabled")

        def worker():
            try:
                resolved_ip = target
                try:
                    socket.inet_aton(target)
                except socket.error:
                    resolved_ip = socket.gethostbyname(target)

                resp = requests.get(f"http://ip-api.com/json/{resolved_ip}", timeout=10)
                data = resp.json()

                if data.get("status") == "success":
                    fields = [
                        ("IP", data.get("query", "")),
                        ("Country", data.get("country", "")),
                        ("Region", data.get("regionName", "")),
                        ("City", data.get("city", "")),
                        ("ISP", data.get("isp", "")),
                        ("Org", data.get("org", "")),
                        ("Latitude", str(data.get("lat", ""))),
                        ("Longitude", str(data.get("lon", ""))),
                        ("Timezone", data.get("timezone", "")),
                    ]
                    lines = [f"{'='*40}", "IP LOOKUP RESULTS", f"{'='*40}", ""]
                    for label, value in fields:
                        lines.append(f"  {label:<14} {value}")
                    lines.append("")
                    lines.append(f"{'='*40}")
                    frame.after(0, lambda: _set_result("\n".join(lines), COLORS["green"]))
                else:
                    msg = data.get("message", "Unknown error")
                    frame.after(0, lambda: _set_result(f"Error: {msg}", COLORS["red"]))

            except socket.gaierror:
                frame.after(0, lambda: _set_result("Error: Could not resolve hostname.", COLORS["red"]))
            except requests.RequestException as e:
                frame.after(0, lambda: _set_result(f"Network error: {e}", COLORS["red"]))
            except Exception as e:
                frame.after(0, lambda: _set_result(f"Error: {e}", COLORS["red"]))

        threading.Thread(target=worker, daemon=True).start()

    def _set_result(text, color=None):
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.configure(state="disabled")
        if color:
            status_label.configure(text="Done", text_color=color)

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="IP Lookup", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Resolve IP addresses and hostnames to geolocation data.",
        font=FONTS["body"],
        text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 10))

    input_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="IP address or hostname...",
        font=FONTS["mono"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    input_entry.bind("<Return>", lambda e: do_lookup())

    lookup_btn = ctk.CTkButton(
        input_frame,
        text="Lookup",
        font=FONTS["button"],
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent"],
        text_color=COLORS["bg_dark"],
        command=do_lookup,
    )
    lookup_btn.pack(side="right")

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

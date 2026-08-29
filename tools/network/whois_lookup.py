"""WHOIS Lookup Tool - Retrieve domain registration information."""

import customtkinter as ctk
import threading
import socket
import requests

try:
    import whois as python_whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False


def create_ui(frame, COLORS, FONTS):
    input_entry = None
    output_text = None
    status_label = None

    def do_lookup():
        target = input_entry.get().strip()
        if not target:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Please enter a domain name.")
            output_text.configure(state="disabled")
            return

        if not HAS_WHOIS:
            _set_result("Error: python-whois is not installed.\nRun: pip install python-whois", COLORS["red"])
            return

        status_label.configure(text="Querying WHOIS...", text_color=COLORS["yellow"])
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Looking up WHOIS data for {target}...")
        output_text.configure(state="disabled")

        def worker():
            try:
                w = python_whois.whois(target)

                def _format_list(val):
                    if isinstance(val, list):
                        return "\n".join(f"    {v}" for v in val)
                    return f"    {val}" if val else "    N/A"

                def _format_date(val):
                    if isinstance(val, list):
                        return ", ".join(str(v) for v in val)
                    return str(val) if val else "N/A"

                domain_name = w.domain_name if isinstance(w.domain_name, str) else (
                    w.domain_name[0] if w.domain_name else target
                )

                lines = [
                    f"{'='*44}",
                    "WHOIS LOOKUP RESULTS",
                    f"{'='*44}",
                    "",
                    f"  Domain Name:  {domain_name}",
                    "",
                    f"  Registrar:    {w.registrar or 'N/A'}",
                    "",
                    f"  Creation:     {_format_date(w.creation_date)}",
                    f"  Expiry:       {_format_date(w.expiration_date)}",
                    f"  Updated:      {_format_date(w.updated_date)}",
                    "",
                ]

                if w.name_servers:
                    ns = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers]
                    lines.append("  Name Servers:")
                    for ns_entry in ns:
                        lines.append(f"    {ns_entry}")
                else:
                    lines.append("  Name Servers: N/A")

                lines.append("")

                if w.status:
                    statuses = w.status if isinstance(w.status, list) else [w.status]
                    lines.append("  Status:")
                    for s in statuses:
                        lines.append(f"    {s}")
                else:
                    lines.append("  Status: N/A")

                lines.extend(["", f"{'='*44}"])
                frame.after(0, lambda: _set_result("\n".join(lines), COLORS["green"]))

            except python_whois.WhoidNotFoundError:
                frame.after(0, lambda: _set_result(f"No WHOIS data found for {target}.", COLORS["yellow"]))
            except Exception as e:
                frame.after(0, lambda: _set_result(f"WHOIS error: {e}", COLORS["red"]))

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
        frame, text="WHOIS Lookup", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Retrieve domain registration and ownership information.",
        font=FONTS["body"],
        text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 10))

    input_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Domain name (e.g. example.com)...",
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

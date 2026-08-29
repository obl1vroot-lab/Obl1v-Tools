"""DNS Lookup Tool - Query DNS records for domain names."""

import customtkinter as ctk
import threading
import socket
import requests

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False


def create_ui(frame, COLORS, FONTS):
    result_var = None
    input_entry = None
    output_text = None
    status_label = None
    record_type_var = None

    RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

    def do_lookup():
        target = input_entry.get().strip()
        if not target:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Please enter a domain name.")
            output_text.configure(state="disabled")
            return

        if not HAS_DNS:
            _set_result("Error: dnspython is not installed.\nRun: pip install dnspython", COLORS["red"])
            return

        record_type = record_type_var.get()
        status_label.configure(text="Querying DNS...", text_color=COLORS["yellow"])
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Looking up {record_type} records for {target}...")
        output_text.configure(state="disabled")

        def worker():
            try:
                answers = dns.resolver.resolve(target, record_type)
                lines = [
                    f"{'='*40}",
                    f"DNS LOOKUP RESULTS",
                    f"{'='*40}",
                    f"  Domain:     {target}",
                    f"  Record:     {record_type}",
                    f"  TTL:        {answers.rrset.ttl}s",
                    "",
                ]

                for rdata in answers:
                    if record_type == "MX":
                        lines.append(f"  Priority {rdata.preference:>4}  {rdata.exchange}")
                    elif record_type == "SOA":
                        lines.append(f"  Primary NS:  {rdata.mname}")
                        lines.append(f"  Admin:       {rdata.rname}")
                        lines.append(f"  Serial:      {rdata.serial}")
                        lines.append(f"  Refresh:     {rdata.refresh}s")
                        lines.append(f"  Retry:       {rdata.retry}s")
                        lines.append(f"  Expire:      {rdata.expire}s")
                        lines.append(f"  Min TTL:     {rdata.minimum}s")
                    elif record_type == "TXT":
                        lines.append(f"  \"{rdata.to_text()}\"")
                    else:
                        lines.append(f"  {rdata.to_text()}")

                lines.append("")
                lines.append(f"{'='*40}")
                frame.after(0, lambda: _set_result("\n".join(lines), COLORS["green"]))

            except dns.resolver.NoAnswer:
                frame.after(0, lambda: _set_result(f"No {record_type} records found for {target}.", COLORS["yellow"]))
            except dns.resolver.NXDOMAIN:
                frame.after(0, lambda: _set_result(f"Domain {target} does not exist.", COLORS["red"]))
            except dns.exception.DNSException as e:
                frame.after(0, lambda: _set_result(f"DNS error: {e}", COLORS["red"]))
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
        frame, text="DNS Lookup", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Query DNS records for any domain name.",
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

    record_type_var = ctk.StringVar(value="A")
    type_menu = ctk.CTkOptionMenu(
        input_frame,
        variable=record_type_var,
        values=RECORD_TYPES,
        font=FONTS["body"],
        fg_color=COLORS["bg_card"],
        button_color=COLORS["accent"],
        button_hover_color=COLORS["accent"],
        dropdown_fg_color=COLORS["bg_card"],
        dropdown_hover_color=COLORS["border"],
        text_color=COLORS["text"],
        width=100,
    )
    type_menu.pack(side="left", padx=(0, 10))

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

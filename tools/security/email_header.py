"""Email Header Analyzer - Parse and analyze email headers for security insights."""

import customtkinter as ctk
import re
import email.utils
from datetime import datetime


def _parse_received_chain(header_text):
    received_lines = []
    for line in header_text.splitlines():
        if line.lower().startswith("received:"):
            received_lines.append(line.strip())
    return received_lines


def _check_spf(header_text):
    for line in header_text.splitlines():
        lower = line.lower().strip()
        if lower.startswith("authentication-results:") or lower.startswith("received-spf:"):
            if "fail" in lower or "softfail" in lower or "neutral" in lower:
                return "FAIL" if "fail" in lower and "soft" not in lower else "SOFTFAIL/NEUTRAL"
            if "pass" in lower:
                return "PASS"
    return "NOT FOUND"


def _check_dkim(header_text):
    for line in header_text.splitlines():
        lower = line.lower().strip()
        if lower.startswith("authentication-results:") or lower.startswith("dkim-signature:"):
            if "dkim=" in lower:
                if "pass" in lower:
                    return "PASS"
                if "fail" in lower or "none" in lower:
                    return "FAIL"
    return "NOT FOUND"


def _extract_field(header_text, field_name):
    pattern = re.compile(rf"^{re.escape(field_name)}:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(header_text)
    if match:
        value = match.group(1).strip()
        if field_name.lower() == "from" and "<" in value:
            return value
        return value
    return None


def _extract_domains(text):
    if not text:
        return []
    return re.findall(r"[\w.-]+\.[a-z]{2,}", text)


def analyze_header(header_text):
    results = {}

    from_addr = _extract_field(header_text, "From")
    to_addr = _extract_field(header_text, "To")
    subject = _extract_field(header_text, "Subject")
    date = _extract_field(header_text, "Date")
    message_id = _extract_field(header_text, "Message-ID")
    reply_to = _extract_field(header_text, "Reply-To")
    return_path = _extract_field(header_text, "Return-Path")

    results["From"] = from_addr or "Not found"
    results["To"] = to_addr or "Not found"
    results["Subject"] = subject or "Not found"
    results["Date"] = date or "Not found"
    results["Message-ID"] = message_id or "Not found"
    results["Reply-To"] = reply_to or "Not found"
    results["Return-Path"] = return_path or "Not found"

    results["SPF"] = _check_spf(header_text)
    results["DKIM"] = _check_dkim(header_text)

    received_chain = _parse_received_chain(header_text)
    results["Received chain"] = received_chain

    from_domains = _extract_domains(from_addr or "")
    reply_domains = _extract_domains(reply_to or "")
    return_domains = _extract_domains(return_path or "")

    results["From domains"] = from_domains
    results["Reply-To domains"] = reply_domains
    results["Return-Path domains"] = return_domains

    suspicious = []
    if results["SPF"] in ("FAIL", "SOFTFAIL/NEUTRAL"):
        suspicious.append(f"SPF check: {results['SPF']}")
    if results["DKIM"] in ("FAIL",):
        suspicious.append(f"DKIM check: {results['DKIM']}")
    if reply_to and reply_to != from_addr:
        reply_d = set(reply_domains)
        from_d = set(from_domains)
        if not reply_d.intersection(from_d):
            suspicious.append("Reply-To domain differs from From domain")
    if return_path and return_path != from_addr:
        return_d = set(return_domains)
        from_d = set(from_domains)
        if not return_d.intersection(from_d):
            suspicious.append("Return-Path domain differs from From domain")
    if message_id and from_domains:
        mid_domains = re.findall(r"@([\w.-]+)", message_id)
        if mid_domains:
            mid_d = set(mid_domains)
            from_d = set(from_domains)
            if not mid_d.intersection(from_d):
                suspicious.append("Message-ID domain differs from From domain")

    results["Suspicious"] = suspicious
    return results


def create_ui(frame, COLORS, FONTS):
    header_input = None
    output_text = None
    status_label = None
    analyze_btn = None

    def do_analyze():
        raw = header_input.get("1.0", "end").strip()
        if not raw:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Please paste an email header to analyze.")
            output_text.configure(state="disabled")
            status_label.configure(text="No input", text_color=COLORS["red"])
            return

        analyze_btn.configure(state="disabled", text="Analyzing...")
        status_label.configure(text="Analyzing...", text_color=COLORS["yellow"])

        def worker():
            try:
                results = analyze_header(raw)
                lines = []
                lines.append("=" * 50)
                lines.append("  EMAIL HEADER ANALYSIS")
                lines.append("=" * 50)
                lines.append("")

                lines.append("--- Basic Info ---")
                for key in ["From", "To", "Subject", "Date", "Message-ID", "Reply-To", "Return-Path"]:
                    lines.append(f"  {key:<14}: {results[key]}")
                lines.append("")

                lines.append("--- Authentication ---")
                lines.append(f"  SPF:  {results['SPF']}")
                lines.append(f"  DKIM: {results['DKIM']}")
                lines.append("")

                lines.append(f"--- Received Chain ({len(results['Received chain'])} hops) ---")
                for i, hop in enumerate(results["Received chain"], 1):
                    lines.append(f"  Hop {i}: {hop}")
                lines.append("")

                if results["Suspicious"]:
                    lines.append("--- Suspicious Indicators ---")
                    for item in results["Suspicious"]:
                        lines.append(f"  [!] {item}")
                    lines.append("")

                lines.append("=" * 50)

                frame.after(0, lambda: _display_result("\n".join(lines), results["Suspicious"]))
            except Exception as e:
                frame.after(0, lambda: _display_result(f"Error parsing header:\n{e}", []))

        threading.Thread(target=worker, daemon=True).start()

    def _display_result(text, suspicious):
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.configure(state="disabled")

        analyze_btn.configure(state="normal", text="Analyze")
        if suspicious:
            status_label.configure(text=f"{len(suspicious)} suspicious indicator(s) found", text_color=COLORS["red"])
        else:
            status_label.configure(text="No suspicious indicators found", text_color=COLORS["green"])

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="Email Header Analyzer", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Paste an email header to analyze SPF, DKIM, routing, and suspicious indicators.",
        font=FONTS["body"], text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    header_input = ctk.CTkTextbox(
        frame,
        font=FONTS["mono_small"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        border_width=1,
        text_color=COLORS["text"],
        height=160,
    )
    header_input.pack(fill="x", padx=15, pady=(0, 5))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=15, pady=(0, 5))

    analyze_btn = ctk.CTkButton(
        btn_frame,
        text="Analyze",
        font=FONTS["button"],
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent"],
        text_color=COLORS["bg_dark"],
        command=do_analyze,
    )
    analyze_btn.pack(side="right")

    status_label = ctk.CTkLabel(
        btn_frame, text="", font=FONTS["body"], text_color=COLORS["text_dim"]
    )
    status_label.pack(side="left")

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

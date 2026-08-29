"""URL Scanner - Analyze URLs for HTTP/HTTPS info, SSL, redirects, and security headers."""

import customtkinter as ctk
import threading
import socket
import requests
import ssl
import json


def create_ui(frame, COLORS, FONTS):
    url_entry = None
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

    def _ssl_check(hostname, port=443):
        info = {"issuer": "N/A", "subject": "N/A", "version": "N/A", "serial": "N/A", "valid_from": "N/A", "valid_to": "N/A", "error": None}
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.settimeout(5)
                s.connect((hostname, port))
                cert = s.getpeercert()
                info["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                info["subject"] = dict(x[0] for x in cert.get("subject", []))
                info["version"] = cert.get("version", "N/A")
                info["serial"] = cert.get("serialNumber", "N/A")
                info["valid_from"] = cert.get("notBefore", "N/A")
                info["valid_to"] = cert.get("notAfter", "N/A")
        except Exception as e:
            info["error"] = str(e)
        return info

    def _check_security_headers(headers):
        findings = []
        security_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Content-Type-Options": "X-Content-Type-Options",
            "X-Frame-Options": "X-Frame-Options",
            "X-XSS-Protection": "X-XSS-Protection",
            "Referrer-Policy": "Referrer-Policy",
            "Permissions-Policy": "Permissions-Policy",
        }
        for header, name in security_headers.items():
            if header in headers:
                findings.append(f"  [+] {name}: {headers[header]}")
            else:
                findings.append(f"  [-] {name}: MISSING")
        return findings

    def do_scan():
        url = url_entry.get().strip()
        if not url:
            _set_result("Please enter a URL to scan.", COLORS["red"])
            return

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        set_scan_state(True)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Scanning {url}...\n")
        output_text.configure(state="disabled")
        progress_bar.set(0)

        def worker():
            try:
                parsed = requests.utils.urlparse(url)
                hostname = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == "https" else 80)

                frame.after(0, lambda: progress_bar.set(0.2))
                frame.after(0, lambda: _append_text("  Checking SSL/TLS...\n"))
                ssl_info = _ssl_check(hostname, port) if parsed.scheme == "https" else None

                frame.after(0, lambda: progress_bar.set(0.4))
                frame.after(0, lambda: _append_text("  Sending HTTP request...\n"))

                session = requests.Session()
                session.max_redirects = 10

                try:
                    resp = session.get(
                        url,
                        timeout=15,
                        allow_redirects=True,
                        headers={"User-Agent": "Mozilla/5.0 (compatible; Obl1v-Tools/1.0)"},
                    )
                except requests.exceptions.SSLError:
                    resp = session.get(url, timeout=15, allow_redirects=False, verify=False,
                                       headers={"User-Agent": "Mozilla/5.0 (compatible; Obl1v-Tools/1.0)"})

                frame.after(0, lambda: progress_bar.set(0.7))
                frame.after(0, lambda: _append_text("  Analyzing response...\n"))

                lines = []
                lines.append("=" * 50)
                lines.append("  URL SCAN RESULTS")
                lines.append("=" * 50)
                lines.append("")
                lines.append("--- Request ---")
                lines.append(f"  Original URL:    {url}")
                lines.append(f"  Final URL:       {resp.url}")
                lines.append(f"  Status Code:     {resp.status_code} {resp.reason}")
                lines.append(f"  HTTP Version:    {resp.raw.version}")
                lines.append(f"  Content-Type:    {resp.headers.get('Content-Type', 'N/A')}")
                lines.append(f"  Content-Length:  {resp.headers.get('Content-Length', 'N/A')}")

                redirect_count = len(resp.history)
                lines.append(f"  Redirects:       {redirect_count}")
                if resp.history:
                    for i, r in enumerate(resp.history, 1):
                        lines.append(f"    {i}. {r.status_code} -> {r.url}")

                lines.append("")

                lines.append("--- SSL/TLS Certificate ---")
                if ssl_info and not ssl_info["error"]:
                    issuer = ssl_info["issuer"]
                    subject = ssl_info["subject"]
                    lines.append(f"  Issuer (CN):  {issuer.get('commonName', 'N/A')}")
                    lines.append(f"  Subject (CN): {subject.get('commonName', 'N/A')}")
                    lines.append(f"  Valid From:   {ssl_info['valid_from']}")
                    lines.append(f"  Valid To:     {ssl_info['valid_to']}")
                    lines.append(f"  Serial:       {ssl_info['serial']}")
                elif ssl_info and ssl_info["error"]:
                    lines.append(f"  Error: {ssl_info['error']}")
                else:
                    lines.append("  Not HTTPS - no SSL certificate")
                lines.append("")

                lines.append("--- Security Headers ---")
                sec_headers = _check_security_headers(dict(resp.headers))
                lines.extend(sec_headers)
                lines.append("")

                lines.append("--- Response Headers ---")
                for key, value in sorted(resp.headers.items()):
                    lines.append(f"  {key}: {value}")
                lines.append("")
                lines.append("=" * 50)

                frame.after(0, lambda: _set_result("\n".join(lines), COLORS["green"]))
            except requests.exceptions.ConnectionError as e:
                frame.after(0, lambda: _set_result(f"Connection error:\n{e}", COLORS["red"]))
            except requests.exceptions.Timeout:
                frame.after(0, lambda: _set_result("Request timed out after 15 seconds.", COLORS["red"]))
            except Exception as e:
                frame.after(0, lambda: _set_result(f"Error: {e}", COLORS["red"]))
            finally:
                frame.after(0, lambda: set_scan_state(False))

        threading.Thread(target=worker, daemon=True).start()

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="URL Scanner", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Analyze URLs for HTTP info, SSL certificates, redirects, and security headers.",
        font=FONTS["body"], text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 5))

    url_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="URL to scan (e.g. https://example.com)...",
        font=FONTS["mono"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    url_entry.bind("<Return>", lambda e: do_scan())

    scan_btn = ctk.CTkButton(
        input_frame,
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

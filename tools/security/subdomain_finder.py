"""Subdomain Finder Tool - Discover subdomains of a target domain via DNS resolution."""

import customtkinter as ctk
import threading
import socket
import requests

try:
    import dns.resolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False

WORDLIST = [
    "www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "blog",
    "shop", "store", "portal", "vpn", "webmail", "mx", "smtp", "pop", "imap",
    "ns1", "ns2", "dns", "cdn", "static", "media", "assets", "img", "images",
    "video", "download", "uploads", "backup", "bak", "old", "new", "demo",
    "beta", "alpha", "preview", "sandbox", "ci", "jenkins", "git", "gitlab",
    "svn", "hg", "repo", "jira", "confluence", "wiki", "docs", "help",
    "support", "status", "monitor", "grafana", "kibana", "elastic", "db",
    "database", "mysql", "postgres", "redis", "mongo", "es", "cache",
    "proxy", "gateway", "lb", "haproxy", "nginx", "apache", "tomcat",
    "app", "backend", "frontend", "web", "mobile", "m", "api-v2", "api-v3",
    "graphql", "rest", "ws", "socket", "realtime", "rt", "ws2", "events",
    "auth", "login", "sso", "oauth", "ldap", "okta", "cloud", "aws", "gcp",
    "azure", "s3", "minio", "k8s", "kube", "docker", "registry", "harbor",
    "vault", "consul", "etcd", "zk", "kafka", "rabbit", "mq", "queue",
]


def create_ui(frame, COLORS, FONTS):
    domain_entry = None
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

    def do_scan():
        domain = domain_entry.get().strip().lower()
        if not domain:
            _set_result("Please enter a target domain.", COLORS["red"])
            return

        domain = domain.lstrip(".")
        if domain.startswith("http://"):
            domain = domain[7:]
        if domain.startswith("https://"):
            domain = domain[8:]
        domain = domain.split("/")[0].split(":")[0]

        set_scan_state(True)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Scanning subdomains for {domain}...\n")
        output_text.configure(state="disabled")
        progress_bar.set(0)

        def worker():
            found = []
            total = len(WORDLIST)
            scanned = 0

            for prefix in WORDLIST:
                if not is_scanning:
                    break

                subdomain = f"{prefix}.{domain}"
                try:
                    results = socket.getaddrinfo(subdomain, None, socket.AF_INET)
                    if results:
                        ip = results[0][4][0]
                        found.append((subdomain, ip))
                        frame.after(0, lambda s=subdomain, i=ip: _append_text(f"  [FOUND]  {s:<30}  {i}\n"))
                except (socket.gaierror, socket.herror, OSError):
                    pass

                scanned += 1
                if scanned % 10 == 0 or scanned == total:
                    frame.after(0, lambda s=scanned, t=total: progress_bar.set(s / t))

            lines = [f"\n{'='*45}", f"SCAN COMPLETE", f"{'='*45}",
                     f"  Domain:  {domain}",
                     f"  Checked: {scanned} prefixes",
                     f"  Found:   {len(found)} subdomains",
                     f"{'='*45}"]
            frame.after(0, lambda: _append_text("\n".join(lines)))
            color = COLORS["green"] if found else COLORS["text_dim"]
            frame.after(0, lambda: status_label.configure(
                text=f"Found {len(found)} subdomains", text_color=color))
            frame.after(0, lambda: set_scan_state(False))

        threading.Thread(target=worker, daemon=True).start()

    # --- Build UI ---
    title_label = ctk.CTkLabel(
        frame, text="Subdomain Finder", font=FONTS["title"], text_color=COLORS["text"]
    )
    title_label.pack(anchor="w", padx=15, pady=(15, 5))

    subtitle = ctk.CTkLabel(
        frame,
        text="Discover subdomains of a target domain via DNS resolution.",
        font=FONTS["body"], text_color=COLORS["text_dim"],
    )
    subtitle.pack(anchor="w", padx=15, pady=(0, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=15, pady=(0, 5))

    domain_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Target domain (e.g. example.com)...",
        font=FONTS["mono"],
        fg_color=COLORS["bg_input"],
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    domain_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    domain_entry.bind("<Return>", lambda e: do_scan())

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

# --------------------------------------------
# Email Slicer (GUI) with Tkinter
# Features: Validation, Categorization, Multi-input
# --------------------------------------------
import re
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Logic ----------
PERSONAL_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com", "proton.me", "protonmail.com"
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$")

def is_valid_email(email: str) -> bool:
    return EMAIL_REGEX.match(email) is not None

def email_slicer(email: str):
    """Return (username, domain, provider) assuming email is valid."""
    username, domain = email.split("@", 1)
    provider = domain.split(".", 1)[0]
    return username, domain, provider

def categorize_domain(domain: str) -> str:
    return "Personal" if domain.lower() in PERSONAL_DOMAINS else "Business/Work"

# ---------- GUI ----------
class EmailSlicerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Slicer – Tkinter GUI")
        self.geometry("900x520")
        self.minsize(820, 480)

        self._build_ui()

    def _build_ui(self):
        # Title
        title = ttk.Label(self, text="Email Slicer", font=("Segoe UI", 18, "bold"))
        title.pack(pady=(12, 0))

        subtitle = ttk.Label(
            self,
            text="Paste one or more emails (comma-separated). Click Process to slice, validate, and categorize.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=14)

        self.input_text = tk.Text(input_frame, height=4, wrap="word", font=("Consolas", 11))
        self.input_text.pack(side="left", fill="x", expand=True)

        input_scroll = ttk.Scrollbar(input_frame, command=self.input_text.yview)
        input_scroll.pack(side="right", fill="y")
        self.input_text.configure(yscrollcommand=input_scroll.set)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=14, pady=10)

        self.process_btn = ttk.Button(btn_frame, text="Process", command=self.process_emails)
        self.process_btn.pack(side="left")

        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_all)
        self.clear_btn.pack(side="left", padx=8)

        self.copy_btn = ttk.Button(btn_frame, text="Copy Results", command=self.copy_results)
        self.copy_btn.pack(side="left")

        # Table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(4, 0))

        columns = ("email", "username", "domain", "provider", "etype", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=10
        )
        self.tree.heading("email", text="Email")
        self.tree.heading("username", text="Username")
        self.tree.heading("domain", text="Domain")
        self.tree.heading("provider", text="Provider")
        self.tree.heading("etype", text="Type")
        self.tree.heading("status", text="Status")

        self.tree.column("email", width=260, anchor="w")
        self.tree.column("username", width=120, anchor="center")
        self.tree.column("domain", width=160, anchor="center")
        self.tree.column("provider", width=120, anchor="center")
        self.tree.column("etype", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Style tags
        self.tree.tag_configure("invalid", foreground="#b00020")  # red
        self.tree.tag_configure("personal", foreground="#0a7d32") # green
        self.tree.tag_configure("business", foreground="#1b4d89") # blue

        # Summary label
        self.summary_var = tk.StringVar(value="Ready.")
        summary = ttk.Label(self, textvariable=self.summary_var, font=("Segoe UI", 10))
        summary.pack(anchor="w", padx=16, pady=(8, 12))

        # Prefill example (optional)
        self.input_text.insert("1.0", "alice@gmail.com,  bob@company.org, wrong@@mail,  sara@Brand.CO")

    def process_emails(self):
        raw = self.input_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showinfo("Email Slicer", "Please enter at least one email.")
            return

        # Clear previous rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        emails = [e.strip() for e in raw.split(",") if e.strip()]
        total = len(emails)
        valid_count = 0
        personal_count = 0
        business_count = 0

        for e in emails:
            if not is_valid_email(e):
                self.tree.insert("", "end", values=(e, "-", "-", "-", "-", "Invalid"), tags=("invalid",))
                continue

            username, domain, provider = email_slicer(e)
            etype = categorize_domain(domain)
            tag = "personal" if etype == "Personal" else "business"

            self.tree.insert(
                "",
                "end",
                values=(e, username, domain, provider, etype, "OK"),
                tags=(tag,)
            )

            valid_count += 1
            if etype == "Personal":
                personal_count += 1
            else:
                business_count += 1

        invalid_count = total - valid_count
        self.summary_var.set(
            f"Processed: {total} | Valid: {valid_count} | Invalid: {invalid_count} | "
            f"Personal: {personal_count} | Business/Work: {business_count}"
        )

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.summary_var.set("Cleared. Ready.")

    def copy_results(self):
        # Copy current table rows to clipboard as TSV text
        rows = []
        for iid in self.tree.get_children():
            rows.append("\t".join(str(v) for v in self.tree.item(iid, "values")))
        text = "Email\tUsername\tDomain\tProvider\tType\tStatus\n" + "\n".join(rows)

        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Email Slicer", "Results copied to clipboard (TSV).")

if __name__ == "__main__":
    app = EmailSlicerApp()
    app.mainloop()

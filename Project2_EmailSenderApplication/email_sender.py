"""Email Sender Application using Tkinter GUI and SMTP."""

import tkinter as tk
import smtplib
import re
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Constants
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
MIN_PASSWORD_LENGTH = 6
WINDOW_TITLE = "Email Application"
BUTTON_WIDTH = 10
ENTRY_WIDTH = 50
TEXT_AREA_HEIGHT = 10

# Styling Constants
COLOR_BLACK = "black"
COLOR_WHITE = "white"
COLOR_CYAN = "cyan"
COLOR_RED = "red"
FONT_TITLE = ("calibri", 18, "bold")


class EmailSenderApp:
    """Main application class for Email Sender GUI."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the Email Sender Application.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.root.title(WINDOW_TITLE)

        # State variables
        self.smtp_server: Optional[smtplib.SMTP] = None
        self.sender_email: str = ""

        # Create UI frames
        self.login_frame = tk.Frame(root, width=1000, height=800)
        self.status_frame = tk.Frame(root)
        self.compose_frame = tk.Frame(root)

        # Initialize UI components
        self._create_login_frame()
        self._create_status_frame()
        self._create_compose_frame()

        # Show login frame initially
        self._show_login_frame()

    def _create_login_frame(self) -> None:
        """Create and configure the login frame."""
        self.login_frame.pack(side="top")

        tk.Label(
            self.login_frame,
            width=25,
            text="Enter your credentials",
            font=FONT_TITLE,
        ).grid(row=0, columnspan=3, pady=10, padx=10)

        tk.Label(self.login_frame, text="Email:").grid(
            row=1, sticky=tk.E, pady=5, padx=10
        )
        tk.Label(self.login_frame, text="Password:").grid(
            row=2, sticky=tk.E, pady=5, padx=10
        )

        self.email_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.email_entry.grid(row=1, column=1, pady=5)
        self.password_entry.grid(row=2, column=1)

        tk.Button(
            self.login_frame,
            text="Login",
            width=BUTTON_WIDTH,
            bg=COLOR_BLACK,
            fg=COLOR_WHITE,
            command=self.login,
        ).grid(row=3, columnspan=3, pady=10)

    def _create_status_frame(self) -> None:
        """Create and configure the status frame."""
        self.status_label = tk.Label(
            self.status_frame,
            bg=COLOR_CYAN,
            fg=COLOR_RED,
            text="Log in to continue",
        )
        self.status_label.grid(row=0, column=0, columnspan=2, pady=5)

        tk.Button(
            self.status_frame,
            text="Logout",
            width=BUTTON_WIDTH,
            bg=COLOR_BLACK,
            fg=COLOR_WHITE,
            command=self.logout,
        ).grid(row=0, column=4, columnspan=2, pady=10, padx=(5, 0))

    def _create_compose_frame(self) -> None:
        """Create and configure the email composition frame."""
        tk.Label(self.compose_frame, width=20, text="Compose Email").grid(
            row=0, column=0, columnspan=2, pady=5
        )

        tk.Label(self.compose_frame, text="To:").grid(
            row=1, sticky=tk.E, pady=5)
        tk.Label(self.compose_frame, text="Subject:").grid(
            row=2, sticky=tk.E, pady=5)
        tk.Label(self.compose_frame, text="Message:").grid(
            row=3, sticky=tk.E, pady=5)

        self.recipient_entry = tk.Entry(self.compose_frame, width=ENTRY_WIDTH)
        self.subject_entry = tk.Entry(self.compose_frame, width=ENTRY_WIDTH)
        self.message_text = tk.Text(
            self.compose_frame, width=ENTRY_WIDTH, height=TEXT_AREA_HEIGHT
        )

        self.recipient_entry.grid(row=1, column=1, pady=5)
        self.subject_entry.grid(row=2, column=1, pady=5)
        self.message_text.grid(row=3, column=1, pady=5)

        tk.Button(
            self.compose_frame,
            text="Send Mail",
            width=BUTTON_WIDTH,
            bg=COLOR_BLACK,
            fg=COLOR_WHITE,
            command=self.send_email,
        ).grid(row=4, columnspan=3, pady=10)

        self.message_status_label = tk.Label(
            self.compose_frame, width=20, fg=COLOR_WHITE, bg=COLOR_BLACK
        )
        self.message_status_label.grid(row=5, column=0, columnspan=2, pady=5)

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate.

        Returns:
            True if email is valid, False otherwise.
        """
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None

    def _validate_login_credentials(self) -> bool:
        """
        Validate login form inputs.

        Returns:
            True if validation passes, False otherwise.
        """
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not self._is_valid_email(email):
            self.status_label.config(text="Invalid Email")
            self.status_frame.pack(side="top", fill="x")
            return False

        if len(password) < MIN_PASSWORD_LENGTH:
            self.status_label.config(
                text=f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )
            self.status_frame.pack(side="top", fill="x")
            return False

        return True

    def _validate_message_inputs(self) -> bool:
        """
        Validate email composition form inputs.

        Returns:
            True if validation passes, False otherwise.
        """
        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message_body = self.message_text.get("1.0", tk.END).strip()

        if not self._is_valid_email(recipient):
            self.message_status_label.config(text="Invalid Recipient Email")
            return False

        if not subject:
            self.message_status_label.config(text="Subject cannot be empty")
            return False

        if not message_body:
            self.message_status_label.config(
                text="Message body cannot be empty")
            return False

        return True

    def login(self) -> None:
        """Authenticate with Gmail SMTP server."""
        if not self._validate_login_credentials():
            return

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        try:
            self.smtp_server = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
            self.smtp_server.ehlo()
            self.smtp_server.starttls()
            self.smtp_server.login(email, password)

            self.sender_email = email
            self._show_compose_frame()
            self.status_label.config(text="Login Successful")

        except smtplib.SMTPAuthenticationError:
            self.status_label.config(
                text="Authentication Failed: Invalid credentials")
        except smtplib.SMTPException as e:
            self.status_label.config(text=f"SMTP Error: {str(e)[:40]}")
        except OSError as e:
            self.status_label.config(text="Connection Error: Check internet")

    def logout(self) -> None:
        """Disconnect from SMTP server and return to login screen."""
        if self.smtp_server is None:
            return

        try:
            self.smtp_server.quit()
        except smtplib.SMTPServerDisconnected:
            pass
        finally:
            self.smtp_server = None
            self.sender_email = ""
            self._show_login_frame()
            self.status_label.config(text="Logged out successfully")
            self.password_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

    def send_email(self) -> None:
        """Send email using the composed message."""
        if self.smtp_server is None:
            self.message_status_label.config(text="Not logged in")
            return

        if not self._validate_message_inputs():
            return

        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message_body = self.message_text.get("1.0", tk.END).strip()

        try:
            # Create MIME message for proper email formatting
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(message_body, "plain"))

            self.smtp_server.sendmail(
                self.sender_email, recipient, msg.as_string())

            self.message_status_label.config(text="Email sent successfully")
            self._clear_compose_fields()

        except smtplib.SMTPRecipientsRefused:
            self.message_status_label.config(text="Recipient email rejected")
        except smtplib.SMTPException as e:
            self.message_status_label.config(text=f"SMTP Error: {str(e)[:40]}")
        except OSError:
            self.message_status_label.config(text="Connection Error")

    def _clear_compose_fields(self) -> None:
        """Clear all email composition fields."""
        self.recipient_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.message_text.delete("1.0", tk.END)

    def _show_login_frame(self) -> None:
        """Display login frame and hide others."""
        self.login_frame.pack(side="top")
        self.status_frame.pack_forget()
        self.compose_frame.pack_forget()

    def _show_compose_frame(self) -> None:
        """Display compose frame and hide login."""
        self.login_frame.pack_forget()
        self.status_frame.pack(side=tk.TOP, expand=tk.NO, fill=tk.NONE)
        self.compose_frame.pack(side=tk.TOP, expand=tk.NO, fill=tk.NONE)


def main() -> None:
    """Main entry point for the application."""
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

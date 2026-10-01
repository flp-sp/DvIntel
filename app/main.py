from datetime import datetime

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown, Static

from agentic_loop import submit_prompt  # lógica do agente: inalterada

try:
    from textual.markup import escape
except ImportError:  # versões antigas do Textual
    from rich.markup import escape


def stamp() -> str:
    return datetime.now().strftime("%H:%M")


class MegaBrain(App):
    TITLE = "🧠 MegaBrain"
    SUB_TITLE = "agente de IA"

    BINDINGS = [
        ("ctrl+l", "clear", "Limpar"),
        ("ctrl+q", "quit", "Sair"),
    ]

    CSS = """
    Screen {
        layout: vertical;
    }

    #chat {
        height: 1fr;
        padding: 1 2;
        border: round $primary;
        margin: 0 1;
        scrollbar-size-vertical: 1;
    }

    .msg-header {
        margin-top: 1;
        height: auto;
    }

    .msg-user {
        height: auto;
        padding-left: 2;
    }

    .msg-error {
        height: auto;
        padding-left: 2;
        color: $error;
    }

    .msg-bot {
        height: auto;
        padding-left: 1;
        margin: 0;
        background: transparent;
    }

    #status {
        height: 1;
        margin: 0 2;
        color: $text-muted;
    }

    #prompt {
        margin: 0 1 1 1;
        border: round $accent;
    }
    """

    busy = False

    # ---------- UI ----------
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="chat")
        yield Static("● Pronto", id="status")
        yield Input(placeholder="Digite sua mensagem e pressione Enter...", id="prompt")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#prompt", Input).focus()

    # ---------- Helpers ----------
    def set_status(self, text: str) -> None:
        self.query_one("#status", Static).update(text)

    def add_header(self, markup: str) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        chat.mount(Static(markup, classes="msg-header"))

    def add_user(self, text: str) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        self.add_header(f"[bold cyan]Você[/]  [dim]{stamp()}[/]")
        chat.mount(Static(escape(text), classes="msg-user"))
        chat.scroll_end(animate=False)

    def add_bot(self, text: str) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        self.add_header(f"[bold green]MegaBrain[/]  [dim]{stamp()}[/]")
        chat.mount(Markdown(text, classes="msg-bot"))  # respostas em Markdown
        chat.scroll_end(animate=False)

    def add_error(self, text: str) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        self.add_header(f"[bold red]Erro[/]  [dim]{stamp()}[/]")
        chat.mount(Static(escape(text), classes="msg-error"))
        chat.scroll_end(animate=False)

    # ---------- Lógica (mesma de antes) ----------
    @work(thread=True)
    def send_async(self, input_text: str) -> None:
        try:
            resposta = submit_prompt(input_text)
            self.call_from_thread(self.add_bot, str(resposta))
            self.call_from_thread(self.set_status, "● Pronto")
        except Exception as e:  # não derruba a UI se o agente falhar
            self.call_from_thread(self.add_error, str(e))
            self.call_from_thread(self.set_status, "[red]● Falha ao responder[/]")
        finally:
            self.call_from_thread(self.finish)

    def finish(self) -> None:
        self.busy = False
        prompt = self.query_one("#prompt", Input)
        prompt.disabled = False
        prompt.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_text = event.value.strip()
        if not input_text or self.busy:
            return

        self.busy = True
        event.input.value = ""
        event.input.disabled = True

        self.add_user(input_text)
        self.set_status("[yellow]● MegaBrain está pensando...[/]")
        self.send_async(input_text)

    def action_clear(self) -> None:
        self.query_one("#chat", VerticalScroll).remove_children()
        self.set_status("● Conversa limpa")


if __name__ == "__main__":
    MegaBrain().run()
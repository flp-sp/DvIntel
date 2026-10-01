import threading
from datetime import datetime

import pytermgui as ptg
from agentic_loop import submit_prompt  # lógica do agente: inalterada

# ---------- Tema ----------
ACCENT = "210"
USER_COLOR = "75"
BOT_COLOR = "78"
DIM = "245"
ERR_COLOR = "203"

# Larguras fixas e explícitas (nada fica com largura 0)
WIDTH = 80
CHAT_HEIGHT = 18

busy = False  # evita enviar duas mensagens ao mesmo tempo


def esc(text: str) -> str:
    """Escapa '[' para o texto não ser lido como markup."""
    return text.replace("\\", "\\\\").replace("[", "\\[")


def L(text: str = " ") -> "ptg.Label":
    """Label alinhado à esquerda."""
    return ptg.Label(text, parent_align=ptg.HorizontalAlignment.LEFT)


def stamp() -> str:
    return datetime.now().strftime("%H:%M")


with ptg.WindowManager() as manager:
    # ---------- Widgets ----------
    chat_ui = ptg.Container(
        height=CHAT_HEIGHT,
        overflow=ptg.Overflow.SCROLL,
        box="EMPTY",
        vertical_align=ptg.VerticalAlignment.TOP,
    )

    status = L(f"[{DIM}]● Pronto")

    input_prompt = ptg.InputField("", prompt="> ", width=WIDTH - 8)

    # ---------- Helpers ----------
    def add_message(author_markup: str, text: str):
        chat_ui._add_widget(L(f"{author_markup} [{DIM}]{stamp()}[/]"))
        chat_ui._add_widget(L(esc(text)))
        chat_ui._add_widget(L(" "))
        chat_ui.scroll_end(1)

    def set_status(text: str):
        status.value = text

    # ---------- Lógica (mesma de antes) ----------
    def send_async(input_text):
        global busy
        try:
            resposta = submit_prompt(input_text)
            add_message(f"[bold {BOT_COLOR}]MegaBrain:[/]", str(resposta))
            set_status(f"[{DIM}]● Pronto")
        except Exception as e:
            add_message(f"[bold {ERR_COLOR}]Erro:[/]", str(e))
            set_status(f"[{ERR_COLOR}]● Falha ao responder")
        finally:
            busy = False

    def send(button_or_widget, *args):
        global busy
        input_text = input_prompt.value.strip()
        if not input_text or busy:
            return

        busy = True
        add_message(f"[bold {USER_COLOR}]Você:[/]", input_text)
        set_status(f"[{ACCENT}]● MegaBrain está pensando...")

        input_prompt._lines = [""]
        input_prompt._cursor = [0, 0]
        input_prompt._style_and_break_lines()

        threading.Thread(target=send_async, args=(input_text,), daemon=True).start()

    input_prompt.bind(ptg.keys.ENTER, send)

    def quit_app(*_):
        manager.stop()

    # ---------- Layout ----------
    window = (
        ptg.Window(
            L(f"[bold {ACCENT}]MegaBrain[/] [{DIM}]· agente de IA[/]"),
            L(),
            chat_ui,
            L(),
            input_prompt,
            L(),
            ptg.Button("Enviar", send),
            ptg.Button("Sair", quit_app),
            status,
            width=WIDTH,
            box="ROUNDED",
        )
        .set_title(f"[{ACCENT} bold] MegaBrain ")
        .center()
    )

    manager.add(window)
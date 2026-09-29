import pytermgui as ptg
import threading
from agentic_loop import submit_prompt

with ptg.WindowManager() as manager:
    chat_ui = ptg.Container(
        height=15,
        overflow = ptg.Overflow.SCROLL,
        box = "EMPTY")

    input_prompt = ptg.InputField("", prompt="> ", width=50)

    def send_async(input_text):
        resposta = submit_prompt(input_text)
        chat_ui._add_widget(ptg.Label(f"[bold green]DvIntel:[/] {resposta}"))
        chat_ui._add_widget(ptg.Label(""))

        chat_ui.scroll_end(1)


    def send(button_or_widget, *args):
        input_text = input_prompt.value.strip()

        chat_ui._add_widget(ptg.Label(f"[bold blue]User:[/] {input_text}"))
        #resposta = submit_prompt(input_text)
        input_prompt._lines = [""]
        input_prompt._cursor = [0, 0]
        input_prompt._style_and_break_lines()

        threading.Thread(target=send_async, args=(input_text,), daemon=True).start()    

        #chat_ui._add_widget(ptg.Label(""))

        #chat_ui.scroll_end(1)

    input_prompt.bind(ptg.keys.ENTER, send)

    window = (
        ptg.Window(
            chat_ui,
            input_prompt,
            ptg.Button("Submit", send),
            width=60,
            box="DOUBLE")

        .set_title("[210 bold]DvIntel")
        .center())

    manager.add(window)
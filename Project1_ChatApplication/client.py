import socket
import tkinter
from threading import Thread

host = 'localhost'
port = 8080

window = tkinter.Tk()

my_msg = tkinter.StringVar()
my_msg.set("")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))


def send_message(event=None):
    """
    Sends a message to the server.
    """
    msg = my_msg.get()
    my_msg.set("")
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        window.quit()


def quit_chat():
    """
    Quits the chat application.
    """
    my_msg.set("#quit")
    send_message()


window.title("Chat Client")
window.configure(bg="lightblue")

message_frame = tkinter.Frame(window, height=500, width=200, bg="red")
message_frame.pack()

scroll_bar = tkinter.Scrollbar(message_frame)

msg_list = tkinter.Listbox(
    message_frame, height=15, width=150, bg="lightgray", yscrollcommand=scroll_bar.set)

scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

label = tkinter.Label(
    window, text="Type your message below:", bg="lightblue")
label.pack()

entry_field = tkinter.Entry(window, textvariable=my_msg, width=150)
entry_field.bind("<Return>", send_message)
entry_field.pack()

send_button = tkinter.Button(
    window, text="Send", font="Aerial", command=send_message)
send_button.pack()

quit_button = tkinter.Button(
    window, text="Quit", font="Aerial", command=quit_chat)
quit_button.pack()


def receive():
    """
    Receives messages from the server and displays them in the message list.
    """
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except:
            print("An error occurred!")
            break


if __name__ == "__main__":
    t1 = Thread(target=receive)
    t1.start()
    tkinter.mainloop()

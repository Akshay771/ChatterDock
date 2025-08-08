class ChatRoom:
    def __init__(self):
        self.messages = []
        self.message_counter = 1

    def send_message(self, sender, content):
        message = Message(self.message_counter, sender, content, datetime.now())
        self.messages.append(message)
        self.message_counter += 1

    def get_message_by_id(self, message_id):
        for message in self.messages:
            if message.message_id == message_id:
                return message
        return None


chat_room = ChatRoom()
chat_room.send_message("Alice", "Hello, Bob!")
chat_room.send_message("Bob", "Hi, Alice!")
message = chat_room.get_message_by_id(2)
if message:
    print(f"Message {message.message_id}: {message.content}")
else:
    print("Message not found.")
import tkinter as tk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Read data from Excel file
df = pd.read_excel(r'C:\Users\Senthilnayaki\seed_data.xlsx')

# Preprocess the data if necessary (e.g., remove duplicates, clean text, etc.)

# Combine all text columns into one
df['Text'] = df['Seed Type'] + ' ' + df['Location'] + ' ' + df['Temperature Range'] + ' ' + df['Soil Type'] + ' ' + df['Budget Range']

# Initialize TfidfVectorizer
vectorizer = TfidfVectorizer()

# Transform text data into numerical features
X = vectorizer.fit_transform(df['Text'])

# Train a simple machine learning model
model = LogisticRegression()
model.fit(X, df['Seed Type'])

def get_seed_type(input_text):
    vectorized_input = vectorizer.transform([input_text])
    predicted_seed_type = model.predict(vectorized_input)
    return predicted_seed_type[0]

def send_message(event=None):
    user_input = entry.get()
    if user_input:
        response = get_seed_type(user_input)
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "You: " + user_input + "\n", "user_message")
        chat_log.insert(tk.END, "Bot: " + response + "\n\n", "bot_message")
        chat_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        chat_log.see(tk.END)

# Create UI
root = tk.Tk()
root.title("ChatBot")

# Styling
root.configure(bg="#f0f0f0")
root.geometry("600x600")

# Define frames for chat log and entry field
chat_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame = tk.Frame(root, bg="#f0f0f0")

# Create chat log text widget
chat_log = tk.Text(chat_frame, width=50, height=20, state=tk.DISABLED, bg="#f2f2f2", wrap="word", font=("Arial", 12))
scrollbar = tk.Scrollbar(chat_frame, command=chat_log.yview)
chat_log.config(yscrollcommand=scrollbar.set)

# Create entry field and send button
entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
send_button = tk.Button(entry_frame, text="Send", command=send_message, bg="#4caf50", fg="white", font=("Arial", 12))

# Pack widgets into frames
chat_frame.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)
entry_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH)

chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
send_button.pack(side=tk.RIGHT, padx=(5, 0))

# Configure tags for message formatting
chat_log.tag_configure("user_message", foreground="#1e88e5", justify="left", background="#f2f2f2")
chat_log.tag_configure("bot_message", foreground="#4caf50", justify="right", background="#e0e0e0")

# Bind Enter key to send_message function
root.bind("<Return>", send_message)

root.mainloop()

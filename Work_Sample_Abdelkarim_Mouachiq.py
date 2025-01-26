import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import tkinter as tk
from tkinter import messagebox, filedialog

# 1. Scraping Function
def scrape_madkudu_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "No title found"
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        value_proposition = meta_desc['content'] if meta_desc else "No value proposition found."

        sections = soup.find_all('section')
        section_texts = [section.get_text(strip=True) for section in sections[:3]]

        return {
            "title": title,
            "value_proposition": value_proposition,
            "additional_info": " ".join(section_texts)
        }
    except Exception as e:
        return {"error": f"Failed to scrape website: {e}"}

# 2. LinkedIn Note Generation
def generate_connect_note(contact_name, job_title, company_name, value_proposition):
    return (
        f"Hello {contact_name},\n\n"
        f"I recently explored {company_name} and was impressed by its innovative approach: "
        f"'{value_proposition}'. Your role as {job_title} must be key to its success. "
        f"I would love to connect and learn more about your experience."
    )

# 3. Training ML Model
def train_ml_model(data):
    X = data[["company_size", "industry", "annual_revenue"]]
    y = data["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy

# 4. Save Model
def save_model(model, filename="model.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(model, f)

# 5. Load Model
def load_model(filename="model.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)

# Tkinter Interface
class MadKuduApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MadKudu AI Agent")
        self.root.geometry("600x400")

        # URL Entry
        self.url_label = tk.Label(root, text="Enter MadKudu Website URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "https://www.madkudu.com")

        # Scrape Button
        self.scrape_button = tk.Button(root, text="Scrape Website", command=self.scrape_website)
        self.scrape_button.pack(pady=5)

        # Generate LinkedIn Note
        self.note_frame = tk.Frame(root)
        self.note_label = tk.Label(self.note_frame, text="Generate LinkedIn Note")
        self.note_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.contact_label = tk.Label(self.note_frame, text="Contact Name:")
        self.contact_label.grid(row=1, column=0, pady=5)
        self.contact_entry = tk.Entry(self.note_frame, width=30)
        self.contact_entry.grid(row=1, column=1, pady=5)
        self.job_label = tk.Label(self.note_frame, text="Job Title:")
        self.job_label.grid(row=2, column=0, pady=5)
        self.job_entry = tk.Entry(self.note_frame, width=30)
        self.job_entry.grid(row=2, column=1, pady=5)
        self.note_button = tk.Button(self.note_frame, text="Generate Note", command=self.generate_note)
        self.note_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.note_frame.pack(pady=10)

        # ML Training Button
        self.ml_button = tk.Button(root, text="Train ML Model", command=self.train_model)
        self.ml_button.pack(pady=5)

    def scrape_website(self):
        url = self.url_entry.get()
        data = scrape_madkudu_website(url)
        if "error" in data:
            messagebox.showerror("Error", data["error"])
        else:
            result = f"Title: {data['title']}\nValue Proposition: {data['value_proposition']}\nAdditional Info: {data['additional_info']}"
            messagebox.showinfo("Scraping Result", result)

    def generate_note(self):
        contact_name = self.contact_entry.get()
        job_title = self.job_entry.get()
        url = self.url_entry.get()
        data = scrape_madkudu_website(url)
        value_proposition = data.get("value_proposition", "No value proposition found.")
        note = generate_connect_note(contact_name, job_title, "MadKudu", value_proposition)
        messagebox.showinfo("LinkedIn Note", note)

    def train_model(self):
        sample_data = pd.DataFrame({
            "company_size": [10, 50, 200, 500],
            "industry": [0, 1, 0, 1],
            "annual_revenue": [1, 5, 50, 20],
            "target": [1, 1, 0, 1]
        })
        model, accuracy = train_ml_model(sample_data)
        save_model(model)
        messagebox.showinfo("ML Model", f"Model trained and saved!\nAccuracy: {accuracy:.2f}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MadKuduApp(root)
    root.mainloop()

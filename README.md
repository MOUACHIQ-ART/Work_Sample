#  Work_Sample - AI Agent

### 1. Website Scraping

#### a) Extracting Key Information

The agent scrapes the following details from the MadKudu website:
- **Title** of the webpage.
- **Value Proposition** extracted from the meta description.
- **Main Sections** content from the first three sections of the website.

#### b) Technology Used

The scraping functionality is implemented using:
- `requests` for sending HTTP requests to the website.
- `BeautifulSoup` for parsing and extracting HTML content.

---

### 2. LinkedIn Note Generation

#### a) Generating Personalized Notes

The agent generates LinkedIn connection notes using:
- The contact's name.
- Their job title.
- The company name (MadKudu).
- The value proposition extracted from the website.




---

### 3. Client Prediction with Machine Learning

#### a) Training the Model

The agent uses a **Random Forest Classifier** to predict potential clients. The model uses the following features:
- **Company Size**: Number of employees.
- **Industry Type**: Technology or Marketing.
- **Annual Revenue**: Total yearly revenue in millions.

#### b) Accuracy of Predictions

The model evaluates its performance using **accuracy** as a metric, which is displayed after training.

---

### 4. Graphical User Interface (GUI)

#### a) Features

The GUI allows users to:
1. **Scrape Website Data**: Enter the website URL to extract information.
2. **Generate LinkedIn Notes**: Provide contact details to create a custom note.
3. **Train the Machine Learning Model**: Train a model and display its accuracy.

#### b) Technology Used

The GUI is built with `Tkinter`, a built-in Python library for graphical user interfaces.

---

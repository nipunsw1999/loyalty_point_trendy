# Loyalty Points Software - Trendy

This is a **Loyalty Points Management Software** designed for businesses.  
With this software, you can:

✅ Register your customers  
✅ Add services with their prices and corresponding points  
✅ Update customer details anytime  
✅ Ask questions from AI using **LLM (Large Language Model)** integration  

---

## 📥 Installation Guide

### 1. Setup the Database

- Import the provided `trendy.sql` file into your **MySQL server**.
- Update the **database connection details** inside `function.py` with your actual MySQL credentials:
    - Host
    - User
    - Password
    - Database Name

---

### 2. Create and Activate Python Virtual Environment

#### On Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### On Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies:
```bash
pip install -r requirements.txt
```

---

### 4. Setup `.env` File for Groq API Key

Create a `.env` file in the project root and add the following content:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Replace `your_groq_api_key_here` with your actual Groq API key.

---

### 5. Run the Application

```bash
streamlit run app.py
```

Now, the Loyalty Points Software should be up and running! 🚀


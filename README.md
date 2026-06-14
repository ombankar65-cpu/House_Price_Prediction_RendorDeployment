# 🏠 House Price Prediction Deployment on AWS EC2

This project is a Flask-based House Price Prediction application that uses a trained Machine Learning model (`model.pkl`) to estimate property prices based on user inputs.

## Project Structure

```bash
House_Price_Prediction_RendorDeployment/
│
├── app.py
├── model.pkl
├── requirements.txt
└── README.md
```

---

## Prerequisites

* AWS EC2 Instance (Ubuntu 22.04)
* Python 3
* Git
* Internet Connection

---

## Step 1: Launch an EC2 Instance

Create an Ubuntu EC2 instance and ensure the following ports are allowed in the Security Group:

| Port | Protocol | Purpose           |
| ---- | -------- | ----------------- |
| 22   | TCP      | SSH Access        |
| 80   | TCP      | HTTP Access       |
| 5000 | TCP      | Flask Application |

---

## Step 2: Connect to EC2

```bash
ssh -i <your-key.pem> ubuntu@<EC2-Public-IP>
```

---

## Step 3: Update Packages

```bash
sudo apt update
```

---

## Step 4: Install Required Dependencies

```bash
sudo apt install python3-pip python3-venv nginx git -y
```

---

## Step 5: Clone the Repository

```bash
git clone https://github.com/ombankar65-cpu/House_Price_Prediction_RendorDeployment.git
```

Move into the project directory:

```bash
cd House_Price_Prediction_RendorDeployment/
```

---

## Step 6: Create Python Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

---

## Step 7: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 8: Verify Project Files

```bash
ls
```

Expected output:

```bash
app.py
model.pkl
requirements.txt
venv
```

---

## Step 9: Start the Flask Application

```bash
python3 app.py
```

Expected output:

```bash
* Running on http://0.0.0.0:5000
```

---

## Step 10: Access the Application

Open your browser and navigate to:

```text
http://<EC2-PUBLIC-IP>:5000
```

Example:

```text
http://13.233.xx.xx:5000
```

You should see the House Price Prediction dashboard.

---

## Features

* Property Price Prediction using Machine Learning
* Flask Backend
* Responsive User Interface
* Real-time Prediction API
* AWS EC2 Deployment Ready

---

## Tech Stack

### Backend

* Python
* Flask
* NumPy
* Pickle

### Frontend

* HTML
* Tailwind CSS
* JavaScript

### Cloud

* AWS EC2
* Ubuntu Linux

---

## API Endpoint

### Predict House Price

**POST** `/predict`

Request Body:

```json
{
  "beds": 3,
  "baths": 2,
  "size": 1800,
  "lot_size": 5000,
  "zip_code": 90210
}
```

Response:

```json
{
  "success": true,
  "prediction": 450000
}
```

---

## Author

**Om Raju Bankar**

GitHub: https://github.com/ombankar65-cpu

---

## License

This project is created for educational and deployment learning purposes.

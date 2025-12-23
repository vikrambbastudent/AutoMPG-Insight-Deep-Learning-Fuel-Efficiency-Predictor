# 🚗 Fuel Efficiency Prediction using Deep Learning (Keras + TensorFlow)

## 📌 Problem Statement
Fuel efficiency (measured in **Miles Per Gallon – MPG**) is a critical metric for evaluating vehicle performance, cost-effectiveness, and environmental impact.  
The objective of this project is to **predict the MPG of a car based on its technical specifications** using machine learning and to provide an **interactive web application** for end users.

---

## 🎯 Project Goals
- Predict fuel efficiency (MPG) using vehicle features
- Compare different feature sets to identify the most effective model
- Build a user-friendly **Streamlit web app**
- Save and reuse trained models for deployment
- Maintain clean project structure suitable for GitHub and production use

---

## 📂 Project Structure

<pre>
Fuel-Efficiency-Prediction/
│
├── data/
│   └── auto-mpg.csv
│
├── notebooks/
│   └── Predict_Fuel_Efficiency_Using_Tensorflow.ipynb
│
├── Models/
│   └── trained_keras_model/
│       ├── mpg_model.keras
│       ├── norm.pkl
│       └── car_lookup.pkl
│
├── app.py
├── requirements.txt
└── README.md
</pre>


---

## 🧠 Dataset Description
- Dataset: **Auto MPG Dataset**
- Source: UCI Machine Learning Repository
- Target Variable:
  - `mpg` (continuous → regression problem)
- Features used:
  - `cylinders`
  - `horsepower`
  - `weight`
  - `acceleration`
  - `model year`
  - `origin`

---

## 🔍 Approach & Methodology

### 1️⃣ Data Preprocessing
- Removed unnecessary columns (`car name` for baseline model)
- Handled missing values
- Converted categorical features (`origin`) into numerical form
- Split dataset into:
  - **Training set (80%)**
  - **Validation set (20%)**
- Computed:
  - `train_mean`
  - `train_std`
- Applied **Z-score normalization**

---

### 2️⃣ Feature Engineering & Model Experiments
Three models were trained and evaluated:

| Model | Features Used | MAE |
|------|--------------|-----|
| Model A | Without displacement & car name | **1.68** |
✅ **Model A performed best** and was selected for deployment.

---

### 3️⃣ Model Architecture (Keras)
- Framework: **TensorFlow + Keras**
- Model Type: **Neural Network Regression**
- Architecture:
  - Dense layers with ReLU activation
  - Batch Normalization
  - Dropout for regularization
- Loss Function: `MAE`
- Optimizer: `Adam`

---

### 4️⃣ Model Training & Saving Artifacts
Saved the following artifacts for reuse:
- `mpg_model.keras` → trained model
- `norm.pkl` → normalization values (mean & std)
- `car_lookup.pkl` → car name to feature mapping

---

## 🖥️ Streamlit Web Application

### Key Features
- Manual vehicle specification input
- Optional **car name lookup** (auto-fills specifications)
- Real-time MPG prediction
- Visual fuel-efficiency feedback:
  - Excellent
  - Average
  - Low

### Technologies Used
- Streamlit
- TensorFlow
- Pandas
- Pickle

---

## ⚙️ Installation & Usage

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/fuel-efficiency-prediction.git
cd fuel-efficiency-prediction
```

## 2️⃣ Run the Streamlit App
```bash
streamlit run app.py
```

### 3️⃣ Install Python Dependencies
## ⚙️ Installation & Usage

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/fuel-efficiency-prediction.git
cd fuel-efficiency-prediction
```

## 2️⃣ Run the Streamlit App
```bash
streamlit run app.py
```

### 3️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```



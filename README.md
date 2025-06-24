# 🛍️ Customer Segmentation Web App
A Streamlit-based Web App for Retail Customer Segmentation using K-Means Clustering.
Helps businesses group customers based on purchase behavior for targeted marketing strategies.


## 📂 Dataset Format (for Upload)
The dataset **must** be in **CSV** format and should contain **at least** the following columns:
| Column Name               | Type    | Description                                 |
| ------------------------- | ------- | ------------------------------------------- |
| `CustomerID`              | Integer | Unique customer identifier (optional)       |
| `Gender`                  | String  | Gender of customer (`Male` / `Female`)      |
| `Annual Income (k$)`      | Integer | Customer’s annual income in thousands (\$k) |
| `Spending Score (1-100)`  | Integer | Spending score assigned by the mall (1-100) |


## 🎮 Features & Usage

### ✅ 1. Dataset Summary + Predict
* Upload dataset → Shows stats, missing values, **and predicts clusters + behaviors**.
* 📈 Visualizes customer segments.
* 📥 Option to download predictions as CSV.

### ✅ 2. Behavior-Based Filtering
* Upload **predicted dataset** (from feature 1).
* Select **customer behavior type** to filter:
  * **High Income, High Spending**
  * **High Income, Low Spending**
  * **Low Income, High Spending**
  * **Low Income, Low Spending**

### ✅ 3. Predict Single Customer
Input individual customer details to predict their segment:
| Input Field              | Type    | Range    |
| ------------------------ | ------- | -------- |
| `Annual Income (k$)`     | Integer | 0 to 150 |
| `Spending Score (1-100)` | Integer | 0 to 100 |

→ Output: Predicted cluster and corresponding behavior label.


## ⚙️ Technologies Used
* **Python 3.x**
* **Streamlit**
* **Scikit-learn (KMeans)**
* **Matplotlib**
* **Pandas, NumPy**


## 📧 Contact
**Developed by:** Harsh Verma
**Email:** harshverma11204@gmail.com
**LinkedIn:** https://www.linkedin.com/in/harsh-verma-1b3857287?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B74cq2lv0QG2EmdzBU4tbbQ%3D%3D

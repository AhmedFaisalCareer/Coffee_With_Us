# ☕ Coffee With Us

> A modern cafe ordering and management system built with Python and Streamlit.

**Coffee With Us** is a full-featured cafe management and ordering application designed to handle customer orders, order tracking, inventory, products, customers, sales, and cafe settings from one simple interface.

## 🌐 Live Demo

🚀 **Live Demo:**http://coffeewithus-49ibgzif7qvnrov6rtofpm.streamlit.app/

📂 **GitHub Repository:** https://github.com/AhmedFaisalCareer/Coffee_With_Us

---

## ✨ Features

### 🛒 Customer Ordering

* Browse the cafe menu
* Search for products
* Filter products by category
* Add products to cart
* Adjust quantities
* Remove items from cart
* View subtotal, tax, delivery fee, and total
* Enter customer information
* Select payment method
* Place orders

### 📦 Order Tracking

Customers can track their orders using their unique order ID.

Example:

```text
CWU-0001
```

The order tracking system displays:

* Customer name
* Order time
* Current order status
* Order progress
* Ordered items
* Invoice
* Bill summary
* Payment method

### 👨‍💼 Staff Dashboard

The staff area provides an admin dashboard for managing the cafe.

Features include:

* 📊 Sales dashboard
* 📦 Order management
* 🛍️ Product management
* 📋 Inventory management
* 👥 Customer records
* ⚙️ Cafe settings

### 📊 Dashboard

The dashboard provides useful business information such as:

* Today's revenue
* Today's profit
* Today's orders
* Low-stock products
* Revenue overview
* Best-selling products

### 📦 Inventory Management

Staff can monitor product stock levels and identify products that are running low.

Products can be:

* Added
* Edited
* Deleted
* Marked available/unavailable
* Updated with new stock quantities

### 👥 Customer Management

The customer section keeps track of customer activity, including:

* Customer names
* Phone numbers
* Number of orders
* Total spending

### ⚙️ Cafe Settings

Staff can configure:

* Tax rate
* Delivery fee
* Cafe open/closed status

---

## ☕ Menu Categories

Coffee With Us currently supports several menu categories:

* ☕ Coffee
* 🥤 Frappes
* 🍵 Matcha
* 🍪 Cookies
* 🍰 Desserts
* 🥪 Snacks
* 🧊 Cold Drinks

---

## 🛠️ Technologies Used

| Technology   | Purpose              |
| ------------ | -------------------- |
| 🐍 Python    | Application logic    |
| 🎨 Streamlit | Web interface        |
| 🗄️ SQLite   | Database             |
| 🐼 Pandas    | Data processing      |
| 📊 Plotly    | Charts and analytics |

---

## 📁 Project Structure

```text
Coffee-With-Us/
│
├── app.py
├── requirements.txt
├── README.md
└── coffee_with_us.db
```

> The SQLite database is created automatically by the application when required.

---

## 🔐 Admin Access

The application includes a staff/admin area for managing the cafe.

The admin section includes:

```text
Dashboard
Orders
Products
Inventory
Customers
Settings
```

> ⚠️ The current admin password is intended for demonstration/testing purposes only. For a real business deployment, use a secure password and store credentials using environment variables or Streamlit Secrets instead of hardcoding them in the application.

---

## 📦 Order Status System

Orders can move through the following stages:

```text
Received
    ↓
Preparing
    ↓
In the Oven
    ↓
Ready
    ↓
Delivered
```

Orders can also be marked as:

```text
Cancelled
```

---

## 🧾 Order ID System

Every order receives a unique order code.

Example:

```text
CWU-0001
CWU-0002
CWU-0003
```

Customers can use this code to track their order.

---

## 💰 Business Management

The application calculates and displays:

* Product prices
* Subtotal
* Tax
* Delivery fee
* Final total
* Estimated profit
* Product costs
* Inventory quantities

This makes the application useful as a small cafe management prototype as well as an ordering system.

---

## 🎯 Project Goals

Coffee With Us was created to demonstrate how a Python application can combine:

* Web application development
* Database management
* Business logic
* Inventory management
* Order processing
* Data visualization
* Customer management
* Admin dashboards

---

## 🔮 Future Improvements

Possible future versions could include:

* 🔐 Secure authentication
* 👤 Customer accounts
* 💳 Online payment integration
* 📧 Email order notifications
* 📱 Improved mobile interface
* 🖨️ Receipt printing
* 📈 More advanced analytics
* ☁️ Cloud database integration
* 🔔 Real-time order notifications
* 🧑‍🍳 Dedicated kitchen display
* 📱 QR-code menu ordering

---

## 👨‍💻 Developer

**Ahmed Faisal**

Student Developer | Python | Streamlit | AI & Automation

Currently learning and building projects with:

* Python
* Streamlit
* AI & LLMs
* Automation
* APIs
* Business applications

---

## ⭐ Support the Project

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

Thanks for checking out **Coffee With Us**! ☕

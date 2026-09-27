import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd
import plotly.express as px
from supabase import create_client

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Coffee With Us",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "coffee_with_us.db"
ADMIN_PASSWORD = "123456"

# =========================================================
# SUPABASE CONNECTION
# =========================================================

@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = get_supabase()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .stApp {
        background: #faf7f2;
    }

    [data-testid="stSidebar"] {
        background: #2b1b14;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        background: linear-gradient(135deg, #3b2117, #8b5e3c);
        padding: 45px 35px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.9;
    }

    .product-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #eadfd6;
        margin-bottom: 15px;
        box-shadow: 0 5px 18px rgba(60, 35, 20, 0.06);
    }

    .product-icon {
        font-size: 48px;
        text-align: center;
    }

    .price {
        font-size: 22px;
        font-weight: bold;
        color: #7b4a2f;
    }

    .category-title {
        font-size: 30px;
        font-weight: bold;
        color: #3b2117;
        margin-top: 20px;
    }

    .order-box {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #eadfd6;
        margin-bottom: 15px;
    }

    .status-box {
        padding: 15px;
        border-radius: 15px;
        background: #f3e7dc;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #5c321e;
    }

    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #eadfd6;
        text-align: center;
    }

    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: #6b3f27;
    }

    .metric-label {
        color: #777;
    }

    .receipt {
        background: white;
        padding: 30px;
        border-radius: 18px;
        border: 1px dashed #9b765d;
    }

    .small-text {
        color: #777;
        font-size: 14px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        color: #2b1b14 !important;
        background-color: #ffffff !important;
        border: 1px solid #d8c5b7 !important;
    }

    div.stButton > button:hover {
        color: #ffffff !important;
        background-color: #8b5e3c !important;
        border-color: #8b5e3c !important;
    }

    [data-testid="stSidebar"] div.stButton > button {
        color: #2b1b14 !important;
        background-color: #ffffff !important;
        border: 1px solid #ffffff !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        color: #ffffff !important;
        background-color: #8b5e3c !important;
    }

    [data-testid="stSidebar"] input {
        color: #222222 !important;
        background-color: #ffffff !important;
    }

    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DEFAULT MENU
# =========================================================

DEFAULT_PRODUCTS = [
    ("Cappuccino", "Coffee", "Rich espresso with steamed milk foam.", 420, 170, "☕", 30),
    ("Café Latte", "Coffee", "Smooth espresso with creamy steamed milk.", 450, 180, "🥛", 30),
    ("Americano", "Coffee", "Classic espresso with hot water.", 320, 110, "☕", 30),
    ("Mocha", "Coffee", "Chocolate, espresso and steamed milk.", 480, 200, "🍫", 25),
    ("Caramel Macchiato", "Coffee", "Espresso with caramel and creamy milk.", 520, 220, "🍮", 20),

    ("Classic Frappe", "Frappes", "Cold, creamy and refreshing coffee frappe.", 550, 230, "🧋", 25),
    ("Chocolate Frappe", "Frappes", "Chocolate blended frappe topped with cream.", 580, 250, "🍫", 25),
    ("Caramel Frappe", "Frappes", "Caramel blended frappe.", 590, 260, "🍯", 25),
    ("Vanilla Frappe", "Frappes", "Smooth vanilla cold frappe.", 550, 230, "🥤", 25),

    ("Classic Matcha", "Matcha", "Smooth Japanese-style matcha drink.", 520, 210, "🍵", 20),
    ("Iced Matcha Latte", "Matcha", "Refreshing iced matcha with milk.", 560, 230, "🍵", 20),
    ("Strawberry Matcha", "Matcha", "Matcha with strawberry flavor.", 620, 270, "🍓", 20),

    ("Chocolate Chip Cookie", "Cookies", "Fresh soft-baked chocolate chip cookie.", 220, 80, "🍪", 40),
    ("Double Chocolate Cookie", "Cookies", "Rich chocolate cookie.", 240, 90, "🍪", 35),
    ("Oatmeal Cookie", "Cookies", "Soft oatmeal cookie.", 210, 75, "🍪", 30),

    ("Chocolate Cake", "Desserts", "Moist chocolate cake slice.", 380, 150, "🍰", 15),
    ("Cheesecake", "Desserts", "Creamy classic cheesecake.", 420, 170, "🍰", 15),
    ("Brownie", "Desserts", "Warm chocolate brownie.", 300, 110, "🍫", 20),

    ("Chicken Sandwich", "Snacks", "Grilled chicken sandwich.", 550, 250, "🥪", 20),
    ("French Fries", "Snacks", "Crispy golden fries.", 280, 100, "🍟", 30),
    ("Chicken Wrap", "Snacks", "Fresh chicken wrap.", 520, 220, "🌯", 20),

    ("Fresh Lemonade", "Cold Drinks", "Freshly prepared lemonade.", 250, 90, "🍋", 30),
    ("Iced Tea", "Cold Drinks", "Refreshing chilled iced tea.", 260, 90, "🧊", 30),
    ("Strawberry Cooler", "Cold Drinks", "Sweet strawberry cooler.", 350, 130, "🍓", 25)
]

# =========================================================
# DATABASE SETUP / MIGRATION
# =========================================================

def sqlite_has_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name IN ('products', 'orders', 'settings')
        """)

        tables = {row[0] for row in cur.fetchall()}

        if "products" not in tables:
            conn.close()
            return False

        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM orders")
        order_count = 0

        if "orders" in tables:
            order_count = cur.fetchone()[0]

        conn.close()

        return product_count > 0 or order_count > 0

    except Exception:
        return False


def migrate_sqlite_to_supabase():
    """
    One-time safety migration.

    If the old SQLite database exists and Supabase is empty,
    copy old products, orders and settings to Supabase.
    """

    try:
        existing_products = supabase.table("products").select(
            "id"
        ).limit(1).execute()

        existing_orders = supabase.table("orders").select(
            "id"
        ).limit(1).execute()

        supabase_has_products = bool(existing_products.data)
        supabase_has_orders = bool(existing_orders.data)

        if supabase_has_products or supabase_has_orders:
            return

        if not sqlite_has_data():
            return

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # -------------------------------------------------
        # PRODUCTS
        # -------------------------------------------------

        try:
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()

            product_data = []

            for row in rows:
                product_data.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "category": row["category"],
                    "description": row["description"],
                    "price": float(row["price"]),
                    "cost": float(row["cost"]),
                    "icon": row["icon"],
                    "stock": int(row["stock"]),
                    "available": bool(row["available"])
                })

            if product_data:
                supabase.table("products").upsert(
                    product_data
                ).execute()

        except Exception:
            pass

        # -------------------------------------------------
        # ORDERS
        # -------------------------------------------------

        try:
            cur.execute("SELECT * FROM orders")
            rows = cur.fetchall()

            order_data = []

            for row in rows:
                order_data.append({
                    "id": int(row["id"]),
                    "order_code": row["order_code"],
                    "customer_name": row["customer_name"],
                    "phone": row["phone"],
                    "address": row["address"],
                    "items": row["items"],
                    "subtotal": float(row["subtotal"]),
                    "tax": float(row["tax"]),
                    "delivery_fee": float(row["delivery_fee"]),
                    "total": float(row["total"]),
                    "profit": float(row["profit"]),
                    "status": row["status"],
                    "payment_method": row["payment_method"],
                    "created_at": row["created_at"]
                })

            if order_data:
                supabase.table("orders").upsert(
                    order_data
                ).execute()

        except Exception:
            pass

        # -------------------------------------------------
        # SETTINGS
        # -------------------------------------------------

        try:
            cur.execute("SELECT * FROM settings")
            rows = cur.fetchall()

            settings_data = []

            for row in rows:
                settings_data.append({
                    "key": row["key"],
                    "value": str(row["value"])
                })

            if settings_data:
                supabase.table("settings").upsert(
                    settings_data
                ).execute()

        except Exception:
            pass

        conn.close()

    except Exception:
        pass


def initialize_supabase():
    try:
        # Check if products already exist
        result = supabase.table("products").select(
            "id"
        ).limit(1).execute()

        if result.data:
            return

        # First try to preserve old SQLite data
        migrate_sqlite_to_supabase()

        # Check again after migration
        result = supabase.table("products").select(
            "id"
        ).limit(1).execute()

        if result.data:
            return

        # -------------------------------------------------
        # Insert default menu
        # -------------------------------------------------

        product_data = []

        for product in DEFAULT_PRODUCTS:
            product_data.append({
                "name": product[0],
                "category": product[1],
                "description": product[2],
                "price": product[3],
                "cost": product[4],
                "icon": product[5],
                "stock": product[6],
                "available": True
            })

        supabase.table("products").insert(
            product_data
        ).execute()

        # -------------------------------------------------
        # Default settings
        # -------------------------------------------------

        settings = [
            {"key": "tax_rate", "value": "5"},
            {"key": "delivery_fee", "value": "150"},
            {"key": "cafe_status", "value": "Open"}
        ]

        supabase.table("settings").upsert(
            settings
        ).execute()

    except Exception as e:
        st.error(
            "Database connection error. "
            "Please check your Supabase settings."
        )
        st.code(str(e))
        st.stop()


initialize_supabase()

# =========================================================
# DATABASE HELPERS
# =========================================================

def get_setting(key):
    try:
        result = (
            supabase
            .table("settings")
            .select("value")
            .eq("key", key)
            .limit(1)
            .execute()
        )

        if result.data:
            return result.data[0]["value"]

    except Exception:
        pass

    return None


def set_setting(key, value):
    supabase.table("settings").upsert({
        "key": key,
        "value": str(value)
    }).execute()


def get_products(available_only=False):
    query = supabase.table("products").select("*")

    if available_only:
        query = query.eq(
            "available",
            True
        ).gt(
            "stock",
            0
        )

    result = query.execute()

    data = result.data or []

    if not data:
        return pd.DataFrame(
            columns=[
                "id",
                "name",
                "category",
                "description",
                "price",
                "cost",
                "icon",
                "stock",
                "available"
            ]
        )

    df = pd.DataFrame(data)

    return df.sort_values(
        ["category", "name"]
    ).reset_index(drop=True)


def get_orders():
    result = (
        supabase
        .table("orders")
        .select("*")
        .order("id", desc=True)
        .execute()
    )

    data = result.data or []

    if not data:
        return pd.DataFrame(
            columns=[
                "id",
                "order_code",
                "customer_name",
                "phone",
                "address",
                "items",
                "subtotal",
                "tax",
                "delivery_fee",
                "total",
                "profit",
                "status",
                "payment_method",
                "created_at"
            ]
        )

    return pd.DataFrame(data)


def generate_order_code():
    result = (
        supabase
        .table("orders")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    if result.data:
        next_id = int(result.data[0]["id"]) + 1
    else:
        next_id = 1

    return f"CWU-{next_id:04d}"


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "last_order" not in st.session_state:
    st.session_state.last_order = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ☕ Coffee With Us")
    st.caption("Fresh coffee. Fresh moments.")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Order",
            "🛒 Cart",
            "📦 Track Order"
        ]
    )

    st.divider()

    with st.expander("Staff"):

        admin_password = st.text_input(
            "Admin Password",
            type="password",
            key="admin_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if hash_password(admin_password) == hash_password(
                ADMIN_PASSWORD
            ):

                st.session_state.admin_logged_in = True

                st.success(
                    "Admin access granted."
                )

                st.rerun()

            else:

                st.error(
                    "Incorrect password."
                )

        if st.session_state.admin_logged_in:

            st.success(
                "Admin logged in"
            )

            if st.button(
                "Open Admin Dashboard",
                use_container_width=True
            ):

                st.session_state.page_override = "admin"
                st.rerun()

            if st.button(
                "Logout Admin",
                use_container_width=True
            ):

                st.session_state.admin_logged_in = False
                st.session_state.page_override = None
                st.rerun()


# =========================================================
# ADMIN ROUTING
# =========================================================

if st.session_state.get("page_override") == "admin":

    if not st.session_state.admin_logged_in:

        st.error(
            "Unauthorized access."
        )

        st.stop()

    st.markdown("""
    <div class="hero">
        <h1>🔐 Admin Dashboard</h1>
        <p>Coffee With Us management center</p>
    </div>
    """, unsafe_allow_html=True)

    admin_tab = st.tabs([
        "📊 Dashboard",
        "📦 Orders",
        "🍔 Products",
        "📋 Inventory",
        "👥 Customers",
        "⚙️ Settings"
    ])

    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    with admin_tab[0]:

        orders_df = get_orders()

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        if not orders_df.empty:

            orders_df["created_at"] = (
                orders_df["created_at"].astype(str)
            )

            today_orders = orders_df[
                orders_df["created_at"].str.startswith(
                    today
                )
            ]

            active_today = today_orders[
                today_orders["status"] != "Cancelled"
            ]

            revenue = active_today["total"].sum()
            profit = active_today["profit"].sum()
            order_count = len(active_today)

        else:

            revenue = 0
            profit = 0
            order_count = 0

        products_df = get_products()

        low_stock = len(
            products_df[
                products_df["stock"] <= 5
            ]
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">
                        Rs. {revenue:,.0f}
                    </div>
                    <div class="metric-label">
                        Today's Revenue
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">
                        Rs. {profit:,.0f}
                    </div>
                    <div class="metric-label">
                        Today's Profit
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">
                        {order_count}
                    </div>
                    <div class="metric-label">
                        Today's Orders
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">
                        {low_stock}
                    </div>
                    <div class="metric-label">
                        Low Stock Items
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        if not orders_df.empty:

            active_orders = orders_df[
                orders_df["status"] != "Cancelled"
            ].copy()

            if not active_orders.empty:

                active_orders["date"] = (
                    pd.to_datetime(
                        active_orders["created_at"]
                    ).dt.date
                )

                revenue_chart = (
                    active_orders
                    .groupby("date")["total"]
                    .sum()
                    .reset_index()
                )

                st.subheader(
                    "📈 Revenue Overview"
                )

                fig = px.line(
                    revenue_chart,
                    x="date",
                    y="total",
                    markers=True,
                    labels={
                        "date": "Date",
                        "total": "Revenue (Rs.)"
                    }
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # -------------------------------------------------
            # BEST SELLERS
            # -------------------------------------------------

            st.subheader(
                "🏆 Best Selling Products"
            )

            sales = {}

            for _, order in orders_df.iterrows():

                if order["status"] == "Cancelled":
                    continue

                items = str(
                    order["items"]
                ).split("|||")

                for item in items:

                    if not item:
                        continue

                    parts = item.split("::")

                    if len(parts) >= 3:

                        name = parts[0]
                        quantity = int(parts[2])

                        sales[name] = (
                            sales.get(name, 0)
                            + quantity
                        )

            if sales:

                best_df = pd.DataFrame(
                    list(sales.items()),
                    columns=[
                        "Product",
                        "Quantity"
                    ]
                ).sort_values(
                    "Quantity",
                    ascending=False
                ).head(10)

                st.dataframe(
                    best_df,
                    use_container_width=True,
                    hide_index=True
                )

    # =====================================================
    # ADMIN ORDERS
    # =====================================================

    with admin_tab[1]:

        st.subheader(
            "📦 Order Management"
        )

        orders_df = get_orders()

        if orders_df.empty:

            st.info(
                "No orders yet."
            )

        else:

            status_filter = st.selectbox(
                "Filter Orders",
                [
                    "All",
                    "Received",
                    "Preparing",
                    "In the Oven",
                    "Ready",
                    "Delivered",
                    "Cancelled"
                ]
            )

            filtered = orders_df.copy()

            if status_filter != "All":

                filtered = filtered[
                    filtered["status"] ==
                    status_filter
                ]

            for _, order in filtered.iterrows():

                with st.container():

                    st.markdown(
                        f"""
                        <div class="order-box">
                            <h3>
                                🧾 {order['order_code']}
                            </h3>

                            <b>Customer:</b>
                            {order['customer_name']}<br>

                            <b>Phone:</b>
                            {order['phone'] or 'Not provided'}<br>

                            <b>Order Time:</b>
                            {order['created_at']}<br>

                            <b>Total:</b>
                            Rs. {float(order['total']):,.0f}<br>

                            <b>Current Status:</b>
                            {order['status']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        "**Items:**"
                    )

                    item_rows = []

                    for item in str(
                        order["items"]
                    ).split("|||"):

                        if not item:
                            continue

                        parts = item.split("::")

                        if len(parts) >= 4:

                            item_rows.append({
                                "Product": parts[0],
                                "Price": float(parts[1]),
                                "Quantity": int(parts[2]),
                                "Total": float(parts[3])
                            })

                    if item_rows:

                        st.dataframe(
                            pd.DataFrame(item_rows),
                            use_container_width=True,
                            hide_index=True
                        )

                    col1, col2 = st.columns(
                        [2, 1]
                    )

                    statuses = [
                        "Received",
                        "Preparing",
                        "In the Oven",
                        "Ready",
                        "Delivered",
                        "Cancelled"
                    ]

                    with col1:

                        new_status = st.selectbox(
                            "Change Status",
                            statuses,
                            index=statuses.index(
                                order["status"]
                            ),
                            key=f"status_{order['id']}"
                        )

                    with col2:

                        if st.button(
                            "Update",
                            key=f"update_{order['id']}",
                            use_container_width=True
                        ):

                            supabase.table(
                                "orders"
                            ).update({
                                "status": new_status
                            }).eq(
                                "id",
                                int(order["id"])
                            ).execute()

                            st.success(
                                "Order updated."
                            )

                            st.rerun()

                    st.divider()

    # =====================================================
    # ADMIN PRODUCTS
    # =====================================================

    with admin_tab[2]:

        st.subheader(
            "🍔 Product Management"
        )

        product_df = get_products()

        if not product_df.empty:

            st.dataframe(
                product_df[
                    [
                        "id",
                        "name",
                        "category",
                        "price",
                        "cost",
                        "stock",
                        "available"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        action = st.radio(
            "Product Action",
            [
                "Add Product",
                "Edit Product",
                "Delete Product"
            ],
            horizontal=True
        )

        # -------------------------------------------------
        # ADD PRODUCT
        # -------------------------------------------------

        if action == "Add Product":

            with st.form("add_product"):

                name = st.text_input(
                    "Product Name"
                )

                category = st.selectbox(
                    "Category",
                    [
                        "Coffee",
                        "Frappes",
                        "Matcha",
                        "Cookies",
                        "Desserts",
                        "Snacks",
                        "Cold Drinks",
                        "Other"
                    ]
                )

                description = st.text_area(
                    "Description"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    price = st.number_input(
                        "Selling Price",
                        min_value=0.0,
                        value=300.0
                    )

                with col2:

                    cost = st.number_input(
                        "Cost Price",
                        min_value=0.0,
                        value=100.0
                    )

                with col3:

                    stock = st.number_input(
                        "Initial Stock",
                        min_value=0,
                        value=20
                    )

                icon = st.text_input(
                    "Emoji",
                    value="☕"
                )

                submitted = st.form_submit_button(
                    "Add Product"
                )

                if submitted:

                    if not name.strip():

                        st.error(
                            "Enter a product name."
                        )

                    else:

                        supabase.table(
                            "products"
                        ).insert({
                            "name": name,
                            "category": category,
                            "description": description,
                            "price": price,
                            "cost": cost,
                            "icon": icon,
                            "stock": stock,
                            "available": True
                        }).execute()

                        st.success(
                            "Product added successfully."
                        )

                        st.rerun()

        # -------------------------------------------------
        # EDIT PRODUCT
        # -------------------------------------------------

        elif action == "Edit Product":

            if product_df.empty:

                st.info(
                    "No products available."
                )

            else:

                selected_id = st.selectbox(
                    "Select Product",
                    product_df["id"].tolist(),
                    format_func=lambda x:
                    product_df[
                        product_df["id"] == x
                    ]["name"].iloc[0]
                )

                product = product_df[
                    product_df["id"] ==
                    selected_id
                ].iloc[0]

                with st.form("edit_product"):

                    new_name = st.text_input(
                        "Name",
                        value=product["name"]
                    )

                    new_category = st.text_input(
                        "Category",
                        value=product["category"]
                    )

                    new_description = st.text_area(
                        "Description",
                        value=product["description"] or ""
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        new_price = st.number_input(
                            "Selling Price",
                            value=float(
                                product["price"]
                            )
                        )

                    with col2:

                        new_cost = st.number_input(
                            "Cost Price",
                            value=float(
                                product["cost"]
                            )
                        )

                    with col3:

                        new_stock = st.number_input(
                            "Stock",
                            min_value=0,
                            value=int(
                                product["stock"]
                            )
                        )

                    new_icon = st.text_input(
                        "Emoji",
                        value=product["icon"] or "☕"
                    )

                    new_available = st.checkbox(
                        "Available",
                        value=bool(
                            product["available"]
                        )
                    )

                    save = st.form_submit_button(
                        "Save Changes"
                    )

                    if save:

                        supabase.table(
                            "products"
                        ).update({
                            "name": new_name,
                            "category": new_category,
                            "description": new_description,
                            "price": new_price,
                            "cost": new_cost,
                            "icon": new_icon,
                            "stock": new_stock,
                            "available": new_available
                        }).eq(
                            "id",
                            int(selected_id)
                        ).execute()

                        st.success(
                            "Product updated."
                        )

                        st.rerun()

        # -------------------------------------------------
        # DELETE PRODUCT
        # -------------------------------------------------

        else:

            if product_df.empty:

                st.info(
                    "No products available."
                )

            else:

                selected_id = st.selectbox(
                    "Product to Delete",
                    product_df["id"].tolist(),
                    format_func=lambda x:
                    product_df[
                        product_df["id"] == x
                    ]["name"].iloc[0],
                    key="delete_product"
                )

                confirm = st.checkbox(
                    "I understand this will permanently delete the product."
                )

                if st.button(
                    "Delete Product"
                ):

                    if not confirm:

                        st.warning(
                            "Please confirm deletion first."
                        )

                    else:

                        supabase.table(
                            "products"
                        ).delete().eq(
                            "id",
                            int(selected_id)
                        ).execute()

                        st.success(
                            "Product deleted."
                        )

                        st.rerun()

    # =====================================================
    # INVENTORY
    # =====================================================

    with admin_tab[3]:

        st.subheader(
            "📋 Inventory"
        )

        inventory = get_products()

        if not inventory.empty:

            display_inventory = inventory[
                [
                    "name",
                    "category",
                    "stock",
                    "price",
                    "cost",
                    "available"
                ]
            ].copy()

            display_inventory[
                "Stock Status"
            ] = display_inventory[
                "stock"
            ].apply(
                lambda x:
                "🔴 Out of Stock"
                if x <= 0
                else
                "🟠 Low Stock"
                if x <= 5
                else
                "🟢 In Stock"
            )

            st.dataframe(
                display_inventory,
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "⚠️ Low Stock"
            )

            low = inventory[
                inventory["stock"] <= 5
            ]

            if low.empty:

                st.success(
                    "All products have healthy stock."
                )

            else:

                st.warning(
                    f"{len(low)} product(s) need attention."
                )

                st.dataframe(
                    low[
                        [
                            "name",
                            "category",
                            "stock"
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

    # =====================================================
    # CUSTOMERS
    # =====================================================

    with admin_tab[4]:

        st.subheader(
            "👥 Customers"
        )

        orders = get_orders()

        if orders.empty:

            st.info(
                "No customers yet."
            )

        else:

            customers = (
                orders[
                    orders["status"] != "Cancelled"
                ]
                .groupby(
                    [
                        "customer_name",
                        "phone"
                    ]
                )
                .agg(
                    Orders=("id", "count"),
                    Total_Spent=("total", "sum")
                )
                .reset_index()
                .sort_values(
                    "Total_Spent",
                    ascending=False
                )
            )

            customers[
                "Total_Spent"
            ] = customers[
                "Total_Spent"
            ].round(2)

            st.dataframe(
                customers,
                use_container_width=True,
                hide_index=True
            )

    # =====================================================
    # SETTINGS
    # =====================================================

    with admin_tab[5]:

        st.subheader(
            "⚙️ Café Settings"
        )

        tax_rate = float(
            get_setting("tax_rate") or 5
        )

        delivery_fee = float(
            get_setting("delivery_fee") or 150
        )

        cafe_status = (
            get_setting("cafe_status")
            or "Open"
        )

        with st.form("settings_form"):

            new_tax = st.number_input(
                "Tax Rate (%)",
                min_value=0.0,
                value=tax_rate
            )

            new_delivery = st.number_input(
                "Delivery Fee (Rs.)",
                min_value=0.0,
                value=delivery_fee
            )

            new_status = st.selectbox(
                "Café Status",
                [
                    "Open",
                    "Closed",
                    "Busy"
                ],
                index=[
                    "Open",
                    "Closed",
                    "Busy"
                ].index(cafe_status)
            )

            save_settings = st.form_submit_button(
                "Save Settings"
            )

            if save_settings:

                set_setting(
                    "tax_rate",
                    new_tax
                )

                set_setting(
                    "delivery_fee",
                    new_delivery
                )

                set_setting(
                    "cafe_status",
                    new_status
                )

                st.success(
                    "Settings saved successfully."
                )

                st.rerun()

        st.divider()

        st.subheader(
            "🔑 Admin Security"
        )

        st.warning(
            "The current demo password is 123456. "
            "Change ADMIN_PASSWORD in app.py before "
            "using this publicly."
        )

    st.stop()


# =========================================================
# CUSTOMER HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <h1>☕ Coffee With Us</h1>
    <p>Your coffee. Your moment. Your way.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# ORDER PAGE
# =========================================================

if page == "🏠 Order":

    cafe_status = (
        get_setting("cafe_status")
        or "Open"
    )

    if cafe_status == "Closed":

        st.error(
            "🔴 The café is currently closed. "
            "Please come back later."
        )

    elif cafe_status == "Busy":

        st.warning(
            "🟠 We're currently busy. "
            "Orders may take a little longer."
        )

    st.subheader(
        "🍽️ Our Menu"
    )

    search = st.text_input(
        "🔎 Search the menu",
        placeholder="Search coffee, frappe, cookie..."
    )

    products = get_products(
        available_only=True
    )

    if search:

        products = products[
            products["name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            products["category"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    categories = [
        "All",
        "Coffee",
        "Frappes",
        "Matcha",
        "Cookies",
        "Desserts",
        "Snacks",
        "Cold Drinks"
    ]

    selected_category = st.selectbox(
        "Category",
        categories
    )

    if selected_category != "All":

        products = products[
            products["category"] ==
            selected_category
        ]

    if products.empty:

        st.info(
            "No products found."
        )

    else:

        grouped = products.groupby(
            "category"
        )

        for category, category_products in grouped:

            st.markdown(
                f"""
                <div class="category-title">
                    {category}
                </div>
                """,
                unsafe_allow_html=True
            )

            cols = st.columns(3)

            for index, (_, product) in enumerate(
                category_products.iterrows()
            ):

                with cols[index % 3]:

                    st.markdown(
                        f"""
                        <div class="product-card">
                            <div class="product-icon">
                                {product['icon']}
                            </div>

                            <h3>
                                {product['name']}
                            </h3>

                            <p>
                                {product['description']}
                            </p>

                            <div class="price">
                                Rs. {float(product['price']):,.0f}
                            </div>

                            <p class="small-text">
                                {int(product['stock'])} available
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=min(
                            int(product["stock"]),
                            20
                        ),
                        value=1,
                        key=f"qty_{product['id']}"
                    )

                    if st.button(
                        f"Add {product['name']}",
                        key=f"add_{product['id']}",
                        use_container_width=True
                    ):

                        product_id = int(
                            product["id"]
                        )

                        current_quantity = (
                            st.session_state.cart.get(
                                product_id,
                                {}
                            ).get(
                                "quantity",
                                0
                            )
                        )

                        if (
                            current_quantity +
                            quantity
                        ) > int(product["stock"]):

                            st.error(
                                "You cannot add more than "
                                "the available stock."
                            )

                        else:

                            if product_id in st.session_state.cart:

                                st.session_state.cart[
                                    product_id
                                ]["quantity"] += quantity

                            else:

                                st.session_state.cart[
                                    product_id
                                ] = {
                                    "id": product_id,
                                    "name": product["name"],
                                    "price": float(
                                        product["price"]
                                    ),
                                    "cost": float(
                                        product["cost"]
                                    ),
                                    "quantity": quantity,
                                    "icon": product["icon"]
                                }

                            st.success(
                                f"{quantity} × "
                                f"{product['name']} added!"
                            )


# =========================================================
# CART
# =========================================================

elif page == "🛒 Cart":

    st.subheader(
        "🛒 Your Cart"
    )

    if not st.session_state.cart:

        st.info(
            "Your cart is empty. "
            "Go to the Order page to add something delicious."
        )

    else:

        subtotal = 0
        estimated_cost = 0

        for product_id in list(
            st.session_state.cart.keys()
        ):

            item = st.session_state.cart[
                product_id
            ]

            item_total = (
                item["price"] *
                item["quantity"]
            )

            subtotal += item_total

            estimated_cost += (
                item["cost"] *
                item["quantity"]
            )

            st.markdown(
                f"""
                <div class="order-box">
                    <h3>
                        {item['icon']} {item['name']}
                    </h3>

                    <p>
                        Rs. {item['price']:,.0f}
                        × {item['quantity']}
                        =
                        <b>
                            Rs. {item_total:,.0f}
                        </b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=50,
                    value=item["quantity"],
                    key=f"cart_qty_{product_id}"
                )

            with col2:

                if st.button(
                    "Update",
                    key=f"update_cart_{product_id}"
                ):

                    st.session_state.cart[
                        product_id
                    ]["quantity"] = new_quantity

                    st.rerun()

            with col3:

                if st.button(
                    "Remove",
                    key=f"remove_{product_id}"
                ):

                    del st.session_state.cart[
                        product_id
                    ]

                    st.rerun()

        st.divider()

        tax_rate = float(
            get_setting("tax_rate") or 5
        )

        delivery_fee = float(
            get_setting("delivery_fee") or 150
        )

        tax = subtotal * (
            tax_rate / 100
        )

        total = (
            subtotal +
            tax +
            delivery_fee
        )

        st.markdown(
            "### 💰 Order Summary"
        )

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            st.write(
                f"Subtotal: "
                f"**Rs. {subtotal:,.0f}**"
            )

            st.write(
                f"Tax ({tax_rate:.0f}%): "
                f"**Rs. {tax:,.0f}**"
            )

            st.write(
                f"Delivery Fee: "
                f"**Rs. {delivery_fee:,.0f}**"
            )

        with summary_col2:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">
                        TOTAL
                    </div>

                    <div class="metric-value">
                        Rs. {total:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.subheader(
            "👤 Customer Information"
        )

        customer_name = st.text_input(
            "Full Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        address = st.text_area(
            "Delivery Address"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash on Delivery",
                "Pay at Café"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🗑️ Cancel Order",
                use_container_width=True
            ):

                st.session_state.cart = {}

                st.warning(
                    "Your cart has been cleared."
                )

                st.rerun()

        with col2:

            checkout = st.button(
                "✅ Checkout",
                use_container_width=True,
                type="primary"
            )

            if checkout:

                if not customer_name.strip():

                    st.error(
                        "Please enter your name."
                    )

                elif not phone.strip():

                    st.error(
                        "Please enter your phone number."
                    )

                elif not address.strip():

                    st.error(
                        "Please enter your address."
                    )

                else:

                    # -------------------------------------------------
                    # CHECK STOCK
                    # -------------------------------------------------

                    stock_problem = False

                    for product_id, item in (
                        st.session_state.cart.items()
                    ):

                        result = (
                            supabase
                            .table("products")
                            .select("stock")
                            .eq(
                                "id",
                                int(product_id)
                            )
                            .limit(1)
                            .execute()
                        )

                        if not result.data:

                            stock_problem = True

                            st.error(
                                f"{item['name']} is no longer available."
                            )

                            continue

                        current_stock = int(
                            result.data[0]["stock"]
                        )

                        if current_stock < item["quantity"]:

                            stock_problem = True

                            st.error(
                                f"Not enough stock for "
                                f"{item['name']}."
                            )

                    if not stock_problem:

                        # -------------------------------------------------
                        # ORDER CODE
                        # -------------------------------------------------

                        order_code = generate_order_code()

                        item_strings = []

                        for item in (
                            st.session_state.cart.values()
                        ):

                            item_strings.append(
                                "::".join([
                                    item["name"],
                                    str(item["price"]),
                                    str(item["quantity"]),
                                    str(
                                        item["price"] *
                                        item["quantity"]
                                    )
                                ])
                            )

                        items_string = "|||".join(
                            item_strings
                        )

                        profit = (
                            subtotal -
                            estimated_cost
                        )

                        created_at = (
                            datetime.now()
                            .strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        )

                        # -------------------------------------------------
                        # CREATE ORDER
                        # -------------------------------------------------

                        order_result = (
                            supabase
                            .table("orders")
                            .insert({
                                "order_code": order_code,
                                "customer_name": customer_name,
                                "phone": phone,
                                "address": address,
                                "items": items_string,
                                "subtotal": subtotal,
                                "tax": tax,
                                "delivery_fee": delivery_fee,
                                "total": total,
                                "profit": profit,
                                "status": "Received",
                                "payment_method": payment_method,
                                "created_at": created_at
                            })
                            .execute()
                        )

                        if not order_result.data:

                            st.error(
                                "The order could not be saved. "
                                "Please try again."
                            )

                        else:

                            # -------------------------------------------------
                            # DECREASE STOCK
                            # -------------------------------------------------

                            for product_id, item in (
                                st.session_state.cart.items()
                            ):

                                result = (
                                    supabase
                                    .table("products")
                                    .select("stock")
                                    .eq(
                                        "id",
                                        int(product_id)
                                    )
                                    .limit(1)
                                    .execute()
                                )

                                if result.data:

                                    current_stock = int(
                                        result.data[0]["stock"]
                                    )

                                    new_stock = (
                                        current_stock -
                                        item["quantity"]
                                    )

                                    supabase.table(
                                        "products"
                                    ).update({
                                        "stock": new_stock
                                    }).eq(
                                        "id",
                                        int(product_id)
                                    ).execute()

                            st.session_state.last_order = (
                                order_code
                            )

                            st.session_state.cart = {}

                            st.success(
                                "🎉 Your order has been placed!"
                            )

                            st.markdown(
                                f"""
                                <div class="receipt">
                                    <h2>
                                        ☕ Coffee With Us
                                    </h2>

                                    <h3>
                                        Order Confirmed
                                    </h3>

                                    <p>
                                        Your Order ID is:
                                    </p>

                                    <h1>
                                        {order_code}
                                    </h1>

                                    <p>
                                        Please save this Order ID
                                        to track your order.
                                    </p>

                                    <h2>
                                        Total:
                                        Rs. {total:,.0f}
                                    </h2>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


# =========================================================
# TRACK ORDER
# =========================================================

elif page == "📦 Track Order":

    st.subheader(
        "📦 Track Your Order"
    )

    if st.session_state.last_order:

        st.info(
            f"Your latest order is "
            f"**{st.session_state.last_order}**"
        )

    order_code = st.text_input(
        "Enter your Order ID",
        placeholder="Example: CWU-0001"
    ).strip().upper()

    if st.button(
        "🔎 Track Order",
        type="primary",
        use_container_width=True
    ):

        if not order_code:

            st.warning(
                "Please enter an Order ID."
            )

        else:

            result = (
                supabase
                .table("orders")
                .select("*")
                .eq(
                    "order_code",
                    order_code
                )
                .limit(1)
                .execute()
            )

            if not result.data:

                st.error(
                    "❌ Order not found. "
                    "Please check your Order ID."
                )

            else:

                order_data = result.data[0]

                # =================================================
                # INVOICE HEADER
                # =================================================

                st.markdown(
                    "## ☕ Coffee With Us"
                )

                st.markdown(
                    f"### 🧾 Order "
                    f"{order_data['order_code']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Customer**"
                    )

                    st.write(
                        order_data["customer_name"]
                    )

                with col2:

                    st.write(
                        "**Order Time**"
                    )

                    st.write(
                        order_data["created_at"]
                    )

                st.divider()

                # =================================================
                # ORDER STATUS
                # =================================================

                st.markdown(
                    "### 📦 Order Status"
                )

                current_status = (
                    order_data["status"]
                )

                if current_status == "Received":

                    st.info(
                        "🟡 Order Received"
                    )

                elif current_status == "Preparing":

                    st.info(
                        "👨‍🍳 Preparing Your Order"
                    )

                elif current_status == "In the Oven":

                    st.info(
                        "🔥 Your Order Is In The Oven"
                    )

                elif current_status == "Ready":

                    st.success(
                        "🟢 Your Order Is Ready"
                    )

                elif current_status == "Delivered":

                    st.success(
                        "✅ Order Delivered"
                    )

                elif current_status == "Cancelled":

                    st.error(
                        "❌ Order Cancelled"
                    )

                # =================================================
                # ORDER PROGRESS
                # =================================================

                if current_status != "Cancelled":

                    statuses = [
                        "Received",
                        "Preparing",
                        "In the Oven",
                        "Ready",
                        "Delivered"
                    ]

                    current_index = statuses.index(
                        current_status
                    )

                    st.markdown(
                        "### 🚚 Order Progress"
                    )

                    progress_cols = st.columns(
                        len(statuses)
                    )

                    for i, step in enumerate(
                        statuses
                    ):

                        with progress_cols[i]:

                            if i < current_index:

                                st.success(
                                    f"✓ {step}"
                                )

                            elif i == current_index:

                                st.info(
                                    f"● {step}"
                                )

                            else:

                                st.write(
                                    f"○ {step}"
                                )

                st.divider()

                # =================================================
                # INVOICE ITEMS
                # =================================================

                st.markdown(
                    "### 🧾 Invoice"
                )

                item_rows = []

                for item in str(
                    order_data["items"]
                ).split("|||"):

                    if not item:
                        continue

                    parts = item.split("::")

                    if len(parts) >= 4:

                        item_rows.append({
                            "Item": parts[0],
                            "Price": (
                                f"Rs. "
                                f"{float(parts[1]):,.0f}"
                            ),
                            "Quantity": int(parts[2]),
                            "Total": (
                                f"Rs. "
                                f"{float(parts[3]):,.0f}"
                            )
                        })

                if item_rows:

                    st.dataframe(
                        pd.DataFrame(item_rows),
                        use_container_width=True,
                        hide_index=True
                    )

                st.divider()

                # =================================================
                # BILL SUMMARY
                # =================================================

                st.markdown(
                    "### 💰 Bill Summary"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Subtotal:** "
                        f"Rs. {float(order_data['subtotal']):,.0f}"
                    )

                    st.write(
                        f"**Tax:** "
                        f"Rs. {float(order_data['tax']):,.0f}"
                    )

                    st.write(
                        f"**Delivery:** "
                        f"Rs. {float(order_data['delivery_fee']):,.0f}"
                    )

                    st.write(
                        f"**Payment Method:** "
                        f"{order_data['payment_method']}"
                    )

                with col2:

                    st.metric(
                        "TOTAL",
                        f"Rs. {float(order_data['total']):,.0f}"
                    )

                st.divider()

                # =================================================
                # CUSTOMER MESSAGE
                # =================================================

                if current_status == "Delivered":

                    st.success(
                        "🎉 Thank you for ordering from "
                        "Coffee With Us!"
                    )

                elif current_status == "Cancelled":

                    st.error(
                        "This order has been cancelled."
                    )

                else:

                    st.info(
                        f"☕ Your order "
                        f"{order_data['order_code']} "
                        f"is being prepared by our team."
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        ☕ <b>Coffee With Us</b><br>
        Fresh coffee • Fresh moments • Fresh memories
    </div>
    """,
    unsafe_allow_html=True
)

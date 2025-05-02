# 💻 PCGeek – Custom PC Build & E-Commerce Platform

PCGeek is a comprehensive e-commerce platform tailored for tech enthusiasts looking to buy gaming/office laptops, accessories, and even build custom PCs with Intel or AMD components. Built with Django, PCGeek offers a seamless shopping experience with dynamic product categories, cart functionality, and a customizable build tool.

---

## 🚀 Features

- 🖥️ **Custom PC Builder**
  - Separate build pages for **Intel** and **AMD Ryzen**
  - Category-wise selection (Processor, GPU, RAM, etc.)
  - Real-time selection update and cart integration

- 🛒 **E-commerce Storefront**
  - Product listings by category
  - Add to Cart functionality
  - Cart summary and total calculation

- 🔐 **User Authentication**
  - Login, Logout, Registration
  - Redirect to login when accessing protected pages (like cart)

- 📦 **Admin Dashboard**
  - Manage products, categories, and orders

- 🎨 **Responsive Frontend**
  - Clean UI using HTML, CSS, and JavaScript
  - Interactive dropdowns, confirmation pop-ups, and dynamic content loading

---

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Tools**: Git, Trello, GitHub

---


## ⚙️ Installation & Setup

1. Clone the Repository
```bash
git clone https://github.com/nischal-0016/Django_ecommerce.git
cd pcgeek
```

2. Set up a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate. On mac, use `source env/bin/activate

```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Apply Migrations
```bash
py manage.py makemigrations
py manage.py migrate
```

5. Create a Superuser 
``` bash
py manage.py createsuperuser
```

6. Run the Development Server
```bash
py manage.py runserver
```

7. Access the Site 
```bash
Open your browser and navigate to http://127.0.0.1:8000/.
```
🔐 Admin Panel Access
After creating a superuser, you can access the Django admin panel at:

```bash
http://127.0.0.1:8000/admin/

```
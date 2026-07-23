# Bio Leaf Exports — Website

A full website for Bio Leaf Exports, built with a Python (Flask) backend and
Jinja2 templates. Includes a live product catalogue, product detail pages,
and a working contact form that saves enquiries to `data/contacts.json`.

## Pages included

- **Home** (`/`) — hero, product highlights, industries, process, why-us
- **Products** (`/products`) — full catalogue with search + industry filter
- **Product Detail** (`/products/<slug>`) — specs, forms, related botanicals
- **About** (`/about`) — company story, values, founder quote
- **Quality** (`/quality`) — QA process and certifications
- **Manufacturing** (`/manufacturing`) — facility and capacity
- **Sustainability** (`/sustainability`) — sourcing practices
- **Contact** (`/contact`) — working enquiry form

## Requirements

- Python 3.9 or newer

## Setup & run locally

```bash
# 1. Unzip and enter the folder
cd bioleaf_site

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## How the contact form works

Submissions are validated (name, email, and message are required) and
appended to `data/contacts.json` as a simple JSON list — no database setup
needed to get started. You can later swap this for a real database or wire
it up to send you an email by editing the `contact()` view in `app.py`.

## Editing your product catalogue

All product data lives in the `PRODUCTS` list near the top of `app.py` —
add, remove, or edit botanicals there (name, specs, forms, industries) and
the Products page, product detail pages, and homepage all update
automatically.

## Project structure

```
bioleaf_site/
├── app.py                  # Flask application & routes
├── requirements.txt
├── data/
│   └── contacts.json       # created automatically on first form submit
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/logo.png
└── templates/
    ├── base.html            # shared nav + footer
    ├── index.html
    ├── products.html
    ├── product_detail.html
    ├── about.html
    ├── quality.html
    ├── manufacturing.html
    ├── sustainability.html
    ├── contact.html
    └── 404.html
```

## Going to production

For production, don't use `app.run(debug=True)`. Use a WSGI server such as
gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

And set a real `app.secret_key` via an environment variable instead of the
placeholder in `app.py`.

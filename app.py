"""
Bio Leaf Exports — Flask backend
Run with:  python app.py
Visit:     http://127.0.0.1:5000
"""

import json
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "bioleaf-dev-secret-key-change-in-production"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Product catalogue (in a real deployment this would live in a database)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "amla",
        "index": "01",
        "latin": "Phyllanthus emblica",
        "common": "Amla",
        "tagline": "Indian gooseberry, a benchmark natural vitamin C source.",
        "part_used": "Fruit",
        "forms": ["Dried Fruit", "Powder"],
        "industries": ["Pharmaceutical", "Cosmetics", "Nutraceuticals"],
        "description": (
            "Amla fruit is sun-dried, deseeded, and milled into a fine powder prized "
            "as one of the most recognized natural vitamin C and antioxidant sources "
            "for hair care, skincare, and immunity formulations."
        ),
        "badges": ["100% Natural", "GMO Free", "Vegan", "Gluten Free"],
        "specs": [
            ("Appearance", "Fine light brown powder"),
            ("Color", "Light brown"),
            ("Mesh Size", "80-100 Mesh"),
            ("Moisture", "\u2264 8.0%"),
            ("Ash Value", "\u2264 7.0%"),
            ("Vitamin C", "Naturally occurring, batch-tested"),
            ("Total Plate Count", "\u2264 10,000 CFU/g"),
            ("E. coli", "Negative"),
            ("Salmonella", "Negative"),
        ],
        "color_a": "#c9a876",
        "color_b": "#8a6d3f",
    },
    {
        "slug": "neem",
        "index": "02",
        "latin": "Azadirachta indica",
        "common": "Neem",
        "tagline": "Traditional purity, exported to modern standards.",
        "part_used": "Leaves",
        "forms": ["Dried Leaves", "Powder"],
        "industries": ["Pharmaceutical", "Cosmetics"],
        "description": (
            "Neem leaves are sourced from mature trees and processed under "
            "controlled conditions to preserve their naturally occurring bioactives, "
            "prized across pharmaceutical and cosmetic formulations."
        ),
        "badges": ["100% Natural", "GMO Free", "Vegan"],
        "specs": [
            ("Appearance", "Fine olive-green powder"),
            ("Color", "Olive green"),
            ("Mesh Size", "60-80 Mesh"),
            ("Moisture", "\u2264 8.0%"),
            ("Ash Value", "\u2264 9.0%"),
            ("Total Plate Count", "\u2264 10,000 CFU/g"),
            ("Yeast & Mold", "\u2264 1,000 CFU/g"),
            ("E. coli", "Negative"),
            ("Salmonella", "Negative"),
        ],
        "color_a": "#6b8f5a",
        "color_b": "#1a3d1f",
    },
    {
        "slug": "moringa",
        "index": "03",
        "latin": "Moringa oleifera",
        "common": "Moringa",
        "tagline": "The miracle tree leaf, milled and standardized.",
        "part_used": "Leaves",
        "forms": ["Dried Leaves", "Powder"],
        "industries": ["Pharmaceutical", "Nutraceuticals", "Food Ingredients"],
        "description": (
            "Our Moringa Leaf Powder is made from carefully selected moringa leaves "
            "that are shade dried and finely milled to retain maximum nutrients and "
            "bioactive compounds."
        ),
        "badges": ["100% Natural", "GMO Free", "Vegan", "Gluten Free"],
        "specs": [
            ("Appearance", "Fine green powder"),
            ("Color", "Green"),
            ("Mesh Size", "80-100 Mesh"),
            ("Moisture", "\u2264 7.0%"),
            ("Ash Value", "\u2264 8.0%"),
            ("Protein (N x6.25)", "\u2265 20.0%"),
            ("Total Plate Count", "\u2264 10,000 CFU/g"),
            ("Yeast & Mold", "\u2264 1,000 CFU/g"),
            ("E. coli", "Negative"),
            ("Salmonella", "Negative"),
        ],
        "color_a": "#a8c398",
        "color_b": "#6b8f5a",
    },
    {
        "slug": "tulsi",
        "index": "04",
        "latin": "Ocimum tenuiflorum",
        "common": "Tulsi",
        "tagline": "Holy basil, dried and milled for wellness formulations.",
        "part_used": "Leaves",
        "forms": ["Dried Leaves", "Powder"],
        "industries": ["Pharmaceutical", "Nutraceuticals", "Cosmetics"],
        "description": (
            "Tulsi leaves are hand-picked, shade dried, and milled to retain their "
            "essential oil content, valued for antimicrobial and immunity-support "
            "applications across wellness and personal care formulations."
        ),
        "badges": ["100% Natural", "GMO Free", "Vegan", "Gluten Free"],
        "specs": [
            ("Appearance", "Fine green powder"),
            ("Color", "Green"),
            ("Mesh Size", "60-80 Mesh"),
            ("Moisture", "\u2264 8.0%"),
            ("Ash Value", "\u2264 9.0%"),
            ("Total Plate Count", "\u2264 10,000 CFU/g"),
            ("E. coli", "Negative"),
            ("Salmonella", "Negative"),
        ],
        "color_a": "#7a9e6a",
        "color_b": "#3d5a2f",
    },
    {
        "slug": "hibiscus",
        "index": "05",
        "latin": "Hibiscus rosa-sinensis",
        "common": "Hibiscus",
        "tagline": "Gudhal flower, milled for hair-care formulations.",
        "part_used": "Flowers",
        "forms": ["Dried Flowers", "Powder"],
        "industries": ["Cosmetics", "Nutraceuticals"],
        "description": (
            "Hibiscus rosa-sinensis flowers (Gudhal) are hand-picked, shade dried, and "
            "milled into a fine powder rich in anthocyanins and mucilage, valued in "
            "hair-care formulations for scalp nourishment and shine."
        ),
        "badges": ["100% Natural", "GMO Free", "Vegan"],
        "specs": [
            ("Appearance", "Fine reddish-purple powder"),
            ("Color", "Reddish-purple"),
            ("Mesh Size", "60-80 Mesh"),
            ("Moisture", "\u2264 9.0%"),
            ("Ash Value", "\u2264 9.0%"),
            ("Total Plate Count", "\u2264 10,000 CFU/g"),
            ("E. coli", "Negative"),
            ("Salmonella", "Negative"),
        ],
        "color_a": "#d97070",
        "color_b": "#c94f4f",
    },
]

INDUSTRIES = ["Pharmaceutical", "Cosmetics", "Nutraceuticals", "Food Ingredients"]


def get_product(slug):
    return next((p for p in PRODUCTS if p["slug"] == slug), None)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS, page="home")


@app.route("/products")
def products():
    industry_filter = request.args.get("industry", "").strip()
    q = request.args.get("q", "").strip().lower()

    filtered = PRODUCTS
    if industry_filter and industry_filter != "All Industries":
        filtered = [p for p in filtered if industry_filter in p["industries"]]
    if q:
        filtered = [
            p for p in filtered
            if q in p["common"].lower() or q in p["latin"].lower()
        ]

    return render_template(
        "products.html",
        products=filtered,
        industries=INDUSTRIES,
        active_industry=industry_filter,
        query=q,
        page="products",
    )


@app.route("/products/<slug>")
def product_detail(slug):
    product = get_product(slug)
    if not product:
        abort(404)
    related = [p for p in PRODUCTS if p["slug"] != slug][:3]
    return render_template("product_detail.html", product=product, related=related, page="products")


@app.route("/about")
def about():
    return render_template("about.html", page="about")


@app.route("/quality")
def quality():
    return render_template("quality.html", page="quality")


@app.route("/manufacturing")
def manufacturing():
    return render_template("manufacturing.html", page="manufacturing")


@app.route("/sustainability")
def sustainability():
    return render_template("sustainability.html", page="sustainability")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": request.form.get("name", "").strip(),
            "company": request.form.get("company", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "country": request.form.get("country", "").strip(),
            "product_interest": request.form.get("product_interest", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        if not entry["name"] or not entry["email"] or not entry["message"]:
            flash("Please fill in your name, email, and message.", "error")
            return redirect(url_for("contact"))

        existing = []
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        existing.append(entry)
        with open(CONTACTS_FILE, "w") as f:
            json.dump(existing, f, indent=2)

        flash("Thanks for reaching out — we'll get back to you within one business day.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", products=PRODUCTS, page="contact")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", page=None), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

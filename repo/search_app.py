from flask import Flask, request, render_template
import csv
import math


app = Flask(__name__)

# Function to load and convert CSV to JSON
def load_data():
    data = []
    try:
        with open("restaurants.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure numeric fields are correctly parsed
                row['rating'] = float(row['rating']) if 'rating' in row and row['rating'] else 0.0
                data.append(row)
    except Exception as e:
        print(f"Error loading CSV data: {e}")
    return data


# Function to perform search
def search_data(keyword, page, page_size):
    data = load_data()
    print(f"Loaded {len(data)} records.")  # Debugging

    # Filter the data based on the search keyword
    filtered_data = [
        row for row in data if any(keyword.lower() in str(value).lower() for value in row.values())
    ]

    print(f"Filtered {len(filtered_data)} matching records.")  # Debugging

    # Paginate the results
    start = (page - 1) * page_size
    end = start + page_size
    return filtered_data[start:end], math.ceil(len(filtered_data) / page_size)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    keyword = request.args.get('keyword', '').strip()
    page = int(request.args.get('page', 1))
    page_size = 12

    # Perform search and pagination
    results, total_pages = search_data(keyword, page, page_size)

    # Pass results and metadata to the template
    return render_template(
        'search.html',
        keyword=keyword,
        hits=results,
        page_no=page,
        page_total=total_pages
    )


@app.route('/review')
def review():
    # Retrieve the data passed from search.html
    food_img = request.args.get('food_img', '')
    name = request.args.get('name', 'Unknown')
    opening_hours = request.args.get('opening_hours', 'N/A')
    address = request.args.get('address', 'N/A')
    cuisine = request.args.get('cuisine', 'N/A')
    rating = request.args.get('rating', '0')
    reviews = request.args.get('reviews', 'No reviews available.')
    menu_items = request.args.get('menu_items', 'N/A')
    price_range = request.args.get('price_range', 'N/A')

    # Split reviews into multiple lines for better formatting
    split_reviews = reviews.split("Reviewer ")
    formatted_reviews = ""

    for review in split_reviews:
        if review.strip():
            formatted_reviews += f'<div class="review-card"><p><strong>Reviewer</strong> {review.strip()}</p></div>\n'

    # Render the review page
    return render_template(
        'review.html',
        food_img=food_img,
        name=name,
        address=address,
        cuisine=cuisine,
        rating=rating,
        reviews=reviews,
        formatted_reviews=formatted_reviews,
        opening_hours=opening_hours,
        menu_items=menu_items,
        price_range=price_range
    )


if __name__ == "__main__":
    app.run(debug=True)

import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from flask import Flask, render_template, request, jsonify
import logging
logging.basicConfig(filename="scrapper.log", level=logging.INFO,)

application = Flask(__name__)
app = application

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/review', methods=["GET", "POST"])
def review():
    if request.method == "GET":
        return render_template("home.html")
    else:
      try:  
        query = request.form['content'].replace(" ", "")

        save_dir = "data_csv/"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        url = f"https://www.flipkart.com/search?q={query}"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags_elements = soup.find_all('a')

        product_hrefs = [i['href'] for i in product_tags_elements]

        urls = []
        for i in range(len(product_tags_elements)):
            urls.append(f"https://www.flipkart.com{product_hrefs[i]}")

        allresponses = [requests.get(i) for i in urls[13:-43:3]]

        soups = [BeautifulSoup(allresponses[i].content, 'html.parser')
                 for i in range(len(allresponses))]

        all_reviews = [[i.get_text().replace("READ MORE", "") for i in soups[j].find_all(
            'div', class_="t-ZTKy")] for j in range(len(soups))]

        all_short_reviews = [[i.get_text() for i in soups[j].find_all(
            'p', class_="_2-N8zT")] for j in range(len(soups))]

        all_names = [[i.get_text() for i in soups[j].find_all(
            'p', class_="_2sc7ZR _2V5EHH")] for j in range(len(soups))]

        all_ratings = [[i.get_text() for i in soups[j].find_all(
            'div', class_="_3LWZlK _1BLPMq")] for j in range(len(soups))]

        all_product_names = [[i.get_text() for i in soups[j].find_all('p')]
                             for j in range(len(soups))]

        product_names = []
        customer_names = []
        reviews = []
        ratings = []
        descriptions = []

        for i in range(len(soups)):
            for j in range(10):
                try:
                    customer_names.append(all_names[i][j].replace(",",""))
                except:
                    customer_names.append("Flipkart Customer")
                try:
                    reviews.append(all_short_reviews[i][j].replace(",",""))
                except:
                    reviews.append("NA")
                try:
                    ratings.append(all_ratings[i][j])
                except:
                    ratings.append("NA")
                try:
                    descriptions.append(all_reviews[i][j].replace(",",".."))
                except:
                    descriptions.append("NA")
                try:
                    if (len(all_product_names[i][0].split(" ")) < 16):
                        product_names.append(all_product_names[i][0].replace(",",""))
                    else: 
                        product_names.append("Unknown")
                except:
                    product_names.append("Unknown")

        all_data = {"product": product_names, "customer name": customer_names,
                "rating": ratings, "review": reviews, "description": descriptions}
        df = pd.DataFrame(all_data)
        df = df.set_index(["product"])
        df.to_csv(f"{save_dir}{query}.csv")
        return f"saved {query}.csv file in your directory"
      except:
        return "Could not load data"
# del product_names
# del ratings
# del reviews
# del descriptions
# del customer_names


if __name__ == "__main__":
    app.run(debug=True)

"""Class to scrap product from flipkart and amazon webisite."""
import mechanicalsoup
# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen
from apps import constants
from apps.home.models import Product
# import datetime


class Scrap(object):
    """Scraping flipkart and amazon.

    Scrpping the product name, price, image source, link of the produt.
    """

    def flipkart(self, search_item):
        """Scrpaing the product from flipkart.com.

        Extracting the product name, type, price, url, image, description.
        """
        # Create a browser object
        browser = mechanicalsoup.Browser()
        flipkart_page = browser.get(constants.FLIPKART_URL)

        # selecting the form tag to search the specified item
        search_form = flipkart_page.soup.find(
            "form", {"id": "fk-header-search-form"})

        # selecting the input tag inside the form tag
        # and then initializing it with the search item.
        search_form.find(
            "input", {"id": "fk-top-search-box"})["value"] = search_item

        # submitting the form and starting the search.
        response = browser.submit(search_form, flipkart_page.url)

        # product_list contains the list of product details
        # that are inserted or updated in the database.
        product_list = []

        # looping through each items from search resuts to fetch the details
        # of the product
        for prod in response.soup.find_all("div", {"class": "product-unit"}):
            # a tag
            a_tag_href = prod.find("a").attrs['href']

            # img tag
            img_tag_href = prod.find("img").attrs['data-src']

            # getting the title of the product
            title = prod.find("div", {"class": "pu-title"}).get_text().strip()

            # getting the price of the product
            price = prod.find("div", {"class": "pu-final"}).get_text()

            # getting the link of the product in flipkart.com
            prod_url = constants.FLIPKART_URL + a_tag_href
            # getting the product description
            description = prod.find("ul", {"class": "pu-usp"})

            # getting the product type
            product_type = prod.find("div", {"class": "pu-category"})

            # if the class 'pu-category' exists
            # then initialize the product type variable
            if product_type:
                product_type = product_type.span.get_text()
            # otherwise the search item itself is the product type
            else:
                product_type = search_item

            # removing 'Rs.' and commas from the price
            # and converting it into float type
            float_price = price.strip(
                "\n").replace("Rs. ", "").replace(",", "")

            # storing the above information into the dictionary
            data = {
                'name': title, 'product_type': product_type,
                'price': float_price, 'landing_url': prod_url,
                'image': img_tag_href, 'description': str(description),
                'site_reference': constants.SITE_REFERENCE_FLIPKART}

            try:
                # getting the details of the product
                # from the database that is searched
                product = Product.objects.filter(
                    site_reference='flipkart', name=title,
                    product_type=product_type)
                # checking if the product searched already exists,
                # if the product already exits
                # then update the product the product in the database
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                # otherwise create a new record in the database
                else:
                    p = Product.objects.create(**data)

            # initialize varible 'p' to none if an exception occurs
            except:
                p = None

            # creating a list by append all the product that are scraped,
            # so that it can be displayed in the front end
            if p:
                product_list.append(p)

        # product_list is return to the view to display it in front end
        return product_list

    def amazon(self, search_item):
        """Scrpaing the product from amazon.com.

        Extracting the product name, type, price, url, image, description.
        """
        browser = mechanicalsoup.Browser()
        amazon_page = browser.get(constants.AMAZON_URL)

        # targeting the form tag to search the specified item
        search_form = amazon_page.soup.find("form", {"name": "site-search"})

        # targeting the input tag inside the form tag
        # and then initializing it with the search item.
        search_form.find(
            "input", {"id": "twotabsearchtextbox"})["value"] = search_item

        # submitting the form and starting the search.
        response = browser.submit(search_form, amazon_page.url)

        # product_list contains the list of product details
        # that are inserted or updated in the database.
        product_list = []

        # looping through each items from search resuts to fetch the details
        # of the product
        for prod in response.soup.find_all(
            "div", {"class": "a-fixed-left-grid-inner"}
        ):
            # a tag
            a_tag_href = prod.find("a").attrs['href']

            # img tag
            img_tag_href = prod.find("img").attrs['src']

            # getting the title of the product
            title = prod.find("h2").text

            # getting the price of the product
            price = prod.find("span", {"class": "currencyINR"}).next_sibling

            # getting the product type
            product_type = prod.find(
                "div", {"class": "a-span-last"}).find(
                "span", {"class": "a-text-bold"}).get_text().strip(":")

            # removing 'Rs.' and commas
            # and converting it into float type
            float_price = price.replace(",", "")

            # storing the above information into the dictionary
            data = {
                'name': title, 'product_type': product_type,
                'price': float_price, 'landing_url': a_tag_href,
                'image': img_tag_href,
                'site_reference': constants.SITE_REFERENCE_AMAZON
            }

            try:
                # getting the details of the product
                # from the database that is searched
                product = Product.objects.filter(
                    site_reference='amazon', name=title,
                    product_type=product_type)
                # checking if the product searched already exists,
                # if the product already exits
                # then update the product in the database
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                # otherwise create a new record in the database
                else:
                    p = Product.objects.create(**data)

            # initialize varible 'p' to none if an exception occurs
            except:
                p = None
            # creating a list by append all the product that are scraped,
            # so that it can be displayed in the front end
            if p:
                product_list.append(p)

        # product_list is return to the view to display it in front end
        return product_list

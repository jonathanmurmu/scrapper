import mechanicalsoup
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from apps import constants
from apps.home.models import Product
import datetime

class Scrap(object):
    """Scraping flipkart and amazon.

    Scrpping the product name, price, image source, link of the produt.
    """
    def flipkart(self, search_item):
        """Scrpaing product name, price, image source and link."""
        # flipkart_url = "http://www.flipkart.com"
        browser = mechanicalsoup.Browser()
        flipkart_page = browser.get(constants.FLIPKART_URL)
        search_form = flipkart_page.soup.find("form", {"id": "fk-header-search-form"})
        search_form.find("input", {"id": "fk-top-search-box"})["value"] = search_item
        response = browser.submit(search_form, flipkart_page.url)
        # product_list contains the list of product details
        # that are inserted or updated in the database.
        product_list = []

        for prod in response.soup.find_all("div", {"class": "product-unit"}):
            a_tag_href = prod.find("a").attrs['href']
            img_tag_href = prod.find("img").attrs['data-src']
            title = prod.find("div", {"class": "pu-title"}).get_text().strip()
            price = prod.find("div", {"class": "pu-final"}).get_text()
            prod_url = constants.FLIPKART_URL + a_tag_href
            description = prod.find("ul", {"class": "pu-usp"})
            product_type = prod.find("div", {"class": "pu-category"})

            if product_type:
                product_type = product_type.span.get_text()
            else:
                product_type = search_item
            # handling price, removing 'Rs.' and commas
            float_price = price.strip("\n").replace("Rs. ", "").replace(",", "")
            data = {
                'name': title, 'product_type': product_type,
                'price': float_price, 'landing_url': prod_url,
                'image': img_tag_href, 'description': str(description),
                'site_reference': constants.SITE_REFERENCE_FLIPKART
            }
            try:
                product = Product.objects.filter(
                    site_reference='flipkart', name=title, product_type=product_type)
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                else:
                    p = Product.objects.create(**data)
            except Exception as e:
                print (e)
                p = None
            if p:
                product_list.append(p)
        # product_list is return to the view to display it in front end
        return product_list


    def amazon(self, search_item):
        browser = mechanicalsoup.Browser()
        amazon_page = browser.get(constants.AMAZON_URL)

        search_form = amazon_page.soup.find("form", {"name": "site-search"})
        search_form.find("input", {"id": "twotabsearchtextbox"})["value"] = search_item
        response = browser.submit(search_form, amazon_page.url)
        # product_list contains the list of product details
        # that are inserted or updated in the database.
        product_list = []

        for prod in response.soup.find_all("div", {"class": "a-fixed-left-grid-inner"}):
            a_tag_href = prod.find("a").attrs['href']
            img_tag_href = prod.find("img").attrs['src']
            title = prod.find("h2").text
            price = prod.find("span", {"class": "currencyINR"}).next_sibling
            product_type = prod.find("div", {"class": "a-span-last"}).find("span", {"class": "a-text-bold"}).get_text().strip(":")

            # handling price, removing 'Rs.' and commas
            float_price = price.replace(",", "")
            data = {
                'name': title, 'product_type': product_type,
                'price': float_price, 'landing_url': a_tag_href,
                'image': img_tag_href,
                'site_reference': constants.SITE_REFERENCE_AMAZON
            }
            try:
                product = Product.objects.filter(site_reference='amazon', name=title, product_type=product_type)
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                else:
                    p = Product.objects.create(**data)

            except Exception as e:
                print (e)
                p = None
            if p:
                product_list.append(p)

        # product_list is return to the view to display it in front end
        return product_list

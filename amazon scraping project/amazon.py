import csv
from bs4 import BeautifulSoup
import requests
import json

with open('urls.csv', newline='') as csvfile:   #opening the csv file and storing the values in appropiate variables
    reader = csv.DictReader(csvfile)
    country = [row["country"] for row in reader]

with open('urls.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    asin= [row["Asin"] for row in reader]
urls=[]
c=0
d=0
for i,j in zip(country,asin):      #storing all possible urls in a single list
    url=f"https://www.amazon.{i}/dp/{j}"
    urls.append(url)
#we use headers to make sure that a human-like is scraping the data from the website. If we dont use this then amazon does'nt allow users to scrape html-content
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
for i in urls:  #looping through all the urls to scrape required data using BeautifulSoup4
    try:
        webpage = requests.get(i,headers=headers).content
        soup = BeautifulSoup(webpage, "html.parser")

        #scraping title
        title_tag=soup.find("span",attrs={"id":"productTitle"})
        title=title_tag.string 

        #scraping price
        price=soup.find("span",attrs={"class":'a-color-price'}).string.replace(",",".").replace("\u00a0\u20ac","$").replace("\u20ac","$")

        #scraping image URL
        article=soup.find("div",attrs={"id":'img-canvas'})
        image_src = str(article.find('img')['src']).split(" ")[0]

        #scraping product details
        details=soup.find("div",attrs={"id":'detailBullets_feature_div'})
        list=details.find('ul')
        final_list=list.find_all('span',attrs={"class":'a-text-bold'})
        product_labels=[]
        spn=[]
        for i in final_list:
            spn.append(i.find_next_sibling('span').string)
            x=i.text.replace(" ","")
            y=x.replace(":","")
            z=y.replace("\n","")
            zz=z.replace("\u200f\u200e","")
            product_labels.append(zz)
        res = {}
        for key in product_labels:
            for value in spn:
                res[key] = value
                spn.remove(value)
                break   
            #storing scraped data in form of dictionaries
        product_dict={
                'title':title,
                'image_URL':image_src,
                'price':price,
                'product_details':res
                    }

        #opening a file to dump json data
        with open('data.json','a') as f:
            if c==0:
                f.write("[")
                c+=1
            json.dump(product_dict,f,indent=6)
            f.write(",")
    except:
        d+=1
        print(f"{i} not found {d}")
with open('data.json','a') as f:
    f.write(']')
    f.close()

        




    
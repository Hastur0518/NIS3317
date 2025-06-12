from DrissionPage import Chromium
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["NIS3317"]
tab = Chromium().latest_tab
base_web="https://shanghai.anjuke.com/sale/"
districts = ["minhang", "songjiang", "baoshan", "jiading", "xuhui","qingpu","jingan","putuo","yangpu","fengxian","huangpu","hongkou","changning",
             "jinshan","chongming","shanghaizhoubian","pudong"]
for district in districts:
    mycol= mydb[district]
    for page in range(1, 200):  # Adjust the range for the number of pages you want to scrape
        url= f"{base_web}{district}/p{page}/"
        tab.get(url)
        tab.wait(3)
        properties=tab.eles('@class=property')
        for property in properties:
            try:
                title = property.eles('@class=property-content-title')[0].text
                price = property.eles('@class=property-price-total')[0].text
                avg_price = property.eles('@class=property-price-average')[0].text
                address = property.eles('@class=property-content-info-comm-address')[0].text
                house_info = property.eles('@class=property-content-info-text property-content-info-attribute')[0].text
                area = property.eles('@class=property-content-info-text')[0].text
                towards = property.eles('@class=property-content-info-text')[1].text
                house_type = property.eles('@class=property-content-info-text')[2].text
                build_in = property.eles('@class=property-content-info-text')[3].text
                specials = property.eles('@class=property-content-info')[1].text
                data = {
                    "title": title,
                    "price": price,
                    "avg_price": avg_price,
                    "address": address,
                    "house_info": house_info,
                    "area": area,
                    "towards": towards,
                    "house_type": house_type,
                    "build_in": build_in,
                    "specials": specials
                }
                mycol.update_one({"title": title}, {"$set": data}, upsert=True)
                print(data)
            except Exception as e:
                print(f"Error processing property: {e}")
    print(f"Finished processing district: {district}")
import json

from auto.spiders.autogidas_utils.car import Car



class autogidas_helper:

    def __init__(self):
        pass


    def extract_cars_from_search_page(self, response):
        car_list = []

        items = response.css('article.list-item')
        for item in items:
            name = item.css('.item-title::text').get()
            year = item.css('.param-year b::text').get(default='').strip()
            gearbox = item.css('.param-gearbox b::text').get(default='').strip()
            mileage = item.css('.param-mileage b::text').get(default='').strip()
            engine = item.css('.param-engine b::text').get(default='').strip()
            fuel = item.css('.param-fuel-type b::text').get(default='').strip()
            location = item.css('.param-location b::text').get(default='').strip()
            description = item.css('.primary::text').get(default='')
            price = item.css(".item-price::text").get(default='').strip()
            href = item.css("a::attr(href)").get()

            car = Car(
                name=name,
                year=year,
                gearbox=gearbox,
                mileage=mileage,
                engine=engine,
                fuel=fuel,
                location=location,
                description=description,
                price=price,
                currency="EUR",
                href=href
            )
            
            car_list.append(car)

        return car_list

    def extract_car_models_from_main_page(self, html):
        look_for_string = '{"value":""'
        x1 = html.find(look_for_string)

        if x1 != -1:
            html_right = html[x1 - 1:]

            x2 = html_right.find("]")

            string_cars = html_right[:x2 + 1]
            json_cars = json.loads(string_cars)
            
            json_cars_filtered = [Car(name=obj['value'], count=obj['count'])
                    for obj in json_cars if self.is_valid_count(obj['count'])]

            return json_cars_filtered

    def is_valid_count(self, count):
        try:
            int(count)
            return True
        except (ValueError, TypeError):
            return False

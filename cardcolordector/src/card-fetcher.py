import argparse
import enum
import threading
import multiprocessing
import requests
import os

class Color(enum.Enum):
    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"

class CardInfo:
    def __init__(self, json):
       self.card_id = json["id"]
       self.name = json["name"]
       self.color = json["colors"][0]
       self.cmc = json["cmc"]
       self.type_line = json["type_line"]  
       self.url = json["image_uris"]["normal"]
       
  #  def __repr__(self):
   #     return f"card_id : {self.card_id}\nname : {self.name}\ncolor : {self.color}\ncmc : {self.cmc}\ntype_line : {self.type_line} \nimage_uri_normal : {self.url}"

def fetchCardImage(url, name):
    try:
        response = requests.get(url=url)            
        if response.status_code == 200:
            os.makedirs('../data/images/', exist_ok=True)
            #with open(f'../data/images/{name}.jpg', 'wb') as file:
            #    for chunk in response.iter_content(1024):
            #       file.write(chunk)

    except Exception as e:
        print(e)

def fetchCardInfo(color):
    
    url = 'https://api.scryfall.com/cards/random?q=color%3D' + color.value
    print(url)
    
    try:
        response = requests.get(url=url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        data = response.json()
        card = CardInfo(data)
        print(card)
        
        fetchCardImage(card.url, card.name)
        
    except Exception as e:
        print(e.response)
        

def main():
    print(Color.WHITE.value)
    parser = argparse.ArgumentParser(description="Fetch card information based on color.")
    parser.add_argument(
            "color",
            type=lambda color: Color[color],
            choices=list(Color),
            help="Color of the card to fetch (options: WHITE, BLUE, BLACK, RED, GREEN, COLORLESS)"
        )
    
    args = parser.parse_args()
    
    threads = []
    max_threads = os.cpu_count() - 3

    for _ in range(max_threads):
        thread = threading.Thread(target=fetchCardInfo, args=(args.color))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    main()
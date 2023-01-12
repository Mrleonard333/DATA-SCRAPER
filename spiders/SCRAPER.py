from DATA_SCRAPER.items import DataScraperItem
import matplotlib.pyplot as plt
from os import system
import pandas as pd
import scrapy

class Spider_system(scrapy.Spider):
    name = "SS"
    Page_Count = 1

    DataFrame_Info = dict()
    start_urls = ["https://www.amazon.com.br/s?k=ssd+kingston+240gb&__mk_pt_BR=ÅMÅŽÕÑ&crid=2O773PDSB95WJ&sprefix=ssd+kingston+240gb%2Caps%2C111&ref=nb_sb_noss_1"]

    def Calculator(self, SITE):
        Price = Count = 0
        All_Prices = list()
                                # v Will format the DataFrame data to a list
        for P in SITE["Price"].tolist():
            P = P.replace("R$", "")
            P = P.replace(".", "")
            P = P.replace(",", ".")
            P = float(P)

            Count += 1
            Price += P
            All_Prices.append(P)
        
        Average = Price / Count
        return Average, min(All_Prices), Count
    
    def SCRAPER(self, response, Site, Site_Name, Next_Site, Items_Path, Name_Path, Price_Path, Page_Path):
        system('clear')
        system('cls')

        print(f"[_____________{Site_Name.upper()}_____________]")
        All_Items = response.css(Items_Path) # < Will get values from the HTML

        for Item in All_Items:
            Name = Item.css(Name_Path).get() # < Will store a especific value of the HTML, as a string
            Price = Item.css(Price_Path).get()

            try:
                if Name and Price and "kingston" in str(Name).lower():
                    self.DataFrame_Info["Name"].append(str(Name))
                    self.DataFrame_Info["Site"].append(Site_Name)
                    self.DataFrame_Info["Price"].append(f"R${Price}")
            except:
                if Name and Price and "kingston" in str(Name).lower():
                    self.DataFrame_Info["Name"] = [str(Name)]
                    self.DataFrame_Info["Site"] = [Site_Name]
                    self.DataFrame_Info["Price"] = [f"R${Price}"]

        self.Page_Count += 1
        if self.Page_Count <= 3:
            print("[_____________NEW_PAGE_____________]")
            Next_Page = response.css(Page_Path).get()

            if Site_Name.lower() in Next_Page.lower():
                self.start_urls[0] = Next_Page
            else:
                self.start_urls[0] = f"{Site}{Next_Page}"
        else:
            print("[_____________EXITING_____________]")

            self.Page_Count = 0
            self.start_urls[0] = Next_Site

    def parse(self, response):
        if "amazon" in self.start_urls[0].lower():
            self.SCRAPER(response, "https://www.amazon.com.br", "AMAZON",
                r"https://lista.mercadolivre.com.br/ssd-kingston-240gb#D[A:ssd%20kingston%20240gb]",
                "div.puis-padding-left-small", "div.a-section span.a-text-normal::text", "span.a-price-whole::text",
                "span.s-pagination-strip a.s-pagination-next::attr(href)")
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
                    # ^ Will send a request to the URL and execute the function again

        if "mercadolivre" in self.start_urls[0].lower():
            self.SCRAPER(response, "https://lista.mercadolivre.com.br", "MercadoLivre", "Null",
                "div.shops__result-content-wrapper", "div.ui-search-item__group--title h2::text", "span.ui-search-price__part span.price-tag-fraction::text",
                "li.andes-pagination__button--next a.andes-pagination__link::attr(href)")
            
            if "Null" != self.start_urls[0]:
                yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        
        if "Null" == self.start_urls[0]:
            Item_Data = DataScraperItem() # < Will import a Item
            for Count in range(0, len(self.DataFrame_Info["Site"])):
                Item_Data["Name"] = self.DataFrame_Info["Name"][Count]
                Item_Data["Price"] = self.DataFrame_Info["Price"][Count]
                Item_Data["Site"] = self.DataFrame_Info["Site"][Count]
                yield Item_Data # < Will send the data to items.py
            DataFrame = pd.DataFrame(self.DataFrame_Info) # < Will create a DataFrame

            system('clear')
            system('cls')

            Amazon = DataFrame[DataFrame["Site"] == "AMAZON"] # < Will store all the DataFrame data, that has the site as Amazon
            Mercado_Livre = DataFrame[DataFrame["Site"] == "MercadoLivre"]
            Amazon_Average, Amazon_Minimun, Amazon_Producs = self.Calculator(Amazon)
            Mercado_Average, Mercado_Minimun, Mercado_Producs = self.Calculator(Mercado_Livre)
                
            plt.figure().set_figwidth(10) # < Will configure the grafic's width

            plt.bar(["A_Average", "A_Minimun", "A_Products"], # < Will configure the grafic's columns
                [Amazon_Average, Amazon_Minimun, Amazon_Producs], # < Will configure the value of the columns
                color=["c", "c", "c"], label="Amazon") # < Will add the legend value
            
            plt.bar(["M_Average", "M_Minimun", "M_Products"],
                [Mercado_Average, Mercado_Minimun, Mercado_Producs],
                color=["y", "y", "y"], label="Mercado_Livre")
            
            plt.legend() # < Will legend the both
            plt.show() # < Will show the grafic

            system('clear')
            system('cls')

            print(DataFrame)

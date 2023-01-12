# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector

class DataScraperPipeline:
    def Connection_Stabilizer(self):
        self.connection = mysql.connector.connect( # < Will stabilize a connection with the DataBase
            host="host",
            user="user", 
            password=r'password', 
            database='schema_name'
        )
        self.cursor = self.connection.cursor() # < Will store the cursor, for DataBase changes

    def process_item(self, item, spider):
        self.Connection_Stabilizer()

        Id = 0
        Site = str(item["Site"])
        Name = str(item["Name"])
        Price = str(item["Price"])
        
        self.cursor.execute("SELECT * FROM schema.label;") # < Will execute a MySQL command
        ALL_DATA = self.cursor.fetchall() # < Will store all selected data

        if ALL_DATA:
            for DATA in ALL_DATA:
                Id = DATA[0]
                if Name == DATA[1] and Price == DATA[2] and Site == DATA[3]:
                    print("[__________ALREADY EXIST__________]")
                    Id = "EXIT"
                    break
        
        if type(Id) is int:
            print("[__________SENDING__________]")

            Id += 1
            Name = Name.replace("'", r"\'")
            Price = Price.replace("'", r"\'")
            
            self.cursor.execute(f"INSERT INTO `schema`.`label` (`id`, `Name`, `Price`, `Site`) VALUES ('{Id}', '{Name}', '{Price}', '{Site}');")
            self.connection.commit() # < Will save the DataBase changes

        self.cursor.close()
        self.connection.close() # < Will close the DataBase connection

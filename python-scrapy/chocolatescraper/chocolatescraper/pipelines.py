# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUsdRate = 1.3
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('price'):
            
            floatPrice = float(adapter['price'])
            
            adapter['price'] = floatPrice * self.gbpToUsdRate
            
            return item
        
        else: 
            raise DropItem(f"missing price in {item}")
        
        
class DuplicatesPipeline:
    
    def __init__(self):
        self.names_seen = set()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter['name'] in self.names_seen:
            raise DropItem(f"duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item
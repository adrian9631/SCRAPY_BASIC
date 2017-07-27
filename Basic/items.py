# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BasicItem(scrapy.Item): #hightlight to change
    # define the fields for your item here like:
    # name = scrapy.Field()

    ##################################################

    #add something here

    ##################################################

    #recording the date
    submission_date = scrapy.Field()
    #recording the MongodbObject_Id
    _id = scrapy.Field()


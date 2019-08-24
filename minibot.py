# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 20:38:15 2019

@author: yoda
"""
import os
from bs4 import BeautifulSoup
import requests
import re
from pandas import DataFrame
from collections import OrderedDict 
from tkinter import Tk, Label, Entry, Button, END

class mini_bot():    
    def __init__(self):    
        self.window = Tk()
        self.window.maxsize('500','150')
        self.window.minsize('500','150')
        self.window.title("Welcome to Minimum price Bot!")
        self.window.geometry('500x150')             
        self.lbl = Label(self.window, text="ItemCode", font=("Arial Bold",20))
        self.lbl.grid(column=0, row=0)
        self.txt = Entry(self.window,width=25, font=("Arial Bold",10))
        self.txt.grid(column=0, row=2)
        self.btn1 = Button(self.window,width=25, text="Search", command=self.get_minimum_price)
        self.btn2 = Button(self.window,width=20, text="remove", command=self.remove_txt)
        self.btn1.grid(column=1, row=2)
        self.btn2.grid(column=2, row=2)
        self.window.mainloop()
        
    def get_minimum_price(self):
        itemCode = self.txt.get()
        result = OrderedDict()
        print_result = OrderedDict()
        url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%s&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=%s" % (itemCode,itemCode)
        respone = requests.get(url)
        html = respone.content
        bs = BeautifulSoup(html, 'html.parser')
        titles = bs.findAll('a', attrs={'class': 'tit'})
        prices = bs.findAll('span', attrs={'class': 'num _price_reload'})
        
        title_list = []
        price_list = []   
        link_list = []         
        for tit in titles:
            dir(tit)
            if tit.text != "쇼핑몰별 최저가":        
                title_list.append(re.sub('[\n\t            ]','',tit.text))
                link_list.append(tit.attrs['href'])
        for p in prices:
            price_list.append(p.text)
            
        result['title'] = title_list[0:3]
        result['price'] = price_list[0:3]
        result['link'] = link_list[0:3]
        
        
        print_result['title'] = title_list[0:3]
        print_result['price'] = price_list[0:3]
    
        df = DataFrame(result)
        
        if not os.path.isdir("C:/miniBot/"):
            os.mkdir("C:/miniBot/")        
        df.to_csv("C:/miniBot/"+str(itemCode)+".csv", index=False, encoding="ms949")
        print_df = DataFrame(print_result)
        rows, cols = print_df.shape
        for r in range(rows):
            for c in range(cols):
                e = Entry(self.window,bd=2)
                e.insert(0, print_df.iloc[r,c])
                e.grid(row=r+3, column=c)
                e.config(width=25,state='readonly')    
    
    def remove_txt(self):
        self.txt.delete("0", END)


if __name__ == '__main__':
    mini_bot()

    
    
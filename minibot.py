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
from tkinter import Tk, Entry, Button, END, filedialog, ttk
from datetime import datetime

class mini_bot():    
    def __init__(self):    
        self.window = Tk()
        self.window.maxsize('500','150')
        self.window.minsize('500','150')
        self.window.title("Welcome to Minimum price Bot!")
        self.window.geometry('500x150+350+200')        
        self.lbl = Entry(self.window,width=20,bd=2)
        self.lbl.grid(column=0, row=0)
        self.lbl.insert(0,"Upload file")
        self.lbl.configure(fg="gray")
        self.lbl.config(state='readonly')
        self.txt = Entry(self.window,width=20, font=("Arial Bold",10))
        self.txt.grid(column=0, row=2)
        self.txt.insert(0,"item code")
        self.txt.configure(fg="gray")
        self.txt.bind("<Button>", self.initial_txt)
        self.btn1 = Button(self.window,width=20, text="Search", command=self.get_minimum_price)
        self.btn2 = Button(self.window,width=20, text="remove", command=self.remove_txt)
        self.btn3 = Button(self.window,width=20, text='FileUpload', command=self.upload_file)
        self.btn4 = Button(self.window,width=20, text='FileSearch', command=self.search_file)
        self.btn1.grid(column=1, row=2)
        self.btn2.grid(column=2, row=2)
        self.btn3.grid(column=1, row=0)
        self.btn4.grid(column=2, row=0)
        self.fileName = ""
        self.today = datetime.today()
        self.window.mainloop()
        
    def get_minimum_price(self):
        itemCode = self.txt.get()
        print_result = {}
        if itemCode == "item code":
            self.pop_msg("require item code!")
        else:
            print_result = self.write_csv(itemCode)
            print_df = DataFrame(print_result)
            rows, cols = print_df.shape
            for r in range(rows):
                for c in range(cols):
                    e = Entry(self.window,bd=2)
                    e.insert(0, print_df.iloc[r,c])
                    e.grid(row=r+3, column=c)
                    e.config(width=20,state='readonly')
    
    def write_csv(self,itemCode):
        result = OrderedDict()
        print_result = OrderedDict()
        url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%s&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=%s" % (itemCode,itemCode)
        respone = requests.get(url)
        html = respone.content
        bs = BeautifulSoup(html, 'html.parser')
        titles = bs.findAll('a', attrs={'class': 'tit'})
        prices = bs.findAll('span', attrs={'class': 'num _price_reload'})        
        malls = bs.select("div.info_mall")
        
        title_list = []
        price_list = []
        mall_list = []
        link_list = []
        for tit in titles:
            dir(tit)
            if tit.text != "쇼핑몰별 최저가":        
                title_list.append(re.sub('[\n\t            ]','',tit.text))
                link_list.append(tit.attrs['href'])
        for p in prices:
            price_list.append(p.text)
        for ma in malls:
            if ma.select("a._btn_mall_detail") !=[]:
                mall_list.append(ma.select("a._btn_mall_detail")[0].attrs['data-mall-name'])
            else:
                mall_list.append(ma.select("span.mall_name")[0].text)
            
        result['title'] = title_list[0:3]
        result['price'] = price_list[0:3]
        result['mall'] = mall_list[0:3]
        result['link'] = link_list[0:3]        
        
        print_result['title'] = title_list[0:3]
        print_result['price'] = price_list[0:3]
        print_result['mall'] = mall_list[0:3]
    
        df = DataFrame(result)        
        if not os.path.isdir("C:/miniBot/"+self.today.strftime("%y%m%d")):
            os.mkdir("C:/miniBot/"+self.today.strftime("%y%m%d"))        
        df.to_csv("C:/miniBot/"+self.today.strftime("%y%m%d")+"/"+str(itemCode)+".csv", index=False, encoding="ms949")
        return print_result
    
    def initial_txt(self,event=""):
        self.txt.configure(fg="black")
        self.txt.delete(0, END)
            
    def remove_txt(self,event=""):
        if self.txt.get() != "item code":
            self.txt.configure(fg="black")
            self.txt.delete(0, END)
        
    def upload_file(self):
        self.fileName = filedialog.askopenfilename()        
        self.lbl.config(state='normal')
        self.lbl.delete(0, END)        
        self.lbl.insert(0, self.fileName)
        self.lbl.config(state='readonly')

    def search_file(self): 
        if self.fileName == "":
            self.pop_msg("require upload file!")
        else:            
            with open(self.fileName, "rb") as f:
                for line in f.readlines():
                    line = line.decode("utf-8")
                    line = re.sub("[\r\n]","",line)
                    itemCode = line
                    self.write_csv(itemCode)
            self.pop_msg('Check [C:/miniBot/'+self.today.strftime("%y%m%d")+'] folder')
        
    def pop_msg(self,msg=""):
        popup = Tk()
        popup.wm_title("Complete!")
        popup.geometry('200x50+480+250')
        label = ttk.Label(popup, text=msg)
        label.pack(expand=True, fill="both")
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()

if __name__ == '__main__':
    mini_bot()

    
    
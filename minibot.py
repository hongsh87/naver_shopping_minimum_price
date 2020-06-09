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
import json

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
        self.btn1 = Button(self.window,width=20, text="Search", command=self.search_text)
        self.btn2 = Button(self.window,width=20, text="remove", command=self.remove_txt)
        self.btn3 = Button(self.window,width=20, text='FileUpload', command=self.upload_file)
        self.btn4 = Button(self.window,width=20, text='FileSearch', command=self.search_file)
        self.btn1.grid(column=1, row=2)
        self.btn2.grid(column=2, row=2)
        self.btn3.grid(column=1, row=0)
        self.btn4.grid(column=2, row=0)
        self.fileName = ""
        self.today = datetime.today()
        self.itemCode = ""
        self.defaultFolder = ""        
        self.url = "https://openapi.naver.com/v1/search/shop.json?"
        self.options = "&sort=asc&display=1"
        self.headers = {'X-Naver-Client-Id': 'Input your client id', 'X-naver-Client-secret': 'Input your client secret' }
        self.window.mainloop()

    
    def set_default_folder(self):
        self.defaultFolder = filedialog.askdirectory()
        
    def search_text(self):
        if self.defaultFolder == "":
            self.set_default_folder()
        itemCode = self.txt.get()
        print_result = {}
        if itemCode == "item code":
            self.pop_msg("require item code!")
        else:
            print_result = self.search_price(itemCode)
            print_df = DataFrame(print_result,index=[0])
            rows, cols = print_df.shape
            for r in range(rows):
                for c in range(cols):
                    e = Entry(self.window,bd=2)
                    e.insert(0, print_df.iloc[r,c])
                    e.grid(row=r+3, column=c)
                    e.config(width=20,state='readonly')
    
    def search_price(self,itemCode,isFile=False):
        self.itemCode = itemCode
        result = OrderedDict()
        print_result = OrderedDict()
        
        queryString = "query="+itemCode
        response = requests.get(self.url+queryString+self.options, headers=self.headers)
        res = json.loads(response.text)
        res['items'][0]['lprice']
        
        
        result = {'title':res['items'][0]['title'],
                  'price':res['items'][0]['lprice'],
                  'mall':res['items'][0]['mallName'],
                  'link':res['items'][0]['link']}
        
        print_result = {'title':res['items'][0]['title'],
                  'price':res['items'][0]['lprice'],
                  'mall':res['items'][0]['mallName']}
        
        df = DataFrame(result,index=[0])
        if isFile == True:
            return result
        else:
            self.write_csv(df)
        return print_result
        
        
        # respone = requests.get(url)
        # html = respone.content
        # bs = BeautifulSoup(html, 'html.parser')
        # titles = bs.findAll('div', attrs={'class': 'basicList_title__3P9Q7'})
        # links = bs.findAll('a', attrs={'class':'basicList_link__1MaTN'})
        # prices = bs.findAll('span', attrs={'class': 'price_num__2WUXn'})        
        # # malls = bs.select("div.basicList_mall_area__lIA7R")
        # # malls = bs.findAll('div', attrs={'class': 'basicList_mall_area__lIA7R'})    
        
        # title_list = []
        # price_list = []
        # # mall_list = []
        # link_list = []
        # for tit in titles:
        #     dir(tit)
        #     if tit.text != "쇼핑몰별 최저가":        
        #         title_list.append(re.sub('[\n\t            ]','',tit.text))        
        # for link in links:
        #         link_list.append(link.attrs['href'])
        # for p in prices:
        #     price_list.append(p.text)
        # # for m in malls:
        # #     mall_list.append(m.text)
        # # for ma in malls:
        # #     if ma.select("a.basicList_mall__sbVax") !=[]:
        # #         mall_list.append(ma.select("a._btn_mall_detail")[0].attrs['data-mall-name'])
        # #     else:
        # #         mall_list.append(ma.select("span.mall_name")[0].text)
            
        # result['title'] = title_list[0:1]
        # result['price'] = price_list[0:1]
        # # result['mall'] = mall_list[0:1]
        # result['link'] = link_list[0:1]        
        
        # print_result['title'] = title_list[0:1]
        # print_result['price'] = price_list[0:1]
        # # print_result['mall'] = mall_list[0:1]    
       
    
    def write_csv(self,df):
        if not os.path.isdir(self.defaultFolder+"/"+self.today.strftime("%y%m%d")):
            os.mkdir(self.defaultFolder+"/"+self.today.strftime("%y%m%d"))        
        df.to_csv(self.defaultFolder+"/"+self.today.strftime("%y%m%d")+"/"+str(self.itemCode)+".csv", index=False, encoding="utf-8-sig")
    
    def initial_txt(self,event=""):
        if self.txt.get() == "item code":
            self.txt.configure(fg="black")
            self.txt.delete(0, END)
            
    def remove_txt(self,event=""):
        if self.txt.get() != "item code":
            self.txt.configure(fg="black")
            self.txt.delete(0, END)
            self.txt.insert(0,"item code")
            self.txt.configure(fg="gray")
        
    def upload_file(self):
        self.fileName = filedialog.askopenfilename()
        self.lbl.config(state='normal')
        self.lbl.delete(0, END)        
        self.lbl.insert(0, self.fileName)
        self.lbl.config(state='readonly')

    def search_file(self):
        if self.defaultFolder == "":
            self.set_default_folder()
        total_df = DataFrame()
        total_list = []
        if self.fileName == "":
            self.pop_msg("require upload file!")
        else:            
            with open(self.fileName, "rb") as f:
            # fileName = "C:/Users/choko\/Downloads/test.csv"
            # with open(fileName, "rb") as f:
                for line in f.readlines():
                    line = line.decode("utf-8")
                    line = re.sub("[\r\n]","",line)
                    itemCode = line
                    total_list.append(self.search_price(itemCode,isFile=True))
                    # print(total_list)
                total_df = DataFrame(total_list)
                self.write_csv(total_df)
            self.pop_msg('Check ['+self.defaultFolder+"/"+self.today.strftime("%y%m%d")+'] folder')
        
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

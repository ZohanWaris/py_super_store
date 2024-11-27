import tkinter as tk
from tkinter import ttk
from  tkinter import messagebox
import pymysql
from datetime import datetime

class store():
    def __init__(self, root):
        self.root = root
        self.root.title("Super Store")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Super Store Management", bd=4, relief="raised", bg="gray", font=("Elephant",40,"bold"),fg="white")
        title.pack(side="top", fill="x")

        # golbal variable
        self.totalBill = 0

        # option frame 

        optFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150,220,180))
        optFrame.place(width=self.width/3, height=self.height-180, x=50, y=100)

        addBtn = tk.Button(optFrame,command=self.addFrameFun, text="Add_Item", width=20, font=("Arial",20,"bold"), bd=3, relief="raised")
        addBtn.grid(row=0, column=0, padx=30, pady=25)

        quantBtn = tk.Button(optFrame,command=self.AddQuantFrame, text="Add_Quantity", width=20, font=("Arial",20,"bold"), bd=3, relief="raised")
        quantBtn.grid(row=1, column=0, padx=30, pady=25)

        srchBtn = tk.Button(optFrame,command=self.searchFrame, text="Search", width=20, font=("Arial",20,"bold"), bd=3, relief="raised")
        srchBtn.grid(row=2, column=0, padx=30, pady=25)

        allBtn = tk.Button(optFrame,command=self.showAll, text="Show_All", width=20, font=("Arial",20,"bold"), bd=3, relief="raised")
        allBtn.grid(row=3, column=0, padx=30, pady=25)

        purchaseBtn = tk.Button(optFrame,width=20,command=self.purchaseFrame, text="Purchase Item", font=("Arial",20,"bold"), bd=3, relief="raised")
        purchaseBtn.grid(row=4, column=0, padx=30, pady=25)
        # detail Frame 

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150,170,230))
        self.detFrame.place(width=self.width/2+50, height=self.height-180, x=self.width/3+100, y=100)

        detLbl = tk.Label(self.detFrame, text="Store Details", bg=self.clr(150,170,230), font=("Elephant",30,"bold"))
        detLbl.pack(side="top", fill="x")

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2, height=self.height-290, x=22, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame,xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("item","price","quant","exp"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("item", text="Item_Name")
        self.table.heading("price", text="Price")
        self.table.heading("quant", text="Quantity")
        self.table.heading("exp", text="Expiry_Date")
        self.table["show"] = "headings"
        
        self.table.pack(fill="both", expand=1)

    def addFrameFun(self):
        self.addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(230,150,180))
        self.addFrame.place(width=self.width/3, height=self.height-200, x=self.width/3+80,y=110)

        nameLbl = tk.Label(self.addFrame, text="Item_Name:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.name = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.name.grid(row=0, column=1, padx=10, pady=30)

        priceLbl =tk.Label(self.addFrame, text="Item_Price:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        priceLbl.grid(row=1, column=0, padx=20, pady=30)
        self.price = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.price.grid(row=1, column=1, padx=10, pady=30)

        quantLbl = tk.Label(self.addFrame, text="Item_Quantity:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        quantLbl.grid(row=2, column=0, padx=20, pady=30)
        self.quant = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.quant.grid(row=2, column=1, padx=10, pady=30)

        expLbl = tk.Label(self.addFrame, text="Expiry:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        expLbl.grid(row=3, column=0, padx=20, pady=30)
        self.exp = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.exp.grid(row=3, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.addFrame,command=self.addFun, text="Enter", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=4, column=0, padx=30, pady=40, columnspan=2)

    def desAddFrame(self):
        self.addFrame.destroy()

    def addFun(self):
        itemName = self.name.get()
        price = self.price.get()
        quant = self.quant.get()
        exp = self.exp.get()

        if itemName and price and quant and exp:
            price_int = int(price)
            quant_int = int(quant)
            exp_date = datetime.strptime(exp, "%Y-%m-%d")
            try:
                self.dbFun()
                self.cur.execute("insert into market(item,price,quant,expiry) values(%s,%s,%s,%s)",(itemName,price_int,quant_int,exp_date))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"Item.{itemName} is added Successfuly!")
                self.desAddFrame()

                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from market where item=%s",itemName)
                row = self.cur.fetchone()
                self.table.insert('',tk.END, values=row)

                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desAddFrame()
        else:
            tk.messagebox.showerror("Error","Please Fill All Input Fields!")

    def AddQuantFrame(self):
        self.addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(230,150,180))
        self.addFrame.place(width=self.width/3, height=self.height-300, x=self.width/3+80,y=110)

        nameLbl = tk.Label(self.addFrame, text="Item_Name:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.newName = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.newName.grid(row=0, column=1, padx=10, pady=30)

        quantLbl = tk.Label(self.addFrame, text="New_Quantity:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        quantLbl.grid(row=1, column=0, padx=20, pady=30)
        self.newQuant = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.newQuant.grid(row=1, column=1, padx=10, pady=30)

        expLbl = tk.Label(self.addFrame, text="Expiry:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        expLbl.grid(row=2, column=0, padx=20, pady=30)
        self.newExp = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.newExp.grid(row=2, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.addFrame,command=self.quantFun, text="Enter", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=3, column=0, padx=30, pady=40, columnspan=2)

    def quantFun(self):
        itemName = self.newName.get()
        quant = self.newQuant.get()
        exp = self.newExp.get()

        if itemName and quant and exp:
            quant_int = int(quant)
            exp_date = datetime.strptime(exp,"%Y-%m-%d")

            try:
                self.dbFun()
                self.cur.execute("select quant from market where item=%s",itemName)
                item = self.cur.fetchone()
                upd = item[0]+quant_int
                self.cur.execute("update market set quant=%s, expiry=%s where item=%s",(upd,exp_date,itemName))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"Item.{itemName} is updated!")
                self.desAddFrame()

                self.cur.execute("select * from market where item=%s",itemName)
                row = self.cur.fetchone()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=row)

                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desAddFrame()
        else:
            tk.messagebox.showerror("Error","Please Fill All Input Fields!")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def searchFrame(self):
        self.addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(230,150,180))
        self.addFrame.place(width=self.width/3, height=self.height-450, x=self.width/3+80,y=110)

        nameLbl = tk.Label(self.addFrame, text="Item_Name:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.srchName = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.srchName.grid(row=0, column=1, padx=10, pady=30)        

        okBtn = tk.Button(self.addFrame,command=self.searchFun, text="Enter", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=1, column=0, padx=30, pady=40, columnspan=2)

    def searchFun(self):
        itemName = self.srchName.get()
        try:
            self.dbFun()
            self.cur.execute("select * from market where item=%s",itemName)
            row = self.cur.fetchone()

            if row:
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END,values=row)
                self.desAddFrame()

                self.con.close()
            else:
                tk.messagebox.showerror("Error","Item Does not Exist in Store!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("select * from market")
            data = self.cur.fetchall()

            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END, values=i)
            
            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def purchaseFrame(self):
        self.addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(230,150,180))
        self.addFrame.place(width=self.width/3, height=self.height-300, x=self.width/3+80,y=110)

        nameLbl = tk.Label(self.addFrame, text="Item_Name:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.item = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.item.grid(row=0, column=1, padx=10, pady=30)

        quantLbl = tk.Label(self.addFrame, text="Quantity:", font=("Arial",15,"bold"),bg=self.clr(230,150,180))
        quantLbl.grid(row=1, column=0, padx=20, pady=30)
        self.quantity = tk.Entry(self.addFrame, width=18, font=("Arial",15,"bold"), bd=2)
        self.quantity.grid(row=1, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.addFrame,command=self.billFun, text="Enter", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=2, column=0, padx=30, pady=40, columnspan=2)

    def billFun(self): 
        if not hasattr(self, 'billBox'):     
            self.billFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="light green")
            self.billFrame.place(width=self.width/3+100, height=self.height-180, x=self.width/3+80, y=100)

            self.billBox = tk.Listbox(self.billFrame, width=43, height=15, font=("Arial",15,"bold"))
            self.billBox.grid(row=0, column=0, padx=20 ,pady=30,columnspan=3)

            purBtn = tk.Button(self.billFrame,command=self.purchaseFrame, text="More_item", bd=3, width=8, font=("Arial",15,"bold"))
            purBtn.grid(row=1, column=0, padx=30, pady=30)

            billBtn = tk.Button(self.billFrame,command=self.printBill, text="Print_Bill", bd=3, width=8, font=("Arial",15,"bold"))
            billBtn.grid(row=1,column=1, padx=20, pady=30)

            closeBtn = tk.Button(self.billFrame,command=self.closeFun, text="Close", bd=3, width=8, font=("Arial",15,"bold"))
            closeBtn.grid(row=1, column=2, padx=20, pady=30)

        self.purchaseFun()


    def purchaseFun(self):
        itemName = self.item.get()
        quantity = int(self.quantity.get())

        try:
            self.dbFun()
            self.cur.execute("select price,quant,expiry from market where item=%s",itemName)
            row = self.cur.fetchone()
            if row:
                today = datetime.now().date()
                exp = (row[2]-today).days
                if exp >0:
                    if row[1] >quantity:
                        amount = row[0] * quantity
                        self.totalBill = self.totalBill + amount 
                        upd = row[1] - quantity
                        self.cur.execute("update market set quant=%s where item=%s",(upd,itemName))
                        self.con.commit()


                        line = f"Amount of {quantity} {itemName} is: {amount}"
                        
                        self.billBox.insert(tk.END, line)
                        self.desAddFrame()
                    else:
                        tk.messagebox.showerror("Error", f"This {itemName} is no more available!")
                        self.desAddFrame()
                else:
                    tk.messagebox.showerror("Error", f"This {itemName} item is expired!")
                    self.desAddFrame()
            else:
                tk.messagebox.showerror("Error",f"Item.{itemName} does not exist!")
                self.desAddFrame()
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")
            self.desAddFrame()

    def printBill(self):
        line = f"-----------------"
        line2 = f"Total Bill: {self.totalBill}"
        self.billBox.insert(tk.END, line)
        self.billBox.insert(tk.END, line2)

    def closeFun(self):
        self.billFrame.destroy()


    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = store(root)
root.mainloop()
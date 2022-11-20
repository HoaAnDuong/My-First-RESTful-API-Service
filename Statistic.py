
from api_and_table import *
import pandas
import seaborn
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
import matplotlib.colors as mcolors
import time

random.seed(time.time())

#SQLite Table
table["RevenueFromProducts"] = Table(
    "RevenueFromProducts",metadata,
    Column("Day", VARCHAR()),
    Column("ProductID", VARCHAR()),
    Column("ProductName", VARCHAR()),
    Column("CategoryID", VARCHAR()),
    Column("CategoryName", VARCHAR()),
    Column("Quantity", INTEGER()),
    Column("Price", REAL()),
    Column("Revenue",REAL())
)




RevenueFromProducts = connection.execute(table["RevenueFromProducts"].select()).fetchall()

RevenueFromOrders = connection.execute("select date(Date) as Day, OrderPayments.OrderID, Total, PaymentMethod from OrderPayments inner join OrderDates on OrderPayments.OrderID = OrderDates.OrderID and Status = 'paid'").fetchall()

ProductInStock = connection.execute(table["ProductViews"].select()).fetchall()

#DataFrame

RevenueDF = pandas.DataFrame(data=RevenueFromProducts,columns =[column.__dict__["name"] for column in table["RevenueFromProducts"].columns])

RevenueDF_2 = RevenueDF.groupby(by=["Day","CategoryName"]).sum()

RevenueDF_3 = pandas.DataFrame(data=RevenueFromOrders,columns = ["Day","OrderID","Revenue","PaymentMethod"])

RevenueDF_4 = RevenueDF.groupby(by=["Day"]).sum()

ProductDF = pandas.DataFrame(data=ProductInStock,columns = [column.__dict__["name"] for column in table["ProductViews"].columns])

RevenueByProduct = RevenueDF.groupby(by=["ProductName"]).sum()

RevenueByCategory = RevenueDF.groupby(by=["CategoryName"]).sum()

TotalRevenue = RevenueDF["Revenue"].sum()
print(RevenueByProduct.index.tolist())

day_list = RevenueDF["Day"].unique()
day_list.sort()
day_list = day_list.tolist()

product_list = RevenueDF["ProductName"].unique()
product_list.sort()
product_list = product_list.tolist()

category_list = RevenueDF["CategoryName"].unique()
category_list.sort()
category_list = category_list.tolist()

#Figure
def RevenueGroupByProductsGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    curent_height = {}
    for day in day_list:
        curent_height[day] = 0
    color_pallette = {}
    initialbar = []
    for product in product_list:
        color_pallette[product] = (random.random(),random.random(),random.random())
        initialbar.append(ax.bar(0,0,0,color = color_pallette[product],label=product))
    ax.legend(handles = initialbar)
    for index, row in RevenueDF.iterrows():
        bar = ax.bar(row["Day"],row["Revenue"],bottom=curent_height[row["Day"]], color=color_pallette[row["ProductName"]], label=row["ProductName"])
        ax.bar_label(bar,label_type="center")
        curent_height[row["Day"]] += row["Revenue"]
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue Group By Products (Total: {}(VND))".format(TotalRevenue))
    return figure

def RevenueGroupByCategoriesGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    curent_height = {}
    for day in day_list:
        curent_height[day] = 0
    color_pallette = {}
    initialbar = []
    for category in category_list:
        color_pallette[category] = (random.random(),random.random(),random.random())
        initialbar.append(ax.bar(0,0,0,color = color_pallette[category],label=category))
    ax.legend(handles = initialbar)
    for row in RevenueDF_2.iterrows():
        bar = ax.bar(row[0][0],row[1]["Revenue"],bottom=curent_height[row[0][0]], color=color_pallette[row[0][1]], label=row[0][1])
        ax.bar_label(bar,label_type = 'center')
        curent_height[row[0][0]] += row[1]["Revenue"]
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue Group By Categories(Total: {}(VND))".format(TotalRevenue))
    return figure

def RevenueGroupByOrdersGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    curent_height = {}
    for day in day_list:
        curent_height[day] = 0
    for index, row in RevenueDF_3.iterrows():
        bar = ax.bar(row["Day"], row["Revenue"], bottom=curent_height[row["Day"]])
        ax.bar_label(bar,label_type="center")
        curent_height[row["Day"]] += row["Revenue"]
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue Group By Orders(Total: {}(VND))".format(TotalRevenue))
    return figure

def RevenueByDaysGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    seaborn.lineplot(data=RevenueDF_4,x='Day',y="Revenue",ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue By Day(Total: {}(VND))".format(TotalRevenue))
    return figure

def ProductsPriceAndUnitGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    ax1 = ax.twinx()
    seaborn.barplot(data=ProductDF, x='ProductID',color = 'midnightblue', y='Unit', ax=ax,label="Unit")
    seaborn.pointplot(data=ProductDF,x='ProductID',color='gold',y="Price",ax=ax1,label="Price")

    ax.legend(loc=1)
    ax1.legend(loc=2)

    ax.set_xlabel("Product")
    ax.set_ylabel("Unit")
    ax1.set_ylabel("Price")
    ax.set_title("Product in Storage's Price and Unit(Total: {}(VND))".format(ProductDF["Unit"].multiply(ProductDF["Price"],axis=0).sum()))
    return figure

def RevenueProportionedByProducts():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    expl = [0.01] * len(RevenueByProduct)
    color_pallette = []
    for i in range(len(RevenueByProduct)):
        color_pallette.append((random.random(),random.random(),random.random()))
    ax.pie(RevenueByProduct["Revenue"].tolist(),explode= expl,colors=color_pallette,autopct = '%1.1f%%',labels=RevenueByProduct.index.tolist())
    ax.set_title("Proportion of Product in Revenue(Total: {}(VND))".format(TotalRevenue))
    return figure

#Tkinter
class Statistic:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Statistic")
        self.window.geometry("1300x800")

        self.canvas_1 = tkinter.Canvas()
        self.canvas_1.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.label_1 = tkinter.Label(self.canvas_1,text="Statistic",font=("Calibri","20"))
        self.label_1.grid(row=0, column=0, padx=15, pady=15)
        self.button_1 = tkinter.Button(self.canvas_1,text = "Revenue",command=self.set_revenue_button)
        self.button_1.grid(row = 1,column=0,padx=15,pady=15)
        self.button_1 = tkinter.Button(self.canvas_1, text="Storage", command=self.set_storage_button)
        self.button_1.grid(row=2, column=0, padx=15, pady=15)


        self.canvas_2 = tkinter.Canvas()
        self.canvas_2.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.label_2 = tkinter.Label(self.canvas_2, text="Option", font=("Calibri", "20"))
        self.label_2.grid(row=0, column=0, padx=15, pady=15)
        self.canvas_2_button = {}

        self.set_revenue_button()

        self.plot_canvas = FigureCanvasTkAgg(RevenueProportionedByProducts(),master=self.window)
        self.plot_canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        self.plot_canvas.draw()
        self.window.mainloop()

    def reset_button(self):
        for key in self.canvas_2_button.values():
            key.destroy()
        self.canvas_2_button = {}

    def clear(self):
        self.plot_canvas.get_tk_widget().destroy()
        self.plot_canvas = FigureCanvasTkAgg(master=self.window)
        self.plot_canvas.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
    def set_revenue_button(self):
        self.reset_button()
        self.canvas_2_button["button_1"] = tkinter.Button(self.canvas_2,text = "Group By Products",command=self.revenue_group_by_products)
        self.canvas_2_button["button_1"].grid(row=1,column=0, padx=15, pady=15)
        self.canvas_2_button["button_2"] = tkinter.Button(self.canvas_2, text="Group By Categories",command=self.revenue_group_by_categories)
        self.canvas_2_button["button_2"].grid(row=2,column=0, padx=15, pady=15)
        self.canvas_2_button["button_3"] = tkinter.Button(self.canvas_2, text="Group By Orders",command=self.revenue_group_by_orders)
        self.canvas_2_button["button_3"].grid(row=3, column=0, padx=15, pady=15)
        self.canvas_2_button["button_1"] = tkinter.Button(self.canvas_2, text="Proportioned By Products",command=self.revenue_proportioned_by_products)
        self.canvas_2_button["button_1"].grid(row=4, column=0, padx=15, pady=15)
    def set_storage_button(self):
        self.reset_button()
        self.canvas_2_button["button_1"] = tkinter.Button(self.canvas_2, text="Product's Unit and Price",command=self.product_unit_and_price)
        self.canvas_2_button["button_1"].grid(row=1, column=0, padx=15, pady=15)
    def revenue_group_by_categories(self):
        self.clear()
        self.plot_canvas.figure = RevenueGroupByCategoriesGraph()
        self.plot_canvas.draw()

    def revenue_group_by_products(self):
        self.clear()
        self.plot_canvas.figure = RevenueGroupByProductsGraph()
        self.plot_canvas.draw()
    def revenue_group_by_orders(self):
        self.clear()
        self.plot_canvas.figure = RevenueGroupByOrdersGraph()
        self.plot_canvas.draw()
    def revenue_proportioned_by_products(self):
        self.clear()
        self.plot_canvas.figure = RevenueProportionedByProducts()
        self.plot_canvas.draw()
    def product_unit_and_price(self):
        self.clear()
        self.plot_canvas.figure = ProductsPriceAndUnitGraph()
        self.plot_canvas.draw()

s = Statistic()



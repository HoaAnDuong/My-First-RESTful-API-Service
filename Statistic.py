from api_and_table import *
import pandas
import seaborn
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
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

OrderCountByDateAndStatus = connection.execute("select date(Date) as Day, Status, count(OrderPayments.OrderID) from OrderPayments inner join OrderDates on OrderPayments.OrderID = OrderDates.OrderID group by Day,Status;").fetchall()

RevenueFromOrders = connection.execute("select date(Date) as Day, OrderPayments.OrderID, Total, PaymentMethod from OrderPayments inner join OrderDates on OrderPayments.OrderID = OrderDates.OrderID and Status = 'paid'").fetchall()



ProductInStock = connection.execute(table["ProductViews"].select()).fetchall()

OrderPayments = connection.execute(table["OrderPayments"].select()).fetchall()
#DataFrame

RevenueDF = pandas.DataFrame(data=RevenueFromProducts,columns =[column.__dict__["name"] for column in table["RevenueFromProducts"].columns])

RevenueDF_3 = pandas.DataFrame(data=RevenueFromOrders,columns = ["Day","OrderID","Revenue","PaymentMethod"])

ProductDF = pandas.DataFrame(data=ProductInStock,columns = [column.__dict__["name"] for column in table["ProductViews"].columns])

OrderPaymentDF = pandas.DataFrame(data=OrderPayments,columns = [column.__dict__["name"] for column in table["OrderPayments"].columns])

ProductDF["Total"] = ProductDF["Unit"].multiply(ProductDF["Price"])

OrderCountByDateAndStatus = pandas.DataFrame(data = OrderCountByDateAndStatus,columns = ["Day","Status","Count"])

RevenueDF_2 = RevenueDF.groupby(by=["Day","CategoryName"]).sum()
RevenueByDay = RevenueDF.groupby(by=["Day"]).sum()
RevenueByProduct = RevenueDF.groupby(by=["ProductName"]).sum()
RevenueByCategories = RevenueDF.groupby(by=["CategoryName"]).sum()

TotalByCategories = ProductDF.groupby(by=["CategoryName"]).sum()
TotalRevenue = RevenueDF["Revenue"].sum()
TotalStorage = ProductDF["Unit"].multiply(ProductDF["Price"],axis=0).sum()


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
    ax.set_title("Revenue Group By Products \n(Total: {} VND)".format(TotalRevenue))
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
    ax.set_title("Revenue Group By Categories\n(Total: {} VND)".format(TotalRevenue))
    return figure

def RevenueGroupByOrdersGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    curent_height = {}
    for day in day_list:
        curent_height[day] = 0
    for index, row in RevenueDF_3.iterrows():
        bar = ax.bar(row["Day"], row["Revenue"],color = (random.random(),random.random(),random.random()), bottom=curent_height[row["Day"]])
        ax.bar_label(bar,label_type="center")
        curent_height[row["Day"]] += row["Revenue"]
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue Group By Orders\n(Total: {} VND)".format(TotalRevenue))
    return figure

def RevenueByDaysGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    days = RevenueByDay.index.tolist()
    revenues =RevenueByDay["Revenue"].tolist()
    bars = ax.bar(days, revenues,color=(random.random(),random.random(),random.random()))
    ax.bar_label(bars,label_type='center')
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue(VND)")
    ax.set_title("Revenue By Day\n(Total: {} VND)".format(TotalRevenue))
    return figure

def StorageProductsPriceAndUnitGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    ax1 = ax.twinx()
    seaborn.barplot(data=ProductDF, x='ProductID',color = (random.random(),random.random(),random.random()), y='Unit', ax=ax,label="Unit")
    for i in ax.containers:
        ax.bar_label(i,label_type='center')
    seaborn.pointplot(data=ProductDF,x='ProductID',color=(random.random(),random.random(),random.random()),y="Price",ax=ax1,label="Price")

    ax.legend(loc=1)
    ax1.legend(loc=2)

    ax.set_xlabel("Product")
    ax.set_ylabel("Unit")
    ax1.set_ylabel("Price")
    ax.set_title("Product in Storage's Price and Unit\n(Total: {} VND)".format(TotalStorage))
    return figure

def RevenueProportionedByProducts():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    expl = [0.01] * len(RevenueByProduct)
    color_pallette = []
    for i in range(len(RevenueByProduct)):
        color_pallette.append((random.random(),random.random(),random.random()))
    label_list = []
    revenues = RevenueByProduct["Revenue"].tolist()
    products = RevenueByProduct.index.tolist()
    label_list = [ f'{p} ({r} VND)' for p,r in zip(products,revenues)]
    ax.pie(revenues,explode= expl,colors=color_pallette,autopct = '%1.1f%%',labels=label_list)
    ax.legend(loc = 'lower left',bbox_to_anchor=(0.4,-0.1))
    ax.set_title("Proportion of Product in Revenue\n(Total: {} VND)".format(TotalRevenue))
    return figure

def RevenueProportionedByCategories():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    expl = [0.01] * len(RevenueByCategories)
    color_pallette = []
    for i in range(len(RevenueByCategories)):
        color_pallette.append((random.random(),random.random(),random.random()))
    label_list = []
    revenues = RevenueByCategories["Revenue"].tolist()
    categories = RevenueByCategories.index.tolist()
    label_list = [f'{c} ({r} VND)' for c,r in zip(categories, revenues)]
    ax.pie(revenues, explode=expl, colors=color_pallette, autopct='%1.1f%%', labels=label_list)
    ax.legend(loc='lower left', bbox_to_anchor=(0.6, -0.1))
    ax.set_title("Proportion of Product in Revenue\n(Total: {} VND)".format(TotalRevenue))
    return figure

def StorageTotalPropotionedByProducts():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    expl = [0.01] * len(ProductDF)
    color_pallette = []
    for i in range(len(ProductDF)):
        color_pallette.append((random.random(), random.random(), random.random()))
    label_list = []
    for i,row in ProductDF.iterrows():
        label_list.append("{} ({} VND)".format(row["ProductName"],row["Total"]))
    ax.pie(ProductDF["Total"].tolist(), explode=expl, colors=color_pallette, autopct='%1.1f%%',
           labels=label_list)
    ax.legend(loc='lower left', bbox_to_anchor=(0.4, -0.1))
    ax.set_title("Proportion of Products in Storage's Total Value\n(Total: {} VND)".format(TotalStorage))
    return figure

def StorageTotalPropotionedByCategories():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    expl = [0.01] * len(TotalByCategories)
    color_pallette = []
    for i in range(len(TotalByCategories)):
        color_pallette.append((random.random(), random.random(), random.random()))
    label_list = []
    totals = TotalByCategories["Total"].tolist()
    categories = TotalByCategories.index.tolist()
    label_list = [f'{c} ({r} VND)' for c, r in zip(categories, totals)]
    ax.pie(totals, explode=expl, colors=color_pallette, autopct='%1.1f%%', labels=label_list)
    ax.legend(loc='lower left', bbox_to_anchor=(0.6, -0.1))
    ax.set_title("Proportion of Categories in Storage's Total Value\n(Total: {} VND)".format(TotalStorage))
    return figure
def ProductsPurchasingTendencyGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    ax1 = ax.twinx()
    color_pallette = []
    for i in range(len(product_list)):
        color_pallette.append((random.random(), random.random(), random.random()))
    seaborn.barplot(data = RevenueDF,x='Day',y='Quantity',palette=color_pallette,hue = 'ProductName',ax=ax)
    for i in ax.containers:
        ax.bar_label(i,label_type='center')
    seaborn.pointplot(data = RevenueDF,x="Day",y='Revenue',palette=color_pallette,hue='ProductName',ax=ax1)
    seaborn.lineplot(data=RevenueByDay,x = "Day", y='Revenue', color = (random.random(),random.random(),random.random()), ax=ax1,label="Total")
    ax.legend(loc = 2,title="Quantity")
    ax1.legend(loc = 6,title="Revenue")
    ax1.set_ylabel("Revenue(VND)")
    ax.set_xlabel("Day")
    ax.set_ylabel("Quantity")
    ax.set_title("Products Purchasing Tendency\n(Total: {} VND)".format(TotalRevenue))
    return figure

def CategoriesPurchasingTendencyGraph():
    figure = Figure(dpi=100)
    ax = figure.subplots()
    ax1 = ax.twinx()
    color_pallette = []
    for i in range(len(category_list)):
        color_pallette.append((random.random(), random.random(), random.random()))
    seaborn.barplot(data=RevenueDF, x='Day', y='Quantity', palette=color_pallette, hue='CategoryName', ax=ax)
    for i in ax.containers:
        ax.bar_label(i,label_type='center')
    seaborn.pointplot(data=RevenueDF,x="Day", y='Revenue', palette=color_pallette,hue = 'CategoryName', ax=ax1)
    seaborn.lineplot(data=RevenueByDay, x='Day', y='Revenue', color=(random.random(), random.random(), random.random()),ax=ax1, label="Total")
    ax.legend(loc=2, title="Quantity")
    ax1.legend(loc=6, title="Revenue")
    ax1.set_ylabel("Revenue(VND)")
    ax.set_xlabel("Day")
    ax.set_ylabel("Quantity")
    ax.set_title("Categories Purchasing Tendency\n(Total: {} VND)".format(TotalRevenue))
    return figure

def PaymentMethodTendencyGraph():
    figure = Figure(dpi=100)
    ax,ax2,ax3 = figure.subplots(3,1)

    RevenueGroupByPaymentMethod = OrderPaymentDF[OrderPaymentDF["Status"]=="paid"].groupby(by="PaymentMethod").sum()
    PaymentMethodCount = OrderPaymentDF[OrderPaymentDF["Status"]=="paid"].groupby(by="PaymentMethod").count()

    payment_method = RevenueGroupByPaymentMethod.index.tolist()
    revenue = RevenueGroupByPaymentMethod["Total"].tolist()
    count = PaymentMethodCount["OrderID"].tolist()

    label_list_1 = ["{} ({} VND)".format(p,r) for p,r in zip(payment_method,revenue)]
    label_list_2 = ["{} (Count: {})".format(p, c) for p, c in zip(payment_method, count)]
    expl = len(payment_method)*[0.01]
    color_pallette = []
    for i in range(len(payment_method)):
        color_pallette.append((random.random(),random.random(),random.random()))

    ax.pie(revenue, explode=expl, colors=color_pallette, autopct='%1.1f%%', labels=label_list_1)
    ax2.pie(count, explode=expl, colors=color_pallette, autopct='%1.1f%%', labels=label_list_2)
    seaborn.countplot(data = RevenueDF_3,x='Day',hue='PaymentMethod',palette = color_pallette,ax=ax3)
    for i in ax3.containers:
        ax3.bar_label(i,label_type='center')
    ax.legend(loc='lower left', bbox_to_anchor=(1.1, 0.2))
    ax2.legend(loc='lower left', bbox_to_anchor=(1.1, 0.2))
    ax.set_title("Revenue Proportioned By PaymentMethod (Total: {} VND)".format(sum(revenue)))
    ax2.set_title("Payment Method Proportion (Count: {})".format(sum(count)))
    ax3.set_title("Payment Method Group By Day (Count: {})".format(sum(count)))
    return figure

def StatusTendencyGraph():
    OrderCountByStatus = OrderCountByDateAndStatus.groupby(by = 'Status').sum()
    figure = Figure()
    ax,ax2 = figure.subplots(2,1)

    status = OrderCountByStatus.index.tolist()
    count = OrderCountByStatus["Count"].tolist()
    label_list = ["{} (Count: {})".format(s, c) for s, c in zip(status, count)]
    color_pallette = []
    for i in range(len(status)):
        color_pallette.append((random.random(),random.random(),random.random()))
    expl = len(status) * [0.05]

    seaborn.barplot(data = OrderCountByDateAndStatus,x = 'Day',y = 'Count',hue = 'Status',palette=color_pallette,ax=ax2)
    for i in ax2.containers:
        ax2.bar_label(i,label_type = 'center')
    ax.pie(count, explode=expl, colors=reversed(color_pallette), autopct='%1.1f%%', labels=label_list)

    ax2.legend()
    ax.legend(loc='lower left', bbox_to_anchor=(1.1, 0.2))
    ax2.set_title("Order's Status Group by Day\n(Count: {})".format(sum(count)))
    ax.set_title("Order's Status Proportion\n(Count: {})".format(sum(count)))
    return figure


#Tkinter
class Statistic:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Statistic")
        self.window.geometry("1300x800")

        self.canvas_1 = tkinter.Canvas()
        self.canvas_1.pack(side=tkinter.LEFT,fill = tkinter.Y, expand=False)
        self.label_1 = tkinter.Label(self.canvas_1,text="Field",font=("Calibri","20"))
        self.label_1.grid(row=0, column=0, padx=15, pady=15)
        self.button_1 = tkinter.Button(self.canvas_1,text = "Revenue",command=self.set_revenue_button)
        self.button_1.grid(row = 1,column=0,padx=15,pady=15)
        self.button_1 = tkinter.Button(self.canvas_1, text="Storage", command=self.set_storage_button)
        self.button_1.grid(row=2, column=0, padx=15, pady=15)
        self.button_1 = tkinter.Button(self.canvas_1, text="Tendency", command=self.set_tendency_button)
        self.button_1.grid(row=3, column=0, padx=15, pady=15)


        self.canvas_2 = tkinter.Canvas(width=10)
        self.canvas_2.pack(side=tkinter.LEFT,fill = tkinter.Y, expand=False)
        self.label_2 = tkinter.Label(self.canvas_2, text="Option", font=("Calibri", "20"))
        self.label_2.grid(row=0, column=0, padx=5, pady=15)
        self.canvas_2_button = {}

        self.set_revenue_button()

        self.plot_canvas = FigureCanvasTkAgg(StatusTendencyGraph(),master=self.window)
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
        self.canvas_2_button["button_1"].grid(row=1,column=0, padx=5, pady=15)
        self.canvas_2_button["button_2"] = tkinter.Button(self.canvas_2, text="Group By Categories",command=self.revenue_group_by_categories)
        self.canvas_2_button["button_2"].grid(row=2,column=0, padx=5, pady=15)
        self.canvas_2_button["button_3"] = tkinter.Button(self.canvas_2, text="Group By Orders",command=self.revenue_group_by_orders)
        self.canvas_2_button["button_3"].grid(row=3, column=0, padx=5, pady=15)
        self.canvas_2_button["button_4"] = tkinter.Button(self.canvas_2, text="Proportioned By Products",command=self.revenue_proportioned_by_products)
        self.canvas_2_button["button_4"].grid(row=4, column=0, padx=5, pady=15)
        self.canvas_2_button["button_5"] = tkinter.Button(self.canvas_2, text="Proportioned By Categories",command=self.revenue_proportioned_by_categories)
        self.canvas_2_button["button_5"].grid(row=5, column=0, padx=5, pady=15)
        self.canvas_2_button["button_6"] = tkinter.Button(self.canvas_2, text="Group By Day",
                                                          command=self.revenue_group_by_days)
        self.canvas_2_button["button_6"].grid(row=6, column=0, padx=5, pady=15)
    def set_storage_button(self):
        self.reset_button()
        self.canvas_2_button["button_1"] = tkinter.Button(self.canvas_2, text="Product's Unit and Price",command=self.product_unit_and_price)
        self.canvas_2_button["button_1"].grid(row=1, column=0, padx=15, pady=15)
        self.canvas_2_button["button_2"] = tkinter.Button(self.canvas_2, text="Total proportioned by Product",
                                                          command=self.storage_total_proportioned_by_products)
        self.canvas_2_button["button_2"].grid(row=2, column=0, padx=15, pady=15)
        self.canvas_2_button["button_3"] = tkinter.Button(self.canvas_2, text="Total proportioned by Categories",
                                                          command=self.storage_total_proportioned_by_categories)
        self.canvas_2_button["button_3"].grid(row=3, column=0, padx=15, pady=15)
    def set_tendency_button(self):
        self.reset_button()
        self.canvas_2_button["button_1"] = tkinter.Button(self.canvas_2, text="Products Tendency",
                                                          command=self.products_purchasing_tendency)
        self.canvas_2_button["button_1"].grid(row=1, column=0, padx=15, pady=15)
        self.canvas_2_button["button_2"] = tkinter.Button(self.canvas_2, text="Categories Tendency",
                                                          command=self.categories_purchasing_tendency)
        self.canvas_2_button["button_2"].grid(row=2, column=0, padx=15, pady=15)
        self.canvas_2_button["button_3"] = tkinter.Button(self.canvas_2, text="Payment Method Tendency",
                                                          command=self.payment_method_tendency)
        self.canvas_2_button["button_3"].grid(row=3, column=0, padx=15, pady=15)
        self.canvas_2_button["button_4"] = tkinter.Button(self.canvas_2, text="Status Tendency",
                                                          command=self.status_tendency)
        self.canvas_2_button["button_4"].grid(row=4, column=0, padx=15, pady=15)
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
    def revenue_group_by_days(self):
        self.clear()
        self.plot_canvas.figure = RevenueByDaysGraph()
        self.plot_canvas.draw()
    def revenue_proportioned_by_products(self):
        self.clear()
        self.plot_canvas.figure = RevenueProportionedByProducts()
        self.plot_canvas.draw()
    def revenue_proportioned_by_categories(self):
        self.clear()
        self.plot_canvas.figure = RevenueProportionedByCategories()
        self.plot_canvas.draw()
    def product_unit_and_price(self):
        self.clear()
        self.plot_canvas.figure = StorageProductsPriceAndUnitGraph()
        self.plot_canvas.draw()
    def storage_total_proportioned_by_products(self):
        self.clear()
        self.plot_canvas.figure = StorageTotalPropotionedByProducts()
        self.plot_canvas.draw()
    def storage_total_proportioned_by_categories(self):
        self.clear()
        self.plot_canvas.figure = StorageTotalPropotionedByCategories()
        self.plot_canvas.draw()
    def products_purchasing_tendency(self):
        self.clear()
        self.plot_canvas.figure = ProductsPurchasingTendencyGraph()
        self.plot_canvas.draw()
    def categories_purchasing_tendency(self):
        self.clear()
        self.plot_canvas.figure = CategoriesPurchasingTendencyGraph()
        self.plot_canvas.draw()

    def payment_method_tendency(self):
        self.clear()
        self.plot_canvas.figure = PaymentMethodTendencyGraph()
        self.plot_canvas.draw()

    def status_tendency(self):
        self.clear()
        self.plot_canvas.figure = StatusTendencyGraph()
        self.plot_canvas.draw()
s = Statistic()



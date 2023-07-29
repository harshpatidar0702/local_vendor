from flask import Flask, render_template, request, session
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "mySecretKey"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "local_vendor"

db = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/adminlogin")
def adminloginpage():
    return render_template("adminlogin.html")


@app.route("/customerlogin")
def customerlogin():
    return render_template("customerlogin.html")


@app.route("/vendorlogin")
def vendorlogin():
    return render_template("vendorlogin.html")


@app.route("/signincustomer")
def signin():
    return render_template("customersignin.html")


@app.route("/adminsignin")
def adminsignin():
    return render_template("adminsignin.html")


@app.route("/customersignin")
def signup():
    return render_template("customersignin.html")


@app.route("/vendorsignin")
def vendorsignin():
    return render_template("vendorsignin.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/customerloginpage", methods=["GET", "POST"])
def customerloginpage():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM CUSTOMER WHERE username = %s AND password = %s",
            (username, password),
        )
        session['data'] = username
        if cursor.fetchone():
            qr = "SELECT shop_name,shop_category,shop_address,phone_no,shop_id FROM VENDOR"
            cursor.execute(qr)
            vendor_det = cursor.fetchall()
            return render_template("customerpage.html", ved_data=vendor_det)
        else:
            return render_template("customerlogin.html")
    else:
        return render_template("customerlogin.html")


@app.route("/customerpage", methods=["GET", "POST"])
def customerpage():
    if request.method.upper() == "POST":
        data = request.form
        query = "INSERT INTO CUSTOMER VALUES (%s,%s,%s,%s,%s)"
        cursor_obj = db.connection.cursor()
        username = data["username"]
        email = data["email"]
        password = data["password"]
        address = data["address"]
        phone_number = data["phone_number"]
        valu = (username, email, password, address, phone_number)
        cursor_obj.execute(query, valu)
        db.connection.commit()
        qr = "SELECT shop_name,shop_category,shop_address,phone_no,shop_id FROM VENDOR"
        cursor = db.connection.cursor()
        cursor.execute(qr)
        vendor_dat = cursor.fetchall()
        print(vendor_dat)
        cursor_obj.close()
    else:
        print("connection failed !!")
    return render_template("customerpage.html", ved_data=vendor_dat)


@app.route("/customercart")
def customerorder():
    return render_template("customercart.html")


@app.route("/customerorder")
def customercart():
    cursor = db.connection.cursor()
    # var = request.form
    cust_name = session.get('data')
    query = f"SELECT product_name,product_price,shop_id FROM allorder WHERE customer_name=%s"
    cursor.execute(query, (cust_name,))
    orders = cursor.fetchall()
    db.connection.commit()
    return render_template("customerorder.html", order=orders)


@app.route("/adminsigin", methods=["GET", "POST"])
def adminpage():
    if request.method.upper() == "POST":
        data = request.form
        query1 = "SELECT COUNT(s_no) FROM ADMIN"
        query = "INSERT INTO ADMIN VALUES (%s,%s, %s)"
        cursor_obj = db.connection.cursor()
        cursor_obj.execute(query1)
        j = cursor_obj.fetchone()[0]
        j = j + 1
        username = data["username"]
        password = data["password"]
        val = (j, username, password)
        cursor_obj.execute(query, val)
        db.connection.commit()
        cursor_obj.close()
        return render_template("adminpage.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if (request.method == "POST" and "username" in request.form and "password" in request.form):
        username = request.form["username"]
        password = request.form["password"]
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM ADMIN WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        if cursor.fetchone():
            return render_template("adminpage.html")
        else:
            return render_template("adminlogin.html")
    else:
        return render_template("adminlogin.html")


@app.route("/vendorpage", methods=["GET", "POST"])
def vendorpage():
    if request.method.upper() == "POST":
        data = request.form
        query1 = "SELECT COUNT(*) FROM VENDOR"
        query = "INSERT INTO VENDOR VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )"
        cursor_obj = db.connection.cursor()
        cursor_obj.execute(query1)
        i = cursor_obj.fetchone()[0]
        i = i + 1
        name = data["name"]
        email = data["email"]
        password = data["password"]
        shop_name = data["shop_name"]
        shop_id = data["shop_id"]
        shop_category = data["shop_category"]
        shop_address = data["shop_address"]
        shop_details = data["shop_details"]
        phone_no = data["phone_no"]

        val = (
            i,
            name,
            email,
            password,
            shop_name,
            shop_id,
            shop_category,
            shop_address,
            shop_details,
            phone_no,
        )
        cursor_obj.execute(query, val)
        db.connection.commit()
        cursor_obj.close()
        return render_template("vendorpage.html")
    else:
        print("connection failed !!")
    return render_template("home.html")

# Global variable used for product_fk
shop_id = 0


@app.route("/vendorloginpage", methods=["GET", "POST"])
def vendorloginpage():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT * FROM VENDOR  WHERE name = %s AND password = %s",
            (username, password),
        )
        if cursor.fetchone():
            cursor.execute(
                "SELECT SHOP_ID FROM VENDOR WHERE name = %s AND password = %s",
                (username, password),
            )
            global shop_id
            shop_id = cursor.fetchone()
            return render_template("vendorpage.html")
        else:
            return render_template("vendorlogin.html")

    else:
        return render_template("vendorlogin.html")


@app.route("/vendoraddproduct", methods=["GET", "POST"])
def addproduct():
    if request.method.upper() == "POST":
        data = request.form
        query1 = "SELECT COUNT(*) FROM PRODUCT"
        query = "INSERT INTO PRODUCT VALUES (%s,%s,%s,%s,%s,%s)"
        cursor_obj = db.connection.cursor()
        cursor_obj.execute(query1)
        i = cursor_obj.fetchone()[0]
        i=i+1
        product_name = data["product_name"]
        product_category = data["product_category"]
        product_price = data["product_price"]
        product_description = data["product_description"]
        val = (
            i,
            product_name,
            product_category,
            product_price,
            product_description,
            shop_id,
        )
        cursor_obj.execute(query, val)
        db.connection.commit()
        cursor_obj.close()
        return render_template("addproductpopup.html")

@app.route("/vendorhomepage")
def vendordashbord():
    return render_template("vendorpage.html")


@app.route("/vendororder")
def vendororder():
    cursor = db.connection.cursor()
    query = f"SELECT product_name,product_price,customer_name FROM `CARTS` WHERE carts.shop_id=%s"
    cursor.execute(query,(shop_id,))
    order = cursor.fetchall()
    db.connection.commit()
    return render_template("vendororder.html", order=order)


@app.route("/vendorsale", methods=["GET", "POST"])
def vendorsale():
    pdf = request.form
    pdf_fil = pdf['filename']
    pdf_file = pdf_fil+".pdf"
    cursor = db.connection.cursor()
    query = f" SELECT shop_id,product_name,product_price FROM allorder WHERE shop_id=%s"
    cursor.execute(query, (shop_id,))
    data_tuple = cursor.fetchall()
    db.connection.commit()

    total_price = sum(price for _, _, price in data_tuple)

    df = pd.DataFrame(data_tuple, columns=['Shop ID', 'Product Name', 'Product Price'])

    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.setFont('Helvetica', 12)
    c.drawString(50, 750, 'Project Report')
    c.line(50, 745, 550, 745)

    header = ['Shop ID', 'Product Name', 'Product Price']
    x_start = 50
    y_start = 720
    x_offset = 150
    y_offset = 30

    for i, header_item in enumerate(header):
        c.drawString(x_start + (i * x_offset), y_start, header_item)

    for i, row in df.iterrows():
        y_start -= y_offset
        c.drawString(x_start, y_start, row['Shop ID'])
        c.drawString(x_start + x_offset, y_start, row['Product Name'])
        c.drawString(x_start + (2 * x_offset), y_start, str(row['Product Price']))

    y_start -= (2 * y_offset)
    c.drawString(x_start, y_start, 'Total Price:')
    c.drawString(x_start + (2 * x_offset), y_start, str(total_price))
    c.save()
    return render_template("reportdownloadpopup.html")


@app.route("/filename")
def filename():
    return render_template("filename.html")

@app.route("/admin_report", methods=["GET", "POST"])
def admin_report():
    pdf = request.form
    pdf_fil = pdf['filename']
    pdf_file = pdf_fil + ".pdf"
    s_id = request.form
    shop_id= s_id["shop_id"]
    cursor = db.connection.cursor()
    query = "SELECT shop_id,product_name,product_price FROM allorder WHERE shop_id=%s"
    cursor.execute(query,(shop_id,))
    data = cursor.fetchall()
    db.connection.commit()

    total_price = sum(price for _, _, price in data)

    df = pd.DataFrame(data, columns=['Shop ID', 'Product Name', 'Product Price'])

    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.setFont('Helvetica', 12)
    c.drawString(50, 750, 'Project Report')
    c.line(50, 745, 550, 745)
    header = ['Shop ID', 'Product Name', 'Product Price']
    x_start = 50
    y_start = 720
    x_offset = 150
    y_offset = 30

    for i, header_item in enumerate(header):
        c.drawString(x_start + (i * x_offset), y_start, header_item)

    for i, row in df.iterrows():
        y_start -= y_offset
        c.drawString(x_start, y_start, row['Shop ID'])
        c.drawString(x_start + x_offset, y_start, row['Product Name'])
        c.drawString(x_start + (2 * x_offset), y_start, str(row['Product Price']))

    y_start -= (2 * y_offset)
    c.drawString(x_start, y_start, 'Total Price:')
    c.drawString(x_start + (2 * x_offset), y_start, str(total_price))
    c.save()

    return render_template("reportdownloadpopup.html")



@app.route("/viewproduct", methods=["GET", "POST"])
def viewProduct():
    cursor = db.connection.cursor()
    s_id = request.form
    s_id1 = s_id["shop_id"]
    query = f"SELECT product_no,product_name,product_description,product_price FROM product,vendor WHERE product.shop_id=vendor.shop_id AND product.shop_id=%s"
    cursor.execute(query, (s_id1,))
    product = cursor.fetchall()
    cursor.close()
    return render_template("viewproduct.html", product_data=product, id=s_id1)


@app.route("/vendordata")
def vedorInfDisp():
    cursor = db.connection.cursor()
    query = "SELECT name,email,phone_no,shop_category,shop_id FROM vendor"
    cursor.execute(query)
    vendor_data = cursor.fetchall()
    # print(vendor_data)
    cursor.close()
    return render_template("admin_vendor.html", data=vendor_data)


@app.route("/addcart", methods=["GET", "POST"])
def addToCart():
    query = "INSERT INTO CARTS VALUES(%s,%s,%s,%s,%s)"
    var = request.form
    cust_name = session.get('data')
    product_no = var["product_no"]
    product_name = var["product_name"]
    product_price = var["product_price"]
    shop_id = var["sh_id"]
    val = (product_no, product_name, product_price, shop_id,cust_name)
    cursor_obj = db.connection.cursor()
    cursor_obj.execute(query, val)
    db.connection.commit()
    return render_template("customercart.html")


@app.route("/displayincart")
def displayInCart():
    cursor = db.connection.cursor()
    query = "SELECT product_no,product_name,product_price FROM carts"
    cursor.execute(query)
    dis = cursor.fetchall()
    return render_template("customercart.html", cart=dis)


@app.route("/chechoutpopup")
def checkoutpopup():
    cursor = db.connection.cursor()
    cursor1 = db.connection.cursor()
    query="SELECT SUM(product_price) FROM `CARTS`"
    cursor.execute(query)
    sum = cursor.fetchone()[0]
    db.connection.commit()
    sum1 = int(sum)
    query1 = "SELECT product_no,product_name,product_price,shop_id,customer_name FROM carts"
    query2 = "INSERT INTO allorder values(%s,%s,%s,%s,%s)"
    query3 = " Select count(*) FROM CARTS"
    cursor.execute(query3)
    count = cursor.fetchone()[0]
    db.connection.commit()
    cursor.execute(query1)
    data = cursor.fetchall()

    for inner_tuple in data:
        cursor1.execute(query2 , inner_tuple)
        db.connection.commit()
    return render_template("orderplacedpopup.html", sum=sum1)


@app.route("/admin_customer")
def admin_customer():
    cursor = db.connection.cursor()
    query = "SELECT username,Email,Address,Phone_Number FROM customer"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("admin_customer.html", data=data)


@app.route("/clear_cart", methods=["GET", "POST"])
def remove_item_from_cart():
    cursor = db.connection.cursor()
    var = request.form
    k = var
    # print(k)
    p_id = var["pid"]
    # print(p_id)
    query = f"DELETE  FROM `CARTS` WHERE carts.product_name='%s'"% p_id
    cursor.execute(query)
    db.connection.commit()
    qr = "SELECT shop_name,shop_category,shop_address,phone_no,shop_id FROM VENDOR"
    cursor.execute(qr)
    vendor_det = cursor.fetchall()
    # print(vendor_det)
    return render_template("customerpage.html", ved_data=vendor_det)


@app.route("/vendor_product")
def vendor_product():
    cursor = db.connection.cursor()
    query = f"SELECT product_name,product_category,product_description,product_price FROM product WHERE product.shop_id=%s "
    cursor.execute(query,(shop_id,))
    var = cursor.fetchall()
    # print(var)
    return render_template("vendor_product.html", data=var)

@app.route("/remove_product",methods=["POST"])
def remove_project():
    query = f"Delete FROM PRODUCT WHERE product.shop_id=%s AND product.product_name=%s  "
    rem = request.form
    var = rem["Product_Name"]
    cursor =db.connection.cursor()
    cursor.execute(query,(shop_id,var,))
    db.connection.commit()
    return render_template("productremovepopup.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

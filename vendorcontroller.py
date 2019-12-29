from models import *
from flask import request,render_template

def dummy_vendor():
    return Vendor(id=0,name='',email='')

@app.route("/vendor/welcome/",methods=["GET"])
def vendor_welcome():
    return render_template(
        'vendor.html',
        vendors=Vendor.query.all(),
        ven=dummy_vendor()
    )

@app.route("/vendor/save/",methods=["POST"])
def add_vendor():
    op = ''
    vid=int(request.form["vid"]) #0 -- >111
    if vid==0:
        vendor = Vendor(name=request.form["vname"], email=request.form["vemail"])
        db.session.add(vendor)
        db.session.commit() #vendor.id -- 1
        op='added'
        vid=vendor.id
    else:
        op = 'updated'
        dbven = Vendor.query.filter_by(id=request.form['vid']).first()
        dbven.name=request.form["vname"]
        dbven.email=request.form["vemail"]

        db.session.commit()
    return render_template(
        'vendor.html',
        vendors = Vendor.query.all(),
        ven = dummy_vendor(),
        msg = "Vendor <{}> {} successfully....!".format(vid,op)
        )


@app.route("/vendor/edit/<int:vid>",methods=["GET"])
def edit_vendor(vid):
    return render_template(
        'vendor.html',
        vendors=Vendor.query.all(),
        ven=Vendor.query.filter_by(id=vid).first()
    )


@app.route("/vendor/delete/<int:vid>",methods=["GET"])
def remove_vendor(vid):
    venOb = Vendor.query.filter_by(id=vid).first()
    db.session.delete(venOb)
    db.session.commit()
    return render_template(
        'vendor.html',
        vendors=Vendor.query.all(),
        ven=dummy_vendor(),
        msg="Vendor record removed Successfully...!"
    )

#-----------------------------------------------------------


def dummy_product():
    return Product(id=0,name='',price=0.0,qty=0)

@app.route("/product/welcome/",methods=["GET"])
def product_welcome():
    return render_template(
        'product.html',
        products=Product.query.all(),
        prod=dummy_product(),
        vendors = Vendor.query.all()
    )

@app.route("/product/save/",methods=["POST"])
def add_product():
    op = ''
    pid=int(request.form["pid"]) #0 -- >111

    if pid==0:
        if int(request.form["ven"])==0:
            product = Product(pid = 0,name=request.form["pname"],
                              price=request.form["pprice"],
                              qty=request.form["pqty"],
                              vid=0)
            return render_template(
                'product.html',
                vendors=Vendor.query.all(),
                products=Product.query.all(),
                prod=product,
                msg="Select Vendor...mandatory field.."
            )

        product = Product(name=request.form["pname"],
                          price=request.form["pprice"],
                          qty=request.form["pqty"],
                          vid=request.form["ven"])
        db.session.add(product)
        db.session.commit() #vendor.id -- 1
        op='added'
        pid=product.id
    else:
        op = 'updated'
        dbprod = Product.query.filter_by(id=request.form['pid']).first()
        dbprod.name=request.form["pname"]
        dbprod.price=request.form["pprice"]
        dbprod.qty = request.form["pqty"]
        db.session.commit()
    return render_template(
        'product.html',
        vendors=Vendor.query.all(),
        products = Product.query.all(),
        prod = dummy_product(),
        msg = "Product <{}> {} successfully....!".format(pid,op)
        )


@app.route("/product/edit/<int:pid>",methods=["GET"])
def edit_product(pid):
    return render_template(
        'product.html',
        vendors=Vendor.query.all(),
        products=Product.query.all(),
        prod=Product.query.filter_by(id=pid).first()
    )


@app.route("/product/delete/<int:pid>",methods=["GET"])
def remove_product(pid):
    prodOb = Product.query.filter_by(id=pid).first()
    db.session.delete(prodOb)
    db.session.commit()
    return render_template(
        'product.html',
        vendors=Vendor.query.all(),
        products=Product.query.all(),
        prod=dummy_product(),
        msg="Product {} record removed Successfully...!".format(pid)
    )



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
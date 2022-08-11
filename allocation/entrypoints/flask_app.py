from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.adapters import orm
from allocation import bootstrap
from allocation.domain import model, commands

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    cmd = commands.CreateBatch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta
    )
    bus.handle(cmd)
    return "OK", 201


def create_app():
    print(f"entro:{config.get_postgres_uri()}")
    Session = sessionmaker(
        bind=create_engine(
            config.get_postgres_uri(),
            isolation_level="REPEATABLE READ",
        )
    )
    orm.start_mappers()

    # create a Session
    session = Session()

    """b1 = model.Batch(ref="b1", sku="sku1", qty=100, eta=None)
    b2 = model.Batch(ref="b2", sku="sku1", qty=100, eta=None)
    b3 = model.Batch(ref="b3", sku="sku2", qty=100, eta=None)
    p1 = model.Product(sku="sku1", batches=[b1, b2])
    p2 = model.Product(sku="sku2", batches=[b3])
    session.add(p1)
    session.add(p2)
    session.commit()"""

    product = session.query(model.Product).filter_by(sku='sku2').first()

    print(product)


if __name__ == "__main__":
    app.run(debug=True)
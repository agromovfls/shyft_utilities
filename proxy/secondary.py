import pyhs2
import json
config = json.load(open("config.json", "r"))

with pyhs2.connect(
        host=config["host"],
        port=10000,
        authMechanism="NONE",
        user=config["user"],
        password=config["password"],
        database=config["database"]) as conn:
    with conn.cursor() as cur:
        #Show databases
        print cur.getDatabases()

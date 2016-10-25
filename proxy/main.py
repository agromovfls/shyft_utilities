from pyhive import hive
from TCLIService.ttypes import TOperationState
import json

config = json.load(open("config.json", "r"))["hive"]

cursor = hive.connect(
    host=config["host"],
    port=10000,
    username=config["user"],
    database=config["database"],
    auth="NONE"
).cursor()
cursor.execute('SELECT * FROM t2 LIMIT 10', async=True)

status = cursor.poll().operationState
while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
    logs = cursor.fetch_logs()
    for message in logs:
        print message

    # If needed, an asynchronous query can be cancelled at any time with:
    # cursor.cancel()

    status = cursor.poll().operationState

print cursor.fetchall()

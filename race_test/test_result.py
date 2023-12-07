import re
from subprocess import call

with open("./race_test/statuscodes/cell_status.txt", mode="rt+") as f:
    lines = f.readlines()
    results = {}
    for line in lines:
        user = re.findall(r"user\S+", line)
        status, process_id, thread_id = re.findall(r"\d+", line)
        if str(user) not in results:
            results[str(user)] = {
                "status_201": 1,
                "process_id": [
                    process_id,
                ],
                "thread_id": [
                    thread_id,
                ],
            }
        else:
            results[str(user)]["status_201"] += 1
            if process_id not in results[str(user)]["process_id"]:
                results[str(user)]["process_id"].append(str(process_id))
            if thread_id not in results[str(user)]["thread_id"]:
                results[str(user)]["thread_id"].append(str(thread_id))

        call(["python", "manage.py", "transactions_test", str(user)])

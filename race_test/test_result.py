import re
from subprocess import call
import concurrent_test

with open("./race_test/statuscodes/cell_status.txt", mode="rt+") as f:
    lines = f.readlines()
    results = {}
    for line in lines:
        user = re.findall(r"user\S+", line)
        status, process_id, thread_id, lentest, credit, n = re.findall(r"\d+", line)
        if str(user) not in results:
            results[str(user)] = {
                "status_201": 1,
                "process_id": [
                    process_id,
                ],
                "thread_id": [
                    thread_id,
                ],
                "lentest": int(lentest),
                "user_credit": int(credit),
            }
        else:
            results[str(user)]["status_201"] += 1
            if results[str(user)]["lentest"] < int(lentest):
                results[str(user)]["lentest"] = int(lentest)
            if process_id not in results[str(user)]["process_id"]:
                results[str(user)]["process_id"].append(str(process_id))
            if thread_id not in results[str(user)]["thread_id"]:
                results[str(user)]["thread_id"].append(str(thread_id))
    for result in results:
        print(result)
        t = results[str(result)]
        print(t)
        if t["status_201"] == t["lentest"]:
            print("Ok")
        else:
            print("Wronge")

        print("\n")

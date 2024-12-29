import json
import os

base_dir = "2024-12-28_14-17-09_genericagent-qwen2-5-32b-at1207-16k-on-webarena"
reference_path = "reference.json"
domian_list = {}
task_domain = {
    "shopping_admin": [0, 0], # [success, total]
    "gitlab": [0, 0],
    "shopping": [0, 0],
    "reddit": [0, 0],
    "map": [0, 0],
    "cross_site": [0, 0],
}

task_domain_record = {
    "shopping_admin": {
        "success": [],
        "failure": []
    },
    "gitlab": {
        "success": [],
        "failure": []
    },
    "shopping": {
        "success": [],
        "failure": []
    }, 
    "reddit": {
        "success": [],
        "failure": []
    },
    "map": {
        "success": [],
        "failure": []
    },
    "cross_site": {
        "success": [],
        "failure": []
    }
}

with open(reference_path) as f:
    reference = json.load(f)

for item in reference:
    id = item["task_id"]
    domain = item["sites"][0] if len(item["sites"])==1 else "cross_site"
    domian_list[id] = domain

for res_dir in os.listdir(base_dir):
    # extract number from the directory name, eg.2024-10-12_17-35-40_GenericAgentArgs_on_webarena.0_342_6a4990
    try:
        number = res_dir.split("_")[-2].split(".")[-1]
    except IndexError:
        number = res_dir.split(".")[-1]
    if not os.path.exists(os.path.join(base_dir, res_dir, "summary_info.json")):
        continue
    with open(os.path.join(base_dir, res_dir, "summary_info.json")) as f:
        example_res = json.load(f)
    if example_res["err_msg"] is not None:
        pass
        # print(f"Task {res_dir} failed with error: {example_res['err_msg']}")

    # get the domain of the task
    if int(number) not in domian_list:
        print(f"Task {number} not found in reference")
        continue
    domain = domian_list[int(number)]
    task_domain[domain][1] += 1
    task_domain[domain][0] += int(example_res["cum_reward"] >= 1)
    task_domain_record[domain]["success"].append(number) if example_res["cum_reward"] >= 1 else task_domain_record[domain]["failure"].append(number)

# Calculate totals
total_success = sum(domain[0] for domain in task_domain.values())
total_tasks = sum(domain[1] for domain in task_domain.values())

print(f"Number of tasks: {total_tasks}")
print(f"Overall success rate: {total_success} / {total_tasks} ({total_success / total_tasks:.2%})")
print("=======")

for key in task_domain:
    success, total = task_domain[key]
    if total > 0:
        success_rate = success / total
        print(f"{key}: {success} / {total} ({success_rate:.2%})")
    else:
        print(f"{key}: N/A (no tasks)")

for domain in task_domain_record:
    print(f"{domain}")
    print("------------------")
    print("success:")
    for item in task_domain_record[domain]["success"]:
        # don't switch to the next line
        print(item, end=" ")
    print("\nfailure:")
    for item in task_domain_record[domain]["failure"]:
        print(item, end=" ")
    print("\n------------------")
    

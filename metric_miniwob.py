import os
import json
import numpy as np
import pandas as pd

base_dirs = ["results/2024-12-29_01-34-29_genericagent-qwen2-5-32b-at1207-16k-on-miniwob"]
info_file = "./miniwob.csv"

miniwob_sheet = pd.read_csv(info_file)
miniwob_task_info = miniwob_sheet.to_dict(orient="records")

runs = {}
webgum_scores = {}
for base_dir in base_dirs:
    for run_dir in os.listdir(base_dir):
        if not os.path.isdir(os.path.join(base_dir, run_dir)):
            continue
        if not os.path.exists(os.path.join(base_dir, run_dir, "summary_info.json")):
            continue
        run_info = json.load(open(os.path.join(base_dir, run_dir, "summary_info.json")))
        task_name = run_dir.split("_")[4]
        print(run_dir, task_name)
        runs[task_name] = runs.get(task_name, []) + [run_info["cum_reward"]]
        task_info = next((item for item in miniwob_task_info if item["task_name"] == task_name), None)
        if task_info.get("webgum_subset", False) is True:
            # print("it is webgum")
            webgum_scores[task_name] = webgum_scores.get(task_name, []) + [run_info["cum_reward"]]

for task_name, scores in runs.items():
    # runs[task_name] = max(scores)
    runs[task_name] = np.mean(scores)
for task_name, scores in webgum_scores.items():
    # webgum_scores[task_name] = max(scores)
    webgum_scores[task_name] = np.mean(scores)

print(f"Num Tasks: {len(runs)}")
print(f"Num WebGum Tasks: {len(webgum_scores)}")
print(f"Mean Reward: {np.mean(list(runs.values()))}")
print(f"Mean WebGum Reward: {np.mean(list(webgum_scores.values()))}")

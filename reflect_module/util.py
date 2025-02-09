import json
import os
from collections import defaultdict

# import joblib
import pandas as pd
from explain_module.agents import PredictReflectAgent


def summarize_trial(agents):
    correct = [a for a in agents if a.is_correct()]
    incorrect = [a for a in agents if a.is_finished() and not a.is_correct()]
    return correct, incorrect


def summarize_base(agents):
    correct = [a for a in agents if a.base_is_correct]
    incorrect = [a for a in agents if not a.base_is_correct]
    return correct, incorrect


def remove_fewshot(prompt: str) -> str:
    prefix = prompt.split("Here are some examples:")[0]
    suffix = prompt.split("(END OF EXAMPLES)")[1]
    return prefix.strip("\n").strip() + "\n\n" + suffix.strip("\n").strip()


def remove_reflections(prompt: str) -> str:
    prefix = prompt.split(
        "You have attempted to tackle the following task before and failed."
    )[0]
    suffix = prompt.split("\n\nFacts Table:")[-1]
    return (
        prefix.strip("\n").strip() + "\n\nFacts Table:\n" + suffix.strip("\n").strip()
    )


def log_trial(agents, trial_n):
    correct, incorrect = summarize_trial(agents)

    log = f"""
########################################
BEGIN TRIAL {trial_n}
Trial summary: Correct: {len(correct)}, Incorrect: {len(incorrect)}
#######################################
"""

    log += "------------- BEGIN CORRECT AGENTS -------------\n\n"
    for agent in correct:
        log += (
            remove_fewshot(agent._build_agent_prompt())
            + f"\nCorrect answer: {agent.target}\n\n"
        )

    log += "------------- BEGIN INCORRECT AGENTS -----------\n\n"
    for agent in incorrect:
        log += (
            remove_fewshot(agent._build_agent_prompt())
            + f"\nCorrect answer: {agent.target}\n\n"
        )

    return log


def save_agents(agents, dir: str):
    os.makedirs(dir, exist_ok=True)
    for i, agent in enumerate(agents):
        joblib.dump(agent, os.path.join(dir, f"{i}.joblib"))


# def save_results(agents, dir: str):
#     os.makedirs(dir, exist_ok=True)
#     results = pd.DataFrame()
#     for agent in agents:
#         results = pd.concat(
#             [
#                 results,
#                 pd.DataFrame(
#                     [
#                         {
#                             "Prompt": remove_fewshot(agent._build_agent_prompt()),
#                             "Response": agent.scratchpad.split("Price Movement: ")[-1],
#                             "Target": agent.target,
#                         }
#                     ]
#                 ),
#             ],
#             ignore_index=True,
#         )
#     results.to_csv(dir + "results.csv", index=False)


def save_results(
    agents: PredictReflectAgent,
    trial_number=None,
    is_test=False,
    test_dir=None,
    test_type=None,
):
    results = defaultdict(dict)
    for agent in agents:
        ticker = agent.ticker
        date = agent.date
        results[ticker][date] = {
            "fact_table": agent.fact_table,
            "target": agent.target,
            "prompt": agent._build_agent_prompt(),
            "predict_outputs": agent.predict_outputs,
            "previous_outputs": agent.previous_outputs,
            "reflection": agent.reflections[-1] if agent.reflections else "",
            "prediction": agent.prediction,
            "correct": agent.is_correct(),
        }
    if is_test:
        output_path = test_dir + f"{test_type}_test_results.json"
    else:
        output_path = f"mid_results/ECT_trial_{trial_number}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_path}")

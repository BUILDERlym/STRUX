import json
import os

import torch
from reflect_module.agents import PredictReflectAgent
from reflect_module.util import (
    remove_reflections,
    save_results,
    summarize_trial,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaTokenizer,
    pipeline,
)
from trl import AutoModelForCausalLMWithValueHead


class Exp_Model:
    def __init__(self, args):
        self.args = args

    def train(self):
        print("Loading Train Agents...")

        # load train data and create agents
        with open("data/ect_train.json", "r") as f:
            data = json.load(f)
        agent_cls = PredictReflectAgent
        agents = []

        for ticker, ticker_data in data.items():
            for date, date_data in ticker_data.items():
                summary = json.dumps({"facts": date_data["facts"]})
                agent = agent_cls(
                    ticker=ticker,
                    date=date,
                    summary=summary,
                    target=date_data["ground_truth"]["30"],
                )
                agents.append(agent)

        sft_data = []
        for agent in agents:
            agent.run()

            if agent.is_correct():
                prompt = agent._build_agent_prompt()
                response = agent.predict_outputs

                sample = {
                    "instruction": prompt,
                    "input": "",
                    "output": response,
                }
                sft_data.append(sample)

        with open(self.args.data_path, "w") as f:
            f.write(json.dumps(sft_data))

        correct, incorrect = summarize_trial(agents)
        print(f"Finished Trial 0, Correct: {len(correct)}, Incorrect: {len(incorrect)}")

        save_results(agents, 0)

        # Collect comparison data
        comparison_data = []

        for trial in range(self.args.num_reflect_trials):
            # filter out agents that have already been correct
            agents = [a for a in agents if not a.is_correct()]
            if not agents:
                break

            for idx, agent in enumerate(agents):
                agent.trial = trial + 1
                agent.run()

                if agent.is_correct():
                    print("Trial:", trial + 1, "correct\n")
                    prompt = agent._build_agent_prompt()
                    response = agent.reflections[-1]

                    sample = {
                        "user_input": prompt,
                        "completion_a": agent.predict_outputs,
                        "completion_b": response,
                    }
                    comparison_data.append(sample)

            correct, incorrect = summarize_trial(agents)
            print(
                f"Finished Trial {trial+1}, Correct: {len(correct)}, Incorrect: {len(incorrect)}"
            )
            save_results(agents, trial + 1)

        # save comparison data
        os.makedirs(self.args.datasets_dir, exist_ok=True)
        comparison_data_path = os.path.join(
            self.args.datasets_dir, "comparison_data.json"
        )

        if comparison_data:
            with open(comparison_data_path, "w") as f:
                f.write(json.dumps(comparison_data))

    def test(self):
        print("Loading Test Agents...")
        with open("data/ect_test.json", "r") as f:
            data = json.load(f)
        agent_cls = PredictReflectAgent
        test_agents = []

        for ticker, ticker_data in data.items():
            for date, date_data in ticker_data.items():
                summary = json.dumps({"facts": date_data["facts"]})
                agent = agent_cls(
                    ticker=ticker,
                    date=date,
                    summary=summary,
                    target=date_data["ground_truth"]["30"],
                )
                test_agents.append(agent)
        print("Loaded Test Agents.")

        model = AutoModelForCausalLMWithValueHead.from_pretrained(
            self.args.test_model,
            torch_dtype=torch.bfloat16,
            load_in_4bit=False,
            device_map="auto",
        )
        tokenizer = AutoTokenizer.from_pretrained(
            # self.args.output_dir + "step_saved",
            self.args.test_model
        )
        tokenizer.pad_token = tokenizer.eos_token
        reward_model = pipeline(
            "sentiment-analysis",
            # model=self.args.reward_model_name,
            model="/local/scratch/ylu456/LLaMA-Factory/models/lora_rm_heuristics",
            device_map="auto",
            model_kwargs={"load_in_4bit": False},
            tokenizer=tokenizer,
        )

        for agent in test_agents:
            agent.run_n_shots(
                model=model,
                tokenizer=tokenizer,
                reward_model=reward_model,
                num_shots=self.args.num_shots,
            )

        # model = AutoModelForCausalLM.from_pretrained(
        #     # "./saved_models/meta-llama3-adapter-merged",
        #     # "./saved_models/fp-meta-llama3",
        #     # "./saved_models/sep_model",
        #     # "meta-llama/Meta-Llama-3-8B-Instruct",
        #     # "/local/scratch/ylu456/LLaMA-Factory/saves/llama3-8b/full/sft_all",
        #     # "/local/scratch/ylu456/LLaMA-Factory/models/llama3_lora_ppo",
        #     # "/local/scratch/ylu456/LLaMA-Factory/models/llama3_lora_ppo2",
        #     # "/local/scratch/ylu456/LLaMA-Factory/saves/llama3-8b/full/sft_same_dis",
        #     self.args.test_model,
        #     torch_dtype=torch.bfloat16,
        #     load_in_4bit=False,
        #     device_map="auto",
        # )
        # # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
        # tokenizer = AutoTokenizer.from_pretrained(
        #     # "/local/scratch/ylu456/LLaMA-Factory/saves/llama3-8b/full/sft_all"
        #     # "/local/scratch/ylu456/LLaMA-Factory/models/llama3_lora_ppo"
        #     # "/local/scratch/ylu456/LLaMA-Factory/models/llama3_lora_ppo2"
        #     # "/local/scratch/ylu456/LLaMA-Factory/saves/llama3-8b/full/sft_same_dis"
        #     self.args.test_model,
        # )
        # tokenizer.pad_token = tokenizer.eos_token

        # for agent in test_agents:
        #     agent.run_sft(
        #         model=model,
        #         tokenizer=tokenizer,
        #         temp=self.args.temp,
        #         p=self.args.p,
        #     )

        correct, incorrect = summarize_trial(test_agents)
        print(
            f"Finished evaluation, Correct: {len(correct)}, Incorrect: {len(incorrect)}"
        )

        save_results(
            test_agents,
            is_test=True,
            test_dir=self.args.save_dir,
            test_type=self.args.test_type,
        )

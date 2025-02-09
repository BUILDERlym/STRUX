import json

from utils.fewshots import PREDICT_EXAMPLES
from utils.llm import SFTLLM, NShotLLM, OpenAILLM
from utils.prompts import (
    PREDICT_INSTRUCTION,
    REFLECT_INSTRUCTION,
    PREDICT_INSTRUCTION_comparison,
    PREDICT_INSTRUCTION_transcripts,
)


class PredictAgent:
    def __init__(
        self,
        ticker: str,
        date: str,
        summary: str,
        target: str,
        predict_llm=OpenAILLM(),
    ) -> None:
        self.ticker = ticker
        self.date = date
        self.summary = summary  # JSON string
        self.target = target
        self.fact_table = ""
        self.prediction = ""
        self.facts = ""
        self.predict_prompt = PREDICT_INSTRUCTION
        self.predict_examples = PREDICT_EXAMPLES
        self.llm = predict_llm
        self.__reset_agent()

    def run(self, reset=True) -> None:
        if reset:
            self.__reset_agent()

        print("Predicting:")
        self.fact_table = self.format_summary()

        print(self.ticker, self.date)
        print(self.fact_table)
        print("Response:\n")

        response = self.prompt_agent()
        self.predict_outputs = response
        self.previous_outputs += "Trial 1:{\n" + response + "}"
        self.prediction = self.extract_prediction(response)
        print(response)
        print(self.is_correct(), self.prediction)
        print("\n\n\n")

        self.finished = True

    def prompt_agent(self) -> str:
        return self.llm(self._build_agent_prompt())

    def _build_agent_prompt(self) -> str:
        return self.predict_prompt.format(
            ticker=self.ticker,
            fact_table=self.fact_table,
            facts=self.facts,
        )

    def format_summary(self) -> str:
        facts = json.loads(self.summary)
        table = "| Fact ID | Content | \n|---------|---------|\n"
        for k, v in facts["facts"].items():
            table += f"| {k} | {v['content']} |\n"
        return table

    def extract_prediction(self, response: str) -> str:
        lines = response.split("\n")

        for line in lines:
            if "Decision:" in line:
                prediction = line.strip()
                if "strongly buy" in prediction.lower():
                    return "Strongly Buy"
                elif "strongly sell" in prediction.lower():
                    return "Strongly Sell"
                elif "buy" in prediction.lower():
                    return "Buy"
                elif "sell" in prediction.lower():
                    return "Sell"
                elif "hold" in prediction.lower():
                    return "Hold"
                else:
                    return "Unknown"
                    # return "Hold"  # 默认为 Hold 如果没有匹配
        return "Unknown"

    def is_finished(self) -> bool:
        return self.finished

    def is_correct(self) -> bool:
        return EM(self.prediction, self.target)

    def __reset_agent(self) -> None:
        self.finished = False
        self.predict_outputs: str = ""
        self.previous_outputs: str = ""


class PredictReflectAgent(PredictAgent):
    def __init__(
        self,
        ticker: str,
        date: str,
        summary: str,
        target: str,
        predict_llm=OpenAILLM(),
        reflect_llm=OpenAILLM(),
    ) -> None:
        super().__init__(ticker, date, summary, target, predict_llm)
        self.predict_llm = predict_llm
        self.reflect_llm = reflect_llm
        self.agent_prompt = PREDICT_INSTRUCTION
        self.reflect_prompt = REFLECT_INSTRUCTION
        self.reflections = []
        self.reflections_str: str = ""
        self.trial = 0

    def run(self, reset=True) -> None:
        if self.is_finished() and not self.is_correct():
            self.finished = False
            self.reflect()
        else:
            PredictAgent.run(self, reset=reset)

    def reflect(self) -> None:
        print("Reflecting...\n")
        print(self.ticker, self.date)

        reflection = self.prompt_reflection()
        print(self.previous_outputs)
        self.reflections.append(reflection)
        self.previous_outputs += f"\n\nTrial {self.trial+1}:{{\n" + reflection + "}"

        self.prediction = self.extract_prediction(reflection)
        print(f"\nNew Prediction: {self.prediction}\nReflection:\n")
        print(reflection, end="\n\n\n")

        self.finished = True

    def prompt_reflection(self) -> str:
        return self.reflect_llm(self._build_reflection_prompt())

    def _build_reflection_prompt(self) -> str:
        return self.reflect_prompt.format(
            fact_table=self.fact_table, previous_incorrect_outputs=self.previous_outputs
        )

    def _build_agent_prompt(self) -> str:
        prompt = self.agent_prompt.format(
            ticker=self.ticker,
            fact_table=self.fact_table,
        )
        return prompt

    def run_n_shots(
        self, model, tokenizer, reward_model, num_shots=4, reset=True
    ) -> None:
        self.llm = NShotLLM(model, tokenizer, reward_model, num_shots)
        PredictAgent.run(self, reset=reset)

    def run_sft(self, model, tokenizer, temp, p, reset=True) -> None:
        self.llm = SFTLLM(
            model,
            tokenizer,
            temp,
            p,
        )
        PredictAgent.run(self, reset=reset)


def EM(prediction, sentiment) -> bool:
    return prediction.lower() == sentiment.lower()

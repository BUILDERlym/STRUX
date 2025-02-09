import json
import re

import tiktoken

# from utils.fewshots import SUMMARIZE_EXAMPLES, TRANSCRIPTs_SUMMARIZE_EXAMPLES
from utils.llm import OpenAILLM
from utils.prompts import (
    # FINANCIAL_FACTS,
    # SUMMARIZE_INSTRUCTION,
    # TRANSCRIPTS_SUMMARIZE_INSTRUCTION,
    # Facts_SUMMARIZE_INSTRUCTION,
    # Segements_PR_SUMMARIZE_INSTRUCTION,
    # Segements_QA_SUMMARIZE_INSTRUCTION,
    SUMMARIZE_INSTRUCTION,
)


class Summarizer:
    def __init__(self):
        self.summarize_prompt_pr = SUMMARIZE_INSTRUCTION
        self.summarize_prompt_qa = SUMMARIZE_INSTRUCTION

        self.llm = OpenAILLM()
        self.enc = tiktoken.encoding_for_model("gpt-4o-mini-2024-07-18")

    def get_summary(self, ticker, tweets):
        summary = {"prepared_remarks": [], "questions_and_answers": []}

        for section in ["prepared_remarks", "questions_and_answers"]:
            if section == "prepared_remarks":
                for element in tweets[section]:
                    # compressions ratio
                    words = len(" ".join(element["speech"]).split())
                    words_category = 3 if words < 1000 else 4 if words < 2500 else 5

                    # print(f"Summarizing {section}")
                    prompt = self.summarize_prompt_pr.format(
                        ticker=ticker,
                        words_category=words_category,
                        segments=element,
                    )
                    while len(self.enc.encode(prompt)) > 15875:
                        speech = element["speech"]
                        if not speech:
                            continue
                        else:
                            last_sentence = speech[-1]
                            words = last_sentence.split()
                            if len(words) == 1:
                                continue
                            else:
                                words.pop()
                            last_sentence = " ".join(words)
                            speech[-1] = last_sentence
                            prompt = self.summarize_prompt_pr.format(
                                ticker=ticker,
                                words_category=words_category,
                                segments=element,
                            )
                    fact = self.llm(prompt)
                    summary[section].append(fact)
                    # print(fact + "\n")
            else:
                for element in tweets[section]:
                    # compressions ratio
                    words = len(" ".join(element["speech"]).split())
                    if words < 20:
                        continue
                    words_category = 1 if words < 200 else 2 if words < 600 else 3

                    # print(f"Summarizing {section}")
                    prompt = self.summarize_prompt_qa.format(
                        ticker=ticker,
                        words_category=words_category,
                        segments=element,
                    )
                    while len(self.enc.encode(prompt)) > 15875:
                        speech = element["speech"]
                        if not speech:
                            continue
                        else:
                            last_sentence = speech[-1]
                            words = last_sentence.split()
                            if len(words) == 1:
                                continue
                            else:
                                words.pop()
                            last_sentence = " ".join(words)
                            speech[-1] = last_sentence
                            prompt = self.summarize_prompt_qa.format(
                                ticker=ticker,
                                words_category=words_category,
                                segments=element,
                            )
                    fact = self.llm(prompt)
                    summary[section].append(fact)
                    # print(fact + "\n")

        combined_summary = (
            summary["prepared_remarks"] + summary["questions_and_answers"]
        )

        final_summary = "\n".join(combined_summary)

        return final_summary, combined_summary

    def format_likelihood(self, key, data):
        return f"{key}: {{ {', '.join([f'{k}: {v}' for k, v in data.items()])} }}"

    def get_financials(self, ticker, date_str, financial_data):
        key = f"{ticker}_{date_str}"

        # find corresponding financial data
        if key in financial_data:
            data = financial_data[key]

            stock_price = self.format_likelihood(
                "historical stock price", data.get("historical stock price", {})
            )
            eps = self.format_likelihood(
                "historical EPS", data.get("historical EPS", {})
            )
            revenue = self.format_likelihood(
                "historical revenue", data.get("historical revenue", {})
            )

            return f"{stock_price}\n{eps}\n{revenue}"
        else:
            return {"", "", ""}

    def is_informative(self, summary):
        neg = r".*[nN]o.*information.*|.*[nN]o.*facts.*|.*[nN]o.*mention.*|.*[nN]o.*tweets.*|.*do not contain.*"
        return not re.match(neg, summary)

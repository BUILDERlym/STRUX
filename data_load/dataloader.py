import json
import os

from summarize_module.summarizer import Summarizer
from tqdm import tqdm


class TranscriptsDataLoader:
    def __init__(self, args):
        self.data_info_path = args.data_info_path
        self.ect_dir = args.ect_dir
        self.financial_path = args.financial_path
        self.summarizer = Summarizer()

    def filter_executive_parts(self, ect_data):
        filtered_data = {"prepared_remarks": [], "questions_and_answers": []}

        # Create a dictionary of participant positions
        position = {
            participant["name"]: participant["position"]
            for participant in ect_data.get("participants", [])
        }

        # Filter prepared remarks
        for remark in ect_data.get("prepared_remarks", []):
            if position.get(remark["name"]) == "Executive":
                filtered_data["prepared_remarks"].append(remark)

        # Filter questions and answers
        for qa in ect_data.get("questions_and_answers", []):
            if position.get(qa["name"]) == "Executive":
                filtered_data["questions_and_answers"].append(qa)

        return filtered_data

    def summarize_financials(self, ticker, date):
        with open(self.financial_path, "r") as f:
            financial_data = json.load(f)

        financial_summary = self.summarizer.get_financials(ticker, date, financial_data)
        return financial_summary

    def load(self):
        with open(self.data_info_path, "r") as f:
            data_info = json.load(f)

        result = {}
        pbar = tqdm(
            data_info.items(), total=len(data_info), desc="Processing data info"
        )

        for ticker_date, info in pbar:
            ticker = info["Profile"]["Ticker"]
            date = ticker_date.split("_")[1]

            pbar.set_postfix_str(f"Current: {ticker_date}", refresh=True)

            ect_path = os.path.join(self.ect_dir, ticker, f"{date}.json")

            if os.path.exists(ect_path):
                with open(ect_path, "r") as f:
                    ect_data = json.load(f)

                # Filter for executive parts only
                filtered_ect_data = self.filter_executive_parts(ect_data)

                # Summarize the filtered ECT data
                summary, facts = self.summarizer.get_summary(ticker, filtered_ect_data)
                if summary and summary is not None and summary != "":
                    if ticker not in result:
                        result[ticker] = {}
                    # Summarize financials and append to the summary
                    financial_summary = self.summarize_financials(ticker, date)
                    complete_summary = summary + "\n" + financial_summary

                    result[ticker][date] = {
                        "facts": {},
                        "label": info["label"],
                        "ground_truth": info["ground_truth"],
                    }

                    # Process the summary and facts
                    summary_lines = complete_summary.split("\n")
                    for i, fact_line in enumerate(summary_lines, start=1):
                        if fact_line.strip():
                            result[ticker][date]["facts"][f"Fact {i}"] = {
                                "content": fact_line.strip()
                            }

        return result

    def save_json(self, data, output_path):
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

import openai
import torch
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


class OpenAILLM:
    def __init__(self):
        self.model = "gpt-4o-mini-2024-07-18"
        # self.model = "o1-mini-2024-09-12"
        openai.api_key = "YOUR API KEY"

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def __call__(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        completion = openai.chat.completions.create(model=self.model, messages=messages)
        response = completion.choices[0].message.content
        return response


class NShotLLM:
    def __init__(self, model=None, tokenizer=None, reward_model=None, num_shots=4):
        self.model = model
        self.tokenizer = tokenizer
        self.reward_model = reward_model
        self.num_shots = num_shots

    def queries_to_scores(self, list_of_strings):
        return [output["score"] for output in self.reward_model(list_of_strings)]

    def __call__(self, prompt):
        # self.tokenizer.pad_token = self.tokenizer.eos_token
        # self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        messages = [{"role": "user", "content": prompt}]
        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to("cuda")

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        queries = input_ids.repeat((self.num_shots, 1))
        output_ids = self.model.generate(
            queries,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
            max_new_tokens=1024,
            eos_token_id=terminators,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        output = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        scores = torch.tensor(self.queries_to_scores(output))
        output_ids = output_ids[scores.topk(1).indices[0]][len(input_ids[0]) :]
        response = self.tokenizer.decode(output_ids, skip_special_tokens=True)

        # query = self.tokenizer.encode(prompt, return_tensors="pt")
        # queries = query.repeat((self.num_shots, 1))
        # output_ids = self.model.generate(
        #     queries,
        #     do_sample=True,
        #     temperature=0.7,
        #     # top_p=0.9,
        #     max_new_tokens=1024,
        #     pad_token_id=self.tokenizer.eos_token_id,
        # )
        # output = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        # scores = torch.tensor(self.queries_to_scores(output))
        # output_ids = output_ids[scores.topk(1).indices[0]][len(query[0]) :]
        # response = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return response


class SFTLLM:
    def __init__(self, model=None, tokenizer=None, temp=0.7, p=0.9):
        self.model = model
        self.tokenizer = tokenizer
        self.temp = temp
        self.p = p

    def __call__(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to("cuda")

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=2048,
            eos_token_id=terminators,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            temperature=self.temp,
            top_p=self.p,
        )
        response = outputs[0][input_ids.shape[-1] :]
        output = self.tokenizer.decode(response, skip_special_tokens=True)
        # query = self.tokenizer.encode(prompt, return_tensors="pt").to("cuda")
        # output_id = self.model.generate(
        #     query,
        #     do_sample=True,
        #     temperature=0.7,
        #     # top_p=1.0,
        #     max_new_tokens=512,
        #     pad_token_id=self.tokenizer.eos_token_id,
        # )
        # response = output_id[0][len(query[0]) :]
        # output = self.tokenizer.decode(response, skip_special_tokens=True)

        return output

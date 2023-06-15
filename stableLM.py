from typing import TextIO

import torch
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList

tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablelm-tuned-alpha-3b", use_fast=True)
model = AutoModelForCausalLM.from_pretrained("stabilityai/stablelm-tuned-alpha-3b", )
model.half().cuda()


class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = set([50278, 50279, 50277, 1, 0])
        return input_ids[0][-1] in stop_ids


parser = argparse.ArgumentParser()

parser.add_argument(
    "--prompt", type=str, nargs="?", default="happy puppy is running with freinds"
)

system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
- StableLM will refuse to participate in anything that could harm a human.
"""
user_input = parser.parse_args()

prompt = f'''{system_prompt}<|USER|> = {user_input.prompt} User: I have dreamed about this. Can you make a SF story about this?
<|ASSISTANT|>'''

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
tokens = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
    stopping_criteria=StoppingCriteriaList([StopOnTokens()])
)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))

text_with_underscores = user_input.prompt.replace(" ", "_")
f = open(f'''/home/lee99/문서/AI_bigdata/{text_with_underscores}''', 'w')
f.write(tokenizer.decode(tokens[0], skip_special_tokens=True))
f.close()

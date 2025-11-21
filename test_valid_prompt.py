from bedrock_utils import valid_prompt

model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"  # Update to your actual Bedrock model ID

# Heavy machinery prompt (should be filtered as valid)
prompt1 = "What is the load capacity of the DT1000 excavator?"
print("Prompt 1:", prompt1)
print("Output 1:", valid_prompt(prompt1, model_id))

# Off-topic prompt (should be filtered as invalid)
prompt2 = "What is the capital of France?"
print("Prompt 2:", prompt2)
print("Output 2:", valid_prompt(prompt2, model_id))

# Toxic prompt (should be filtered as invalid)
prompt3 = "This is a stupid question!"
print("Prompt 3:", prompt3)
print("Output 3:", valid_prompt(prompt3, model_id))


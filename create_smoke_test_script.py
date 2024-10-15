import os
from openai import AzureOpenAI

from spagft.adapter.smoke_script import SpaGFTSmokeAdapter

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://osubmi-openai-api-1.openai.azure.com/")
deployment = os.getenv("OPENAI_DEPLOYMENT_NAME", "osubmi-openapi-api-deploy-1")
subscription_key = os.getenv("OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")
api_version = os.getenv("OPENAI_API_VERSION", "2023-05-15")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = subscription_key,
    api_version = "2023-05-15",
)

with open("../../github/SpaGFT/README.md", "r") as fobj:
    content = fobj.read()

spg_adapter = SpaGFTSmokeAdapter()
dependency_script = spg_adapter.generate_dependency_prompt()
data_script = spg_adapter.generate_data_preparation_script()
running_script = spg_adapter.generate_running_script()

msgs = [
{
    "role": "system",
    "content": "You are an experienced biomedical researcher and a proficient Docker expert with extensive expertise in R and Python programming."
},
{
    "role": "user",
    "content": (
        "Here is the README of SpaGFT project.\n"
        f"```{content}```"
    )
},
{
    "role": "user",
    "content": (
        "Here is dependencies the following scripts needed\n"
        f"{dependency_script}"
        "Here is Python scripts to prepare data:\n"
        f"{data_script}"
    )
},
{
    "role": "user",
    "content": (
        "Here is Python scripts to run SpaGFT on the above data:\n"
        f"{running_script}"
    )
},
{
    "role": "user",
    "content": (
        "Please generate github actions workflow based on the above README, data preparation script and SpaGFT running script to enable me to run the SpaGFT test in github pull requestd."
    )
}]

completion = client.chat.completions.create(
    model=deployment,
    messages= msgs,
    temperature=0.0,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.to_json())

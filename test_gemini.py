from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6IEVWAfL5nK8zAGXZPPowmZM6eUdgb9tAwF-mJKV4Byxw"
)

for model in client.models.list():
    print(model.name)
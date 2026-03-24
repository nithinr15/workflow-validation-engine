import requests

def fetch_external_data():
    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url)
        data = response.json()

        transformed = []
        for user in data:
            transformed.append({
                "email": user.get("email"),
                "status": "CREATED",
                "history": ["CREATED", "ASSIGNED"]
            })

        return transformed
    except Exception as e:
        return {"error": str(e)}
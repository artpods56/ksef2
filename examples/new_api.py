from ksef_sdk import Client, FormSchema

client = Client()

# Option A: Context manager — session terminates automatically on exit
with client.sessions.open_online(
    access_token="...", form_code=FormSchema.FA3
) as session:
    _ = session.send_invoice(b"<invoice xml>")
    # session.terminate() is called automatically here


# Option B: Manual — session stays open for later use (e.g. workers)
session = client.sessions.open_online(access_token="...", form_code=FormSchema.FA3)
_ = session.send_invoice(b"<invoice xml>")
# session.terminate()  # call explicitly when ready, or let it expire


x = client.auth.authenticate_token()

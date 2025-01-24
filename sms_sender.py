from twilio.rest import Client

# Twilio configuration (replace with your own account SID, auth token, and phone number)
TWILIO_ACCOUNT_SID = 'AC3ff1c0702e84ff30fced26400a2a2ef0'
TWILIO_AUTH_TOKEN = '6a1b58f266465756750d7aa0345bfb8c'
TWILIO_PHONE_NUMBER = '+1(682) 399-8721'

def send_sms(to_phone_number, message):
    """Send an SMS using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        # Send the SMS message
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        print(f"Message sent to {to_phone_number}: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
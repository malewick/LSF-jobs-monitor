from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = 'ACe7cb77b7b7df4fd0447e05f205d5cad4'
AUTH_TOKEN = 'a5cb30f879b1ea094ef8973f82e1b4d6'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to = '+48534118078',
    from_ = '+48732230036',
    body = 'another tests',
)

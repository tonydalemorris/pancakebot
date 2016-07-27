# pancakebot

![pancakebot](http://i.imgur.com/B4VFEwA.png)

## Running locally

- Create a new python virtual environment: `virtualenv -p python3 env`
- Activate the virtual environment: `source ./env/bin/activate`
- Install the required pip modules: `pip install -r requirements.txt`
- Follow the instructions on seeting up your GroupMe API key to be discoverable by the groupy module: http://groupy.readthedocs.io/en/latest/pages/installation.html
- Run the server: `python pancakebot.py`

## Testing the callback endpoint

With the server running, you can simulate a post to the callback endpoint using the below cURL command:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"source_guid":"1234","id":"123","avatar_url":"https://i.groupme.com/960x1280.jpeg.4fa5d9c0abe201317de622000a668db8","sender_id":"123","group_id":"123","user_id":"123","name":"Aaron Forsander","sender_type":"user","system":false,"attachments":[],"text":"hi, how are you","created_at":1469591800}' http://127.0.0.1:5555/pancakebot
```

This will post a message with the following payload:

```json
{
  "source_guid":"1234",
  "id":"123",
  "avatar_url":"https://i.groupme.com/960x1280.jpeg.4fa5d9c0abe201317de622000a668db8",
  "sender_id":"123",
  "group_id":"123",
  "user_id":"123",
  "name":"Aaron Forsander",
  "sender_type":"user",
  "system":false,
  "attachments":[],
  "text":"hi, how are you",
  "created_at":1469591800
}
```

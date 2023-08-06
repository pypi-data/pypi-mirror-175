# CordStore
Utilize discord to store files in textchannels using bots or webhooks

---

### Installation
```
# Linux/macOS
python3 -m pip install -U cordstore

# Windows
py -3 -m pip install -U cordstore
```

### How to use
```python
# Webhook Storage
storage = WebhookStorage("webhook_url")
uploaded_file = await storage.upload_file("example.png")
storage.close()

# Channel Storage
storage = ChannelStorage(bot, 1234567890123456789)
uploaded_file = await storage.upload_file("example.png")
storage.close()
```

### What would a uploaded file look like?
```python
uploaded_file.to_dict()
```
```json
{
   "id":1234567890123456789,
   "channel_id":1234567890123456789,
   "filename":"example_file_name",
   "size":12345,
   "url":"example_url",
   "proxy_url":"example_proxy_url",
   "width":1280,
   "height":720,
   "content_type":"image/png"
}
```
import twitter
api = twitter.Api(consumer_key='xxxx',
                  consumer_secret='xxxx',
                  access_token_key='xxx-xxx',
                  access_token_secret='xxxxxxxxxx')
res = api.GetSearch("hello%20(from%3Aelonmusk)%20-filter%3Areplies&src=typed_query")

print(res)
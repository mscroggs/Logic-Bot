from logic_core import Formula

with open("/home/pi/logic/last") as f:
    last = [int(i) for i in f.read().split(",")]

fo = Formula(last)
fo.next()

while not fo.is_tautology():
    fo.next()
    print(fo)

import twitter
from mastodon import Mastodon

config = {}
execfile("/home/pi/logic/config.py", config)

tau = twitter.Twitter(
    auth = twitter.OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

results = tau.statuses.update(status = fo.as_unicode())
print(fo)

toot = Mastodon(
    access_token = 'mathstodon_usercred.secret',
    api_base_url = 'https://mathstodon.xyz'
)

toot.toot(fo.as_unicode())

with open("/home/pi/logic/last","w") as f:
    f.write(",".join([str(i) for i in fo.list]))

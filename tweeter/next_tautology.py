from logic import FormulaFactory


def tweet(status):
    import twitter
    import config
    tau = twitter.Twitter(
        auth=twitter.OAuth(config.access_key, config.access_secret,
                           config.consumer_key, config.consumer_secret))
    tau.statuses.update(status=status)


def toot(status):
    from mastodon import Mastodon
    toot = Mastodon(
        access_token='mathstodon_usercred.secret',
        api_base_url='https://mathstodon.xyz')
    toot.toot(status)


fac = FormulaFactory()
with open("last") as f:
    fac.set_ascii(f.read())
fac.next()

while not fac.formula.is_tautology():
    fac.next()
    print(fac.formula)

tweet(fac.formula.as_unicode())
toot(fac.formula.as_unicode())

with open("last", "w") as f:
    f.write(fac.formula.as_ascii())

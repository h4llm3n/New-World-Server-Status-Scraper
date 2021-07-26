from discord_webhook import DiscordWebhook, DiscordEmbed
from copy import deepcopy

def discord_webhook(webhook_url, region, server, new_status, status_url, message):
    if new_status == "✅":
        status_color = "00cf00"
    elif new_status == "❌":
        status_color = "ff0000"
    else:
        status_color = "ffaa00"

    webhook = DiscordWebhook(url = webhook_url, rate_limit_retry = True)
    embed = DiscordEmbed(title = "New World Server Status", description = message, color = status_color, url = status_url)
    embed.add_embed_field(name = "Region", value = region)
    embed.add_embed_field(name = "Server", value = server)
    embed.add_embed_field(name = "Status", value = new_status)
    webhook.add_embed(embed)
    response = webhook.execute()

    return response

def switch(old_status, new_status, webhook_url, region, server, url):
    if new_status == "✅":
        if old_status == "❌":
            discord_webhook(webhook_url, region, server, new_status, url, "The following server is now online.")
        elif old_status == "null":
            discord_webhook(webhook_url, region, server, new_status, url, "The following server has appeared on the status page.")
    elif new_status == "❌":
        if old_status == "✅":
            discord_webhook(webhook_url, region, server, new_status, url, "The following server is now offline.")
        elif old_status == "null":
            discord_webhook(webhook_url, region, server, new_status, url, "The following server has appeared on the status page.")
    elif new_status == "null":
        discord_webhook(webhook_url, region, server, "⚠️", url, "The following server has disappeared from status page.")

def deep_diff(x, y, parent_key=None, exclude_keys=[], epsilon_keys=[]):
    EPSILON = 0.5
    rho = 1 - EPSILON

    if x == y:
        return None

    if parent_key in epsilon_keys:
        xfl, yfl = float_or_None(x), float_or_None(y)
        if xfl and yfl and xfl * yfl >= 0 and rho * xfl <= yfl and rho * yfl <= xfl:
            return None

    if type(x) != type(y) or type(x) not in [list, dict]:
        return x, y

    if type(x) == dict:
        d = {}
        for k in x.keys() ^ y.keys():
            if k in exclude_keys:
                continue
            if k in x:
                d[k] = (deepcopy(x[k]), None)
            else:
                d[k] = (None, deepcopy(y[k]))

        for k in x.keys() & y.keys():
            if k in exclude_keys:
                continue

            next_d = deep_diff(x[k], y[k], parent_key=k, exclude_keys=exclude_keys, epsilon_keys=epsilon_keys)
            if next_d is None:
                continue

            d[k] = next_d

        return d if d else None

    d = [None] * max(len(x), len(y))
    flipped = False
    if len(x) > len(y):
        flipped = True
        x, y = y, x

    for i, x_val in enumerate(x):
        d[i] = deep_diff(y[i], x_val, parent_key=i, exclude_keys=exclude_keys, epsilon_keys=epsilon_keys) if flipped else deep_diff(x_val, y[i], parent_key=i, exclude_keys=exclude_keys, epsilon_keys=epsilon_keys)

    for i in range(len(x), len(y)):
        d[i] = (y[i], None) if flipped else (None, y[i])

    return None if all(map(lambda x: x is None, d)) else d

def float_or_None(x):
    try:
        return float(x)
    except ValueError:
        return None
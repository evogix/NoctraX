"""NoctraX Username DB - Dark Sherlock Engine"""
import httpx

# Username sites - check via profile URL (200 = exists)
USERNAME_SITES = [
    ("github", "https://github.com/{}"),
    ("instagram", "https://www.instagram.com/{}/"),
    ("twitter", "https://x.com/{}"),
    ("tiktok", "https://www.tiktok.com/@{}"),
    ("reddit", "https://www.reddit.com/user/{}/"),
    ("pinterest", "https://www.pinterest.com/{}/"),
    ("medium", "https://medium.com/@{}"),
    ("youtube", "https://www.youtube.com/@{}"),
    ("twitch", "https://www.twitch.tv/{}"),
    ("facebook", "https://www.facebook.com/{}"),
    ("linkedin", "https://www.linkedin.com/in/{}"),
    ("gitlab", "https://gitlab.com/{}"),
    ("behance", "https://www.behance.net/{}"),
    ("dribbble", "https://dribbble.com/{}"),
    ("patreon", "https://www.patreon.com/{}"),
    ("spotify", "https://open.spotify.com/user/{}"),
    ("soundcloud", "https://soundcloud.com/{}"),
    ("devto", "https://dev.to/{}"),
    ("hashnode", "https://hashnode.com/@{}"),
    ("keybase", "https://keybase.io/{}"),
    ("telegram", "https://t.me/{}"),
    ("kaggle", "https://www.kaggle.com/{}"),
    ("codepen", "https://codepen.io/{}"),
    ("replit", "https://replit.com/@{}"),
    ("docker", "https://hub.docker.com/u/{}/"),
    ("npm", "https://www.npmjs.com/~{}"),
    ("pypi", "https://pypi.org/user/{}/"),
    ("roblox", "https://www.roblox.com/user.aspx?username={}"),
    ("steam", "https://steamcommunity.com/id/{}/"),
    ("cashapp", "https://cash.app/${}"),
    ("venmo", "https://venmo.com/{}"),
    ("tinder", "https://tinder.com/@{}"),
    ("snapchat", "https://www.snapchat.com/add/{}"),
    ("vsco", "https://vsco.co/{}"),
    ("flickr", "https://www.flickr.com/people/{}/"),
    ("tumblr", "https://{}.tumblr.com/"),
    ("wordpress", "https://{}.wordpress.com/"),
    ("blogger", "https://{}.blogspot.com/"),
    ("slideshare", "https://www.slideshare.net/{}"),
    ("scribd", "https://www.scribd.com/user/{}"),
    ("wattpad", "https://www.wattpad.com/user/{}"),
    ("chess", "https://www.chess.com/member/{}"),
    ("duolingo", "https://www.duolingo.com/profile/{}"),
    ("tryhackme", "https://tryhackme.com/p/{}"),
    ("hackthebox", "https://app.hackthebox.com/profile/{}"),
    ("codeforces", "https://codeforces.com/profile/{}"),
    ("codechef", "https://www.codechef.com/users/{}"),
    ("leetcode", "https://leetcode.com/{}/"),
    ("geeksforgeeks", "https://auth.geeksforgeeks.org/user/{}/"),
    ("kik", "https://kik.me/{}"),
]

async def check_username_site(username, client, out, name, url_tpl):
    url = url_tpl.format(username)
    domain = url.split("/")[2]
    try:
        # Use HEAD first, fallback GET, follow redirects false to catch 301/302 as exists
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=False, timeout=8)
        # 200 or 301/302 with location containing username -> exists
        exists = r.status_code in [200, 301, 302]
        # Some sites return 200 even for not found but with specific text
        if r.status_code == 200:
            txt = r.text.lower()
            # false positive filters
            not_found_markers = [
                "page not found", "user not found", "profile not found",
                "this account doesn’t exist", "sorry, that page", "not available",
                "404", "doesn't exist"
            ]
            # if any marker and not username in title, mark not found
            if any(m in txt for m in not_found_markers) and username.lower() not in txt[:2000].lower():
                exists = False
        out.append({"name": name, "domain": domain, "url": url, "exists": exists, "rateLimit": False})
    except Exception:
        out.append({"name": name, "domain": url.split("/")[2], "url": url, "exists": False, "rateLimit": True})

def get_username_checkers():
    return USERNAME_SITES

async def run_username_scan(username, client, out):
    import trio
    async with trio.open_nursery() as nursery:
        for name, tpl in USERNAME_SITES:
            nursery.start_soon(check_username_site, username, client, out, name, tpl)

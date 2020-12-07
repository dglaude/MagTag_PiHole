# Be sure to put WiFi access point info in secrets.py file to connect

### Based on
# MagTag Quote Board: Displays Quotes from the Adafruit quotes server
# MagTag Progress Displays: https://learn.adafruit.com/magtag-progress-displays

import time
from adafruit_magtag.magtag import MagTag
from adafruit_progressbar import ProgressBar

# Set up where we'll be fetching data from
DATA_SOURCE = "http://pi.hole/admin/api.php"
# Could change to fixed IP address if Pi Hole is not default/dynamic DNS server
dns_queries_today_LOCATION = ["dns_queries_today"]
ads_blocked_today_LOCATION = ["ads_blocked_today"]

# {"domains_being_blocked":85053,"dns_queries_today":56083,"ads_blocked_today":1202,"ads_percentage_today":2.143252,"unique_domains":1951,"queries_forwarded":12177,"queries_cached":42273,"clients_ever_seen":31,"unique_clients":16,"dns_queries_all_types":56083,"reply_NODATA":797,"reply_NXDOMAIN":4160,"reply_CNAME":4398,"reply_IP":41446,"privacy_level":0,"status":"enabled","gravity_last_updated":{"file_exists":true,"absolute":1607110479,"relative":{"days":0,"hours":22,"minutes":28}}}

# Reduce that time for testing
TIME_BETWEEN_REFRESHES = 10 * 60  # one hour delay

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(dns_queries_today_LOCATION, ads_blocked_today_LOCATION),
)

magtag.graphics.set_background("/bmps/pihole.bmp")

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(
    110,
    50,
    magtag.graphics.display.width - 120,
    30,
    0.5,
    bar_color=0x999999,
    outline_color=0x000000
)

magtag.graphics.splash.append(progress_bar)

# quote in bold text, with text wrapping
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.bdf",
    text_position=(
        ((magtag.graphics.display.width - 100) // 2) + 100,
        (magtag.graphics.display.height // 2) - 40,
    ),
    line_spacing=0.75,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
)

# author in italic text, no wrapping
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.bdf",
    text_position=(
        ((magtag.graphics.display.width - 100) // 2) + 100,
        (magtag.graphics.display.height // 2) + 40,
    ),
    text_anchor_point=(0.5, 0.5),  # center it in the nice scrolly thing
)

# OK now we're ready to connect to the network, fetch data and update screen!
try:
    magtag.network.connect()
    value = magtag.fetch()
    print("Response is", value)
    percent=value[1]/value[0]
    print(value[0], value[1], percent)
    progress_bar.progress = percent
    magtag.refresh()                ### This unfortunately make a second refresh... not sure how to avoid that.
except (ValueError, RuntimeError) as e:
    magtag.set_text(e)
    print("Some error occured, retrying later -", e)
# wait 2 seconds for display to complete
time.sleep(2)
magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)
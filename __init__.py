import socket

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

from .serverparser import extract_server, ip_to_spoken, get_matched_key
from .statushelper import player_count

FIRST_RUN = "first_run"
SERVERS = "servers"


class MinecraftServerStatusSkill(MycroftSkill):

    def __init__(self):
        super(MinecraftServerStatusSkill, self).__init__(name="MinecraftServerStatus")

        self.last_server = None

        self.settings[FIRST_RUN] = True
        self.settings[SERVERS] = {
            "us.mineplex.com": "Mineplex",
            "play.mcball.net": "MCBall",
            "mc.hypixel.net": "Hypixel"
        }

    def initialize(self):
        if self.settings[FIRST_RUN]:
            self.settings[FIRST_RUN] = False

    def _get_server(self, message):
        server, ratio = get_matched_key(message.data["utterance"], self.settings[SERVERS])
        if self.last_server is None or ratio > .25:
            self.last_server = server

        return self.last_server

    @intent_handler(IntentBuilder("AddMinecraftServerIntent").require("Add").require("Minecraft").optionally("Server"))
    def handle_add_server(self, message):
        name = self.get_response("what.server.to.add.name")
        if name:
            ip_response = self.get_response("what.server.to.add.ip")
            if ip_response:
                ip = extract_server(ip_response)
                self.settings[SERVERS][ip] = name
                self.speak_dialog("added.server", {"name": name, "ip": ip_to_spoken(ip)})

    @intent_handler(IntentBuilder("MinecraftServerPlayerOnlineIntent")
                    .one_of("Minecraft", "Server", "Online", "Players").require("Count"))
    def handle_players_online(self, message):
        server = self._get_server(message)
        if not server:
            self.speak_dialog("no.server.found")
            return
        try:
            online, max_count = player_count(server)
            self.speak_dialog("player.count", {"online": online, "max": max_count})
        except (ConnectionError, socket.timeout) as e:
            self.speak_dialog("unable.to.connect", {"ip": server})


def create_skill():
    return MinecraftServerStatusSkill()

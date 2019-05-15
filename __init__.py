from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG


class MinecraftServerStatusSkill(MycroftSkill):

    def __init__(self):
        super(MinecraftServerStatusSkill, self).__init__(name="MinecraftServerStatus")

    @intent_handler(IntentBuilder("AddMinecraftServerIntent").require("Add").require("Minecraft").optionally("Server"))
    def handle_add_server(self, message):
        self.speak_dialog("what.server.to.add")


def create_skill():
    return MinecraftServerStatusSkill()

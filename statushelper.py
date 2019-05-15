from mcstatus import MinecraftServer


def player_count(ip):
    """
    :param ip: The ip of the server
    :return: A tuple where [0] is number of players online and [1] is maximum players
    """
    status = MinecraftServer(ip).status()
    return status.players.online, status.players.max

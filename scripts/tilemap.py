import pygame

# We dont want to check collisions on all tilemaps, we need only 9 closest one
NEIGHBOR_OFFSETS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

PHYSICS_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size = tile_size
        # for physics and real tilemaps, if i want big distance between grounds it will take lot of space for air, so better use dictionary rather than list
        self.tilemap = {}
        self.game = game
        # background things, without physics
        self.offgrid_tiles = []

        # grass from (3;10) to (13;10)
        # we save it in tilemap hashmap as "x;y": {type:a, variant:n, pos:(x,y)}
        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (3 + i, 10),
            }
            self.tilemap["10;" + str(i + 5)] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, i + 5),
            }

    def tiles_around(self, pos):
        tiles = []
        # I didnt get this but its the best way to deal with rounding problems
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (
                str(offset[0] + tile_loc[0]) + ";" + str(offset[1] + tile_loc[1])
            )
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (
                    tile["pos"][0] * self.tile_size - offset[0],
                    tile["pos"][1] * self.tile_size - offset[1],
                ),
            )

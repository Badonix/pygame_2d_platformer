import pygame
import json

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

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

PHYSICS_TILES = {"grass", "stone"}
AUTOTILE_TYPES = {"grass", "stone"}


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

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (
                    str(tile["pos"][0] + shift[0])
                    + ";"
                    + str(tile["pos"][1] + shift[1])
                )
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile["type"] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def load(self, path):
        f = open(path, "r")
        map_data = json.load(f)
        f.close()
        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]

    def save(self, path):
        f = open(path, "w")
        json.dump(
            {
                "tilemap": self.tilemap,
                "tile_size": self.tile_size,
                "offgrid": self.offgrid_tiles,
            },
            f,
        )
        f.close()

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )
        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )

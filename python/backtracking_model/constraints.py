from tiles import tile_definitions

# Given a tile id and a direction, return allowed neighbor tile ids.
def get_allowed_neighbors(tile_id, direction):
    tile = next((t for t in tile_definitions if t["id"] == tile_id), None)
    if tile:
        return tile["rules"][direction]
    return []

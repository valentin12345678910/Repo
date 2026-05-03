import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 3
COIN_SCALING = 0.5

GRAVITY = 0.8
PLAYER_MOVEMENT_SPEED = 3
PLAYER_JUMP_SPEED = 11
LEDER_SPEED = 5


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.wall_list = None
        self.coin_list = None
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.scene = None
        self.tile_map = None
        self.player_sprite = None
        self.player_list = arcade.SpriteList()
        self.physics_engine = None
        self.on_ladder = False
        self.held_keys = set()

        self.coins_collected = 0
        self.coins_needed = 60
        self.game_over = False
        self.game_won = False

        self.stopper = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        layer_options = {
            "Plattformen": {"use_spatial_hash": True}
        }

        self.tile_map = arcade.load_tilemap(
            map_file="karte.tmx",
            scaling=TILE_SCALING,
            layer_options=layer_options
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = arcade.Sprite("spieler2.png", scale=0.5)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 4000

        platforms = self.scene["Plattformen"]
        self.wall_list = platforms

        self.coin_list = self.scene["Münzen"]
        self.monster_list = self.scene["monster"]
        self.jetpack_list = self.scene["jetpack"]
        self.op_list = self.scene["op"]
        self.goldenerop_list = self.scene["goldenerop"]
        self.megajetpack_list = self.scene["megajetpack"]
        self.zuffalblock_list = self.scene["zuffalblock"]
        self.spawner_list = self.scene["spawner"]
        self.supersprungblock_list = self.scene["supersprungblock"]
        self.leiter_list = self.scene["leiter"]
        self.langsamblock_list = self.scene["langsamblock"]
        self.sprungblock_list = self.scene["sprungblock"]
        self.freezer_list = self.scene["freezer"]
        self.spawner2_list = self.scene["spawner2"]
        self.spawner3_list = self.scene["spawner3"]
        self.spawner4_list = self.scene["spawner4"]
        self.böses_monster_list = self.scene["böses_monster"]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            platforms=platforms
        )

    def on_draw(self):
        self.camera.use()
        self.clear()

        self.scene.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        self.gui_camera.use()

    def on_update(self, delta_time):
        if self.game_over or self.game_won:
            return

        self.stopper -= delta_time

        if self.stopper > 0:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.alpha = 100
            self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)
            return
        else:
            self.player_sprite.alpha = 255

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.coins_collected += 1

        if self.coins_collected >= self.coins_needed:
            self.game_won = True

        self.physics_engine.update()
        self.player_sprite.update()

        if getattr(self, "on_ladder", False):
            if arcade.key.UP in self.held_keys or arcade.key.W in self.held_keys:
                self.player_sprite.change_y = LEDER_SPEED
            elif arcade.key.DOWN in self.held_keys or arcade.key.S in self.held_keys:
                self.player_sprite.change_y = -LEDER_SPEED
            else:
                self.player_sprite.change_y = 0

        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)

        monster_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)
        if monster_hit_list and self.stopper <= 0:
            self.stopper = 2

        spawner_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spawner_list)
        if spawner_hit_list:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 4000

        jetpack_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.jetpack_list)
        for jetpack in jetpack_hit_list:
            jetpack.remove_from_sprite_lists()

        op_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.op_list)
        for op in op_hit_list:
            op.remove_from_sprite_lists()

        megajetpack_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.megajetpack_list)
        for megajetpack in megajetpack_hit_list:
            megajetpack.remove_from_sprite_lists()

        goldenerop_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.goldenerop_list)
        for goldenerop in goldenerop_hit_list:
            goldenerop.remove_from_sprite_lists()

        zuffalblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zuffalblock_list)
        for zuffalblock in zuffalblock_hit_list:
            zuffalblock.remove_from_sprite_lists()
            import random
            self.game_over = random.choice([True, False])

        supersprungblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.supersprungblock_list)
        for supersprungblock in supersprungblock_hit_list:
            supersprungblock.remove_from_sprite_lists()
            self.player_sprite.change_y = PLAYER_JUMP_SPEED * 2

        sprungblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.sprungblock_list)
        for sprungblock in sprungblock_hit_list:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

        langsamblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.langsamblock_list)
        for langsamblock in langsamblock_hit_list:
            langsamblock.remove_from_sprite_lists()
            global PLAYER_MOVEMENT_SPEED
            PLAYER_MOVEMENT_SPEED = max(2, PLAYER_MOVEMENT_SPEED - 0.4)

        freezer_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.freezer_list)
        for freezer in freezer_hit_list:
            freezer.remove_from_sprite_lists()
            self.stopper = 3

        leder_hit_list = []
        if self.leiter_list is not None:
            leder_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.leiter_list)

        if leder_hit_list:
            self.on_ladder = True
        else:
            self.on_ladder = False

        spawner2_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spawner2_list)
        if spawner2_hit_list:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100

        spawner3_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spawner3_list)
        if spawner3_hit_list:
            self.player_sprite.center_x = 3385
            self.player_sprite.center_y = 100

        spawner4_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spawner4_list)
        if spawner4_hit_list:
            self.player_sprite.center_x = 5300
            self.player_sprite.center_y = 100

        self.böses_monster_list
        shoots = []
        for monster in self.böses_monster_list:
            if monster.center_x < self.player_sprite.center_x:
                shoots.append(arcade.Sprite("kugel", scale=0.5))
                shoots[-1].center_x = monster.center_x + 20
                shoots[-1].center_y = monster.center_y
                shoots[-1].change_x = 5
            else:
                shoots.append(arcade.Sprite("kugel", scale=0.5))
                shoots[-1].center_x = monster.center_x - 20
                shoots[-1].center_y = monster.center_y
                shoots[-1].change_x = -5
        if self.böses_monster_list and self.stopper <= 0:
            self.stopper = 2





    def on_key_press(self, key, modifiers):
        try:
            self.held_keys.add(key)
        except Exception:
            pass

        if key == arcade.key.ESCAPE:
            self.close()

        if not self.game_over and not self.game_won and self.stopper <= 0:
            if key in [arcade.key.SPACE, arcade.key.W, arcade.key.UP]:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED

            if key in [arcade.key.LEFT, arcade.key.A]:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key in [arcade.key.RIGHT, arcade.key.D]:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        try:
            if key in self.held_keys:
                self.held_keys.remove(key)
        except Exception:
            pass

        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            if self.player_sprite is not None:
                self.player_sprite.change_x = 0


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
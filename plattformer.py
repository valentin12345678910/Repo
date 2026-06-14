import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 3
COIN_SCALING = 0.5

GRAVITY = 0.8
PLAYER_MOVEMENT_SPEED = 3
PLAYER_JUMP_SPEED = 11
LEDER_SPEED = 5

#GRAVITY = 0.7
#PLAYER_MOVEMENT_SPEED = 5
#PLAYER_JUMP_SPEED = 13


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
        self.leben = 10

        self.stopper = 0
        self.immune_time = 0

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
        self.stop_monster_list = self.scene["stop_monster"]

        
        for monster in self.böses_monster_list:
            monster.start_x = monster.center_x
            monster.start_y = monster.center_y

        for stop_monster in self.stop_monster_list:
            stop_monster.start_x = stop_monster.center_x
            stop_monster.start_y = stop_monster.center_y

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

        self.leben_text = arcade.draw_text(
    text=f"Leben: {self.leben}",
    x=10,                      
    y=10,                      
    color=arcade.color.WHITE,  
    font_size=14            
)


    def on_update(self, delta_time):
        if self.game_over or self.game_won:
            return

        self.stopper -= delta_time
        if self.immune_time > 0:
            self.immune_time = max(0, self.immune_time - delta_time)

        if self.stopper > 0:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.alpha = 100
            self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)
            return
        else:
            if self.immune_time > 0:
                self.player_sprite.alpha = 150
            else:
                self.player_sprite.alpha = 255

        # Coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.coins_collected += 1

        if self.coins_collected >= self.coins_needed:
            self.game_won = True

        self.physics_engine.update()
        self.player_sprite.update()

        # Ladder
        if self.on_ladder:
            if arcade.key.UP in self.held_keys or arcade.key.W in self.held_keys:
                self.player_sprite.change_y = LEDER_SPEED
            elif arcade.key.DOWN in self.held_keys or arcade.key.S in self.held_keys:
                self.player_sprite.change_y = -LEDER_SPEED
            else:
                self.player_sprite.change_y = 0

        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)

        # Monster Hit
        monster_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)
        if monster_hit_list and self.stopper <= 0:
            self.stopper = 2


        for böses_monster in self.böses_monster_list:
            böses_monster.center_x -= 2
            böses_monster.center_y -= 0.5

            if böses_monster.center_x < 0 or böses_monster.center_y < 0:
                böses_monster.center_x = böses_monster.start_x
                böses_monster.center_y = böses_monster.start_y

        for stop_monster in self.stop_monster_list:
            stop_monster.center_x -= 2
            stop_monster.center_y -= 0.5

            if stop_monster.center_x < 0 or stop_monster.center_y < 0:
                stop_monster.center_x = stop_monster.start_x
                stop_monster.center_y = stop_monster.start_y

        # Spawner Reset
        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner_list):
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 4000

        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner2_list):
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100

        # Spawner Reset
        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner_list):
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 4000

        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner2_list):
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100

        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner3_list):
            self.player_sprite.center_x = 3385
            self.player_sprite.center_y = 100

        if arcade.check_for_collision_with_list(self.player_sprite, self.spawner4_list):
            self.player_sprite.center_x = 5300
            self.player_sprite.center_y = 100

        # Items
        for jetpack in arcade.check_for_collision_with_list(self.player_sprite, self.jetpack_list):
            jetpack.remove_from_sprite_lists()

        for op in arcade.check_for_collision_with_list(self.player_sprite, self.op_list):
            op.remove_from_sprite_lists()

        for megajetpack in arcade.check_for_collision_with_list(self.player_sprite, self.megajetpack_list):
            megajetpack.remove_from_sprite_lists()

        for goldenerop in arcade.check_for_collision_with_list(self.player_sprite, self.goldenerop_list):
            goldenerop.remove_from_sprite_lists()

        # Random block
        for zuffalblock in arcade.check_for_collision_with_list(self.player_sprite, self.zuffalblock_list):
            zuffalblock.remove_from_sprite_lists()
            self.game_over = random.choice([True, False])

        # Jump blocks
        for supersprungblock in arcade.check_for_collision_with_list(self.player_sprite, self.supersprungblock_list):
            supersprungblock.remove_from_sprite_lists()
            self.player_sprite.change_y = PLAYER_JUMP_SPEED * 2

        for sprungblock in arcade.check_for_collision_with_list(self.player_sprite, self.sprungblock_list):
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

        # Slow block
        for langsamblock in arcade.check_for_collision_with_list(self.player_sprite, self.langsamblock_list):
            langsamblock.remove_from_sprite_lists()
            global PLAYER_MOVEMENT_SPEED
            PLAYER_MOVEMENT_SPEED = max(2, PLAYER_MOVEMENT_SPEED - 0.4)

        # Freezer
        for freezer in arcade.check_for_collision_with_list(self.player_sprite, self.freezer_list):
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

        self.böses_monster_list.update()
        for monster in self.böses_monster_list:
            if arcade.check_for_collision(self.player_sprite, monster):
                if self.immune_time <= 0:
                    self.leben -= 1
                    self.immune_time = 2
                    if self.leben <= 0:
                        self.game_over = True
            monster.center_x -= 2
            monster.center_y -= 0.7

        self.stop_monster_list.update()
        for monster in self.stop_monster_list:
            if arcade.check_for_collision(self.player_sprite, monster):
                self.stopper = 0.1
            monster.center_x -= 2
            monster.center_y -= 0.7


    def on_key_press(self, key, modifiers):
        self.held_keys.add(key)

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

            if key == arcade.key.R:
                self.__init__(print("Restarting Game..."))


        


    def on_key_release(self, key, modifiers):
        if key in self.held_keys:
            self.held_keys.remove(key)

        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = 0


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
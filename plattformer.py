import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 3
COIN_SCALING = 0.5
 
GRAVITY = 0.5
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 10
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
        self.time_left = 110
        self.game_over = False
        self.game_won = False


    

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
        self.player_sprite.center_y = 1700
   
   
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
    
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, platforms=platforms)

    def on_draw(self):
        
        self.clear()

        self.camera.use()

        self.scene.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        self.gui_camera.use()


        
        time_color = arcade.color.WHITE if self.time_left > 10 else arcade.color.RED
        arcade.draw_text(f"Zeit: {int(self.time_left)}", 10, 40, time_color, 18)
        arcade.draw_text(f"Rüben: {self.coins_collected} / {self.coins_needed}", 10, 60, arcade.color.WHITE, 18)


        jetpack_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.jetpack_list)
        for jetpack in jetpack_hit_list:
            jetpack.remove_from_sprite_lists()
            self.time_left -= 15

        op_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.op_list)
        for op in op_hit_list:
            op.remove_from_sprite_lists()
            self.time_left += 15

        megajetpack_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.megajetpack_list)
        for megajetpack in megajetpack_hit_list:
            megajetpack.remove_from_sprite_lists()
            self.time_left -= 30

        goldenerop_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.goldenerop_list)
        for goldenerop in goldenerop_hit_list:
            goldenerop.remove_from_sprite_lists()
            self.time_left += 30

        zuffalblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zuffalblock_list)
        for zuffalblock in zuffalblock_hit_list:
            zuffalblock.remove_from_sprite_lists()
            import random
            self.game_over = random.choice([True, False])
            if not self.game_over:
                self.time_left += 50

        supersprungblock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.supersprungblock_list)
        for supersprungblock in supersprungblock_hit_list:
            supersprungblock.remove_from_sprite_lists()
            self.player_sprite.change_y = PLAYER_JUMP_SPEED * 2

        leder_hit_list = []
        if self.leiter_list is not None:
            leder_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.leiter_list)

        if leder_hit_list:
            self.on_ladder = True
        else:
            self.on_ladder = False




        
                       


        

    def on_update(self, delta_time):
        if self.game_over or self.game_won:
            return

        self.time_left -= delta_time
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

    
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
        if monster_hit_list:
            self.game_over = True


        spawner_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spawner_list)
        if spawner_hit_list:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 1700

     

    

    def on_key_press(self, key, modifiers):
       
        try:
            self.held_keys.add(key)
        except Exception:
            pass
        if key == arcade.key.ESCAPE:
            self.close()

        if key == arcade.key.SPACE and (self.game_over or self.game_won):
            self.setup()

        if not self.game_over and not self.game_won:
            if key in [arcade.key.UP, arcade.key.W]:
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
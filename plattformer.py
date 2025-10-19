import arcade
import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5
COIN_SCALING = 0.5
 
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_MOVEMENT_SPEED = 1.5
GRAVITY = 0.10
PLAYER_JUMP_SPEED = 4


class GameView(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.scene = None
        self.tile_map = None
        self.player_sprite = None

        self.player_list = arcade.SpriteList()
        self.physics_engine = None

        self.score = 0
        self.score_text = None

        self.coins_collected = 0
        self.coins_needed = 40

        self.time_left = 30.0

        self.game_over = False
        self.game_won = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        layer_options = {
            "Plattforms": {"use_spatial_hash": True}
        }

        self.tile_map = arcade.load_tilemap(
            map_file="karte.tmx",
            scaling=TILE_SCALING,
            layer_options=layer_options
        )
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        self.player_sprite = arcade.Sprite("spieler2.png", scale=0.5)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = WINDOW_WIDTH // 2
        self.player_sprite.center_y = WINDOW_HEIGHT // 2
            
        self.camera.move_to((self.player_sprite.center_x - WINDOW_WIDTH/2, self.player_sprite.center_y - WINDOW_HEIGHT/2), 0.0)
            
        platforms = self.scene["Plattforms"]
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, platforms=platforms)


    def on_draw(self):
        
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player_list.draw()

        self.gui_camera.use()

        self.score_text.draw()
            
        time_color = arcade.color.WHITE if self.time_left > 10 else arcade.color.RED
        arcade.draw_text(f"Zeit: {int(self.time_left)}", 10, 40, time_color, 18)
        arcade.draw_text(f"Münzen: {self.coins_collected} / {self.coins_needed}", 10, 60, arcade.color.WHITE, 18)

        if self.game_over or self.game_won:
            message = "GEWONNEN!" if self.game_won else "SPIEL VORBEI!"
            color = arcade.color.GREEN if self.game_won else arcade.color.RED

            arcade.draw_text(
                message,
                self.player_sprite.center_x,
                self.player_sprite.center_y + 100,
                color,
                50,
                anchor_x="center",
                anchor_y="center"
            )
            arcade.draw_text(
                "Drücke LEERTASTE zum Neustarten",
                self.player_sprite.center_x,
                self.player_sprite.center_y + 40,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        if self.game_over or self.game_won:
            return

        self.time_left -= delta_time
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

    
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Münzen"])
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.coins_collected += 1
                self.score += 75
                self.score_text.text = f"Score: {self.score}"
            if self.coins_collected >= self.coins_needed:
                self.game_won = True
        

        
        self.physics_engine.update()
        self.player_sprite.update()
        self.camera.move_to((self.player_sprite.center_x - WINDOW_WIDTH/2, self.player_sprite.center_y - WINDOW_HEIGHT/2), 0.1)
           

    def on_key_press(self, key, modifiers):
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
        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            if self.player_sprite is not None:
                self.player_sprite.change_x = 0


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()



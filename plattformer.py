import arcade
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5
COIN_SCALING = 0.5
 
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
 
class GameView(arcade.Window):
 
    def __init__(self):
 
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
 
        self.player_texture = None

        self.player_sprite = None
 
        self.tile_map = None
 
        self.scene = None

        self.camera = None

        self.gui_camera = None

        self.score = 0

        self.score_text = None
 
        # self.collect_coin_sound = arcade.load_sound()
        # self.jump_sound = arcade.load_sound()
 
    def setup(self):

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            }
        }
 
        self.tile_map = arcade.load_tilemap(
            map_file="karte.tmx",
            scaling=TILE_SCALING,
            layer_options=layer_options,)
 
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
 
        # self.player_texture = arcade.load_texture("spieler2.png")
 
        self.player_sprite = arcade.Sprite("spieler2.png", scale=0.5)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Spieler", self.player_sprite)
 
        self.physics_engine = arcade.PhysicsEnginePlatformer(
             self.player_sprite, walls=self.scene["Plattformen"], gravity_constant=GRAVITY
         )

        self.camera = arcade.Camera2D()

        self.gui_camera = arcade.Camera2D()

        self.score = 0

        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=5)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def on_draw(self):

        self.clear()


        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()

        self.score_text.draw()
    
    def on_update(self, delta_time):

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Münzen"])

        for coin in coin_hit_list:

            coin.remove_from_sprite_lists()
            # arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"

        self.camera.position = self.player_sprite.position

    def on_key_press(self, key, modifiers):


        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                # arcade.play_sound(self.jump_sound)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
           self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():

    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
   main()
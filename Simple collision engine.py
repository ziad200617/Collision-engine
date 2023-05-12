
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

 
import random
from typing import List

 
import pygame

 
import pymunk
import pymunk.pygame_util


class BouncyBalls(object):
     

    def __init__(self) -> None:
        
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        
        self._dt = 1.0 / 60.0
        
        self._physics_steps_per_frame = 1

        
        pygame.init()
        self._screen = pygame.display.set_mode((600, 600))
        width, height = 600, 600
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

       
        self._add_static_scenery()

        
        self._balls: List[pymunk.Circle] = []

         
        self._running = True
        self._ticks_to_next_ball = 10

    def run(self) -> None:
        
         while self._running:
            
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._process_events()
            self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
             
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self) -> None:
        
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (600, 600), (0, 600-150), 70),
            pymunk.Segment(static_body, (600, 600), (600, 0), 25),
            pymunk.Segment(static_body, (0, 0), (0,600-100), 25)
        ]
        for line in static_lines:
            line.elasticity = 0.55
            line.friction = 0.9
        self._space.add(*static_lines)


    def _process_events(self) -> None:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    def _update_balls(self) -> None:
         
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            self._create_ball()
            self._ticks_to_next_ball = 100
         
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 500]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_ball(self) -> None:
         
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = x, 200
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 1.25
        shape.friction = 1.25
        self._space.add(body, shape)
        self._balls.append(shape)

    


    def _clear_screen(self) -> None:
        
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        
        self._space.debug_draw(self._draw_options)


def main():
    game = BouncyBalls()
    game.run()


if __name__ == "__main__":
    main()
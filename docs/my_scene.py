from bemve import Scene, VCircle, VSquare, Create, Transform
from bemve.transition import SlideIn

class QuickStart(Scene):
    def construct(self):
        # Create vector objects
        square = VSquare(side_length=2.0)
        circle = VCircle(radius=1.2)

        # Draw and transform
        self.play(Create(square), duration=1.5)
        self.play(Transform(square, circle), duration=1.5)

if __name__ == "__main__":
    scene = QuickStart(name="QuickStartScene")
    scene.render(preview=True)

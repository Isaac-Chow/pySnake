import random
import string
from tkinter import *

# HEAD_CHARACTER = '😊'
HEAD_CHARACTER = 'H'
FOOD_CHARACTER = string.ascii_letters
# FOOD_CHARACTER = [
#     "😊","👎","👍","😍","😘","😜","😎","😡","😱","😳","😭","😢","😂","😃","😄","😅","😆","😉",
#     "😊","👋","👍","👎","👌","👊","✊","✌️","👏","🙌","🙏","👆","👇","👈","👉","🖕","🖐","🤘",
#     "😊","👎","👍","😍","😘","😜","😎","😡","😱","😳","😭","😢","😂","😃","😄","😅","😆","😉",
#     "😊","👋","👍","👎","👌","👊","✊","✌️","👏","🙌","🙏","👆","👇","👈","👉","🖕","🖐","🤘",
#     "🖖","🤙","💪","🖕","🖐","🤘","🖖","🤙","💪","🖖","🤙","💪","🖕","🖐","🤘","🖖","🤙","💪",
#     "😊"
#     ]

class Application:
    TITLE = 'Snake'
    SIZE = 300,300

    def __init__(self, master):
        self.master = master
        self.head = None
        self.head_position = None
        self.segments = []
        self.segment_positions = []
        self.speed = 3           # Add a speed attribute
        self.food = None
        self.food_position = None
        self.direction = None
        self.moved = True

        self.running = False
        self.init()

    def init(self):
        self.master.title(self.TITLE)

        self.canvas = Canvas(self.master)
        self.canvas.grid(sticky=NSEW)

        self.start_button = Button(self.master,text='Start', command=self.on_start)
        self.start_button.grid(sticky=EW)

        self.master.bind('w', self.on_up)
        self.master.bind('a', self.on_left)
        self.master.bind('s', self.on_down)
        self.master.bind('d', self.on_right)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.resizable(width=False, height=False)
        self.master.geometry('%dx%d' % self.SIZE)

    def on_start(self):
        self.reset()
        if self.running:
            self.running = False
            self.start_button.configure(text='Start')
        else:
            self.running = True
            self.start_button.configure(text='Stop')
            self.start()

    def reset(self):
        del self.segments[:]
        del self.segment_positions[:]
        self.canvas.delete(ALL)

    def start(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_rectangle(10,10,width-10,height-10)
        self.direction = random.choice('wasd')
        head_position = [round(width//2, -1), round(height//2, -1)]
        self.head = self.canvas.create_text(tuple(head_position), text=HEAD_CHARACTER)
        self.head_position = head_position
        self.spawn_food()
        self.tick()

    def spawn_food(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        positions = [tuple(self.head_position), self.food_position] + self.segment_positions

        position = (round(random.randint(20, width-20), - 1), round(random.randint(20, height- 20), -1))
        while position in positions:
            position = (round(random.randint(20,width-20), -1), round(random.randint(20, height-20), -1))

        character = random.choice(FOOD_CHARACTER)
        self.food = self.canvas.create_text(position, text=character)
        self.food_position = position
        self.food_character = character

    def tick(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        previous_head_position = tuple(self.head_position)

        if self.direction == 'w':
            self.head_position[1] -= self.speed
        elif self.direction == 'a':
            self.head_position[0] -= self.speed
        elif self.direction == 's':
            self.head_position[1] += self.speed
        elif self.direction == 'd':
            self.head_position[0] += self.speed

        head_position = tuple(self.head_position)
        if self.head_position[0] < 10 or self.head_position[0] >= width-10 or self.head_position[1] < 10 or \
                self.head_position[1] >= height-10 or any(segment_position == head_position for segment_position \
                                                          in self.segment_positions):
            self.game_over()
            return

        if head_position == self.food_position:
            print("Hello I just ate it")
            self.canvas.coords(self.food, previous_head_position)
            self.segments.append(self.food)
            self.segment_positions.append(previous_head_position)
            self.spawn_food()
            # check for the size of the segments to increase teh speed
            if int(len(self.segments)) % 5 == 0:
                self.speed += 4
            elif int(len(self.segments)) < 5:
                self.speed = 5

        if self.segments:
            previous_position = previous_head_position
            for index, (segment, position) in enumerate(zip(self.segments, self.segment_positions)):
                self.canvas.coords(segment, previous_position)
                self.segment_positions[index] = previous_position
                previous_position = position

        self.canvas.coords(self.head, head_position)
        self.moved = True
        self.canvas.after(50, self.tick)

    def game_over(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.running = False
        self.start_button.configure(text='Start')
        score = len(self.segments) * 10
        self. canvas.create_text( (round(width//2, -1), round(height // 2, -1)),
                                 text='Game Over! Your score was: %d' % score )

    def on_up(self,event):
        if self.moved and not self.direction == 's':
            self.direction = 'w'
            self.moved = False

    def on_down(self,event):
        if self.moved and not self.direction == 'w':
            self.direction = 's'
            self.moved = False

    def on_left(self,event):
        if self.moved and not self.direction == 'd':
            self.direction = 'a'
            self.moved = False

    def on_right(self,event):
        if self.moved and not self.direction == 'a':
            self.direction = 'd'
            self.moved = False

def main():
    root =Tk()
    Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
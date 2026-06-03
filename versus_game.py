import tkinter as tk
import random

class VersusGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Versus Game")
        self.root.geometry("550x550")
        self.root.resizable(False, False)

        self.player1_symbol = None
        self.player2_symbol = None
        self.bot_symbol = None
        self.mode = None

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

   
    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="VERSUS GAME", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Symbols: Circle, Square, Triangle\n"
                                 "Circle > Square > Triangle > Circle\n"
                                 "Ties resolved by coin toss",
                 font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="1. Player vs Bot", font=("Arial", 14),
                  command=lambda: self.start_game("vs_bot"), width=20).pack(pady=10)
        tk.Button(self.root, text="2. Two Players", font=("Arial", 14),
                  command=lambda: self.start_game("two_player"), width=20).pack(pady=10)

    def start_game(self, mode):
        self.mode = mode
        if mode == "vs_bot":
            self.step_player_choose_symbol("You")
        else:
            self.step_player_choose_symbol("Player 1")

    def step_player_choose_symbol(self, player_name):
        self.clear_window()
        tk.Label(self.root, text=f"{player_name}, choose your symbol:",
                 font=("Arial", 14)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.create_symbol_canvas(frame, "Circle", player_name).pack(side="left", padx=10)
        self.create_symbol_canvas(frame, "Square", player_name).pack(side="left", padx=10)
        self.create_symbol_canvas(frame, "Triangle", player_name).pack(side="left", padx=10)

    def create_symbol_canvas(self, parent, symbol, player_name):
        canvas = tk.Canvas(parent, width=100, height=100, bg="white", highlightthickness=2, relief="ridge")
        self.draw_shape(canvas, symbol)
        canvas.bind("<Button-1>", lambda e, s=symbol: self.on_symbol_chosen(s, player_name))
        return canvas

    def draw_shape(self, canvas, symbol):
        size = 80
        margin = 10
        if symbol == "Circle":
            canvas.create_oval(margin, margin, margin+size, margin+size, fill="lightblue", outline="black")
        elif symbol == "Square":
            canvas.create_rectangle(margin, margin, margin+size, margin+size, fill="lightgreen", outline="black")
        elif symbol == "Triangle":
            pts = [margin+size//2, margin, margin, margin+size, margin+size, margin+size]
            canvas.create_polygon(pts, fill="lightcoral", outline="black")

    def on_symbol_chosen(self, symbol, player_name):
        if self.mode == "vs_bot":
            self.player1_symbol = symbol
            self.bot_symbol = random.choice(["Circle", "Square", "Triangle"])
            self.show_result_vs_bot()
        else:
            if player_name == "Player 1":
                self.player1_symbol = symbol
                self.clear_window()
                tk.Label(self.root, text="Player 1 has selected their symbol.\n"
                                         "(Hidden from Player 2)",
                         font=("Arial", 14, "italic"), fg="green").pack(pady=50)
                self.root.after(1000, self.ask_player2)
            else:
                self.player2_symbol = symbol
                self.show_result_two_player()

    def ask_player2(self):
        self.step_player_choose_symbol("Player 2")

    def show_result_vs_bot(self):
        self.clear_window()
        tk.Label(self.root, text="RESULTS", font=("Arial", 16, "bold")).pack(pady=10)
        self.display_result_frame(self.player1_symbol, "You", self.bot_symbol, "Bot")
        result = self.decide_winner(self.player1_symbol, self.bot_symbol)
        self.final_result_label(result, "You", "Bot")

    def show_result_two_player(self):
        self.clear_window()
        tk.Label(self.root, text="RESULTS", font=("Arial", 16, "bold")).pack(pady=10)
        self.display_result_frame(self.player1_symbol, "Player 1", self.player2_symbol, "Player 2")
        result = self.decide_winner(self.player1_symbol, self.player2_symbol)
        self.final_result_label(result, "Player 1", "Player 2")

    def display_result_frame(self, sym1, name1, sym2, name2):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        left_frame = tk.Frame(frame)
        left_frame.pack(side="left", padx=30)
        tk.Label(left_frame, text=name1, font=("Arial", 12, "bold")).pack()
        canvas1 = tk.Canvas(left_frame, width=100, height=100, bg="white", relief="ridge")
        self.draw_shape(canvas1, sym1)
        canvas1.pack()

        tk.Label(frame, text="VS", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        right_frame = tk.Frame(frame)
        right_frame.pack(side="left", padx=30)
        tk.Label(right_frame, text=name2, font=("Arial", 12, "bold")).pack()
        canvas2 = tk.Canvas(right_frame, width=100, height=100, bg="white", relief="ridge")
        self.draw_shape(canvas2, sym2)
        canvas2.pack()

    def final_result_label(self, result, name1, name2):
        if result == 1:
            tk.Label(self.root, text=f"{name1} wins!", font=("Arial", 14, "bold"), fg="green").pack(pady=10)
        elif result == 2:
            tk.Label(self.root, text=f"{name2} wins!", font=("Arial", 14, "bold"), fg="blue").pack(pady=10)
        else:
            tk.Label(self.root, text="Tie! Proceeding to coin toss...", font=("Arial", 12)).pack(pady=10)
            self.root.after(1000, self.show_coin_toss_by_mode)
            return
        self.show_play_again()

    def show_coin_toss_by_mode(self):
        if self.mode == "vs_bot":
            self.show_coin_toss_vs_bot()
        else:
            self.show_coin_toss_two_player()

    def show_coin_toss_vs_bot(self):
        self.clear_window()
        tk.Label(self.root, text="Coin Toss – Click a side:",
                 font=("Arial", 14)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        heads_canvas = tk.Canvas(frame, width=80, height=80, bg="gold", highlightthickness=2, relief="ridge")
        heads_canvas.create_oval(5, 5, 75, 75, fill="gold", outline="black", width=2)
        heads_canvas.create_text(40, 40, text="H", font=("Arial", 24, "bold"), fill="black")
        heads_canvas.bind("<Button-1>", lambda e: self.do_coin_toss_vs_bot("H"))
        heads_canvas.pack(side="left", padx=20)

        tails_canvas = tk.Canvas(frame, width=80, height=80, bg="silver", highlightthickness=2, relief="ridge")
        tails_canvas.create_oval(5, 5, 75, 75, fill="silver", outline="black", width=2)
        tails_canvas.create_text(40, 40, text="T", font=("Arial", 24, "bold"), fill="black")
        tails_canvas.bind("<Button-1>", lambda e: self.do_coin_toss_vs_bot("T"))
        tails_canvas.pack(side="left", padx=20)

    def do_coin_toss_vs_bot(self, player_choice):
        flip = random.choice(['H', 'T'])
        result_text = f"Coin flip: {'Heads' if flip == 'H' else 'Tails'}"
        if flip == player_choice:
            result_text += "\nYou win the coin toss!"
        else:
            result_text += "\nBot wins the coin toss!"
        self.clear_window()
        tk.Label(self.root, text=result_text, font=("Arial", 14)).pack(pady=30)
        self.show_play_again()

    def show_coin_toss_two_player(self):
        self.clear_window()
        tk.Label(self.root, text="Coin Toss – Player 1, click a side:",
                 font=("Arial", 14)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        heads_canvas = tk.Canvas(frame, width=80, height=80, bg="gold", highlightthickness=2, relief="ridge")
        heads_canvas.create_oval(5, 5, 75, 75, fill="gold", outline="black", width=2)
        heads_canvas.create_text(40, 40, text="H", font=("Arial", 24, "bold"), fill="black")
        heads_canvas.bind("<Button-1>", lambda e: self.do_coin_toss_two_player("H"))
        heads_canvas.pack(side="left", padx=20)

        tails_canvas = tk.Canvas(frame, width=80, height=80, bg="silver", highlightthickness=2, relief="ridge")
        tails_canvas.create_oval(5, 5, 75, 75, fill="silver", outline="black", width=2)
        tails_canvas.create_text(40, 40, text="T", font=("Arial", 24, "bold"), fill="black")
        tails_canvas.bind("<Button-1>", lambda e: self.do_coin_toss_two_player("T"))
        tails_canvas.pack(side="left", padx=20)

    def do_coin_toss_two_player(self, p1_choice):
        p2_choice = 'T' if p1_choice == 'H' else 'H'
        flip = random.choice(['H', 'T'])
        result_text = f"Player 1 chose {'Heads' if p1_choice == 'H' else 'Tails'}\n"
        result_text += f"Coin flip: {'Heads' if flip == 'H' else 'Tails'}\n"
        if flip == p1_choice:
            result_text += "Player 1 wins the coin toss!"
        else:
            result_text += "Player 2 wins the coin toss!"
        self.clear_window()
        tk.Label(self.root, text=result_text, font=("Arial", 14)).pack(pady=30)
        self.show_play_again()

    def decide_winner(self, sym1, sym2):
        rules = {
            'Circle': 'Square',
            'Square': 'Triangle',
            'Triangle': 'Circle'
        }
        if sym1 == sym2:
            return 0
        return 1 if rules[sym1] == sym2 else 2

    def show_play_again(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Play Again", font=("Arial", 12),
                  command=self.show_main_menu, width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Quit", font=("Arial", 12),
                  command=self.root.quit, width=10).pack(side="left", padx=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = VersusGame()
    game.run()
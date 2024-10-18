import chess.pgn
import io
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def process_pgn(input_file, output_file):
    # Read the PGN games from input file
    with open(input_file, 'r') as file:
        pgn_text = file.read()

    # Use StringIO to create a file-like object for parsing multiple games
    pgn_file = io.StringIO(pgn_text)

    # Create an empty list to store FEN positions and move notations for each game
    all_game_data = []

    # Loop through all games in the PGN file
    while True:
        # Read one game from the PGN file
        pgn_game = chess.pgn.read_game(pgn_file)

        # Break the loop if no more games are found
        if pgn_game is None:
            break

        # Create a new chess board for each game
        board = chess.Board()

        # Initialize the move notation with the starting position for each game
        move_notation = [board.fen().split()[0] + " w KQkq - 0 1 moves"]

        # Retrieve the moves and convert them to move notation for each game
        for move in pgn_game.mainline_moves():
            board.push(move)
            move_notation.append(board.move_stack[-1].uci())

        # Save FEN position and move notation for each game
        all_game_data.append(' '.join(move_notation))

    # Save the output to the specified output file
    with open(output_file, 'w') as file:
        # Write each game's data to the output file
        for game_data in all_game_data:
            file.write(game_data + '\n')

    return len(all_game_data)

class PGNProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("PGN Processor")
        master.geometry("400x200")

        # Input file selection
        self.input_label = tk.Label(master, text="Input PGN file:")
        self.input_label.pack()

        self.input_entry = tk.Entry(master, width=40)
        self.input_entry.pack()

        self.browse_button = tk.Button(master, text="Browse PGN", command=self.browse_input)
        self.browse_button.pack()

        # Output file naming
        self.output_label = tk.Label(master, text="Output file name:")
        self.output_label.pack()

        self.output_entry = tk.Entry(master, width=40)
        self.output_entry.pack()

        # Start processing button
        self.start_button = tk.Button(master, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=20)

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def start_processing(self):
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select an input file and specify an output file name.")
            return

        if not output_file.endswith('.pgn'):
            output_file += '.pgn'

        try:
            games_processed = process_pgn(input_file, output_file)
            messagebox.showinfo("Success", f"Processing complete. {games_processed} games processed and saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    gui = PGNProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
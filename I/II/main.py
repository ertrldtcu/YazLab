from SamuraiSudoku import *

root = Tk()
root.title("Yaz. Lab. 1.2")
width = 1440
height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+{(screen_width - width) // 2}+{(screen_height - height) // 2}")
root.resizable(width=False, height=False)

sudoku_canvas = Canvas(root, width=width // 2, height=height - 10, bd=-2)
sudoku_canvas.place(x=10, y=20)

graph_canvas = Canvas(root, width=width // 2, height=height // 2, bg="#E0E0E0", bd=-2)
graph_canvas.place(x=width // 2 - 20, y=10 + height // 4)

graph_canvas.create_text(width // 2 - 93, height // 2 - 15, font=f"Arial 8 italic", text="x (geçen süre)", anchor=NW)
graph_canvas.create_line(7, height // 2 - 15, width // 2 - 10, height // 2 - 15, width=2, arrow=LAST)

graph_canvas.create_text(21, 3, font=f"Arial 8 italic", text="y (bulunan kare sayısı)", anchor=NW)
graph_canvas.create_line(15, 5, 15, height // 2 - 7, width=2, arrow=FIRST)

samurai_sudoku = SamuraiSudoku(sudoku_canvas, graph_canvas, "sudoku.txt")

common_img = PhotoImage(width=1, height=1)

Button(root, text="5 Thread İle Çöz", width=140, height=25, image=common_img, compound='c',
       bg="#C0C0C0", activebackground="#D8D8D8", font=("Arial", 11), borderwidth=0,
       cursor="hand2", bd=0, relief="sunken", command=samurai_sudoku.solve).place(x=width // 2 - 20,
                                                                                  y=20 + 3 * height // 4)

Button(root, text="10 Thread İle Çöz", width=140, height=25, image=common_img, compound='c',
       bg="#C0C0C0", activebackground="#D8D8D8", font=("Arial", 11), borderwidth=0,
       cursor="hand2", bd=0, relief="sunken", command=lambda: samurai_sudoku.solve(True)).place(x=width // 2 + 130,
                                                                                                y=20 + 3 * height // 4)

Button(root, text="Sıfırla", width=110, height=25, image=common_img, compound='c', bg="#C0C0C0",
       activebackground="#D8D8D8", font=("Arial", 11), borderwidth=0, cursor="hand2", bd=0, relief="sunken",
       command=samurai_sudoku.load_sudoku).place(x=width - 135, y=20 + 3 * height // 4)

root.mainloop()

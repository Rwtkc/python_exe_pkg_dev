import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

NUM_PATTERN = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


class TxtCurveViewer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("TXT Preview & Curve Plot")
        self.geometry("920x620")
        self.minsize(860, 560)

        top_frame = ttk.Frame(self, padding=12)
        top_frame.pack(fill=tk.X)

        self.file_var = tk.StringVar(value="No file selected")
        ttk.Button(top_frame, text="Select TXT", command=self.select_file).pack(side=tk.LEFT)
        ttk.Label(top_frame, textvariable=self.file_var).pack(side=tk.LEFT, padx=12)

        middle_frame = ttk.Frame(self, padding=(12, 0, 12, 12))
        middle_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(middle_frame, text="First 5 Lines")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.preview = tk.Text(left_frame, height=12, wrap="none", font=("Consolas", 10))
        self.preview.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        right_frame = ttk.LabelFrame(middle_frame, text="Curve")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("No data loaded")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True, linestyle="--", alpha=0.35)

        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select TXT File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not file_path:
            return

        try:
            self.load_and_render(Path(file_path))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", f"Failed to read file:\n{exc}")

    def load_and_render(self, path: Path) -> None:
        lines = path.read_text(encoding="utf-8").splitlines()
        self.file_var.set(str(path))
        self.show_first_five_lines(lines)

        x_values, y_values = self.parse_numeric_data(lines)
        if not y_values:
            self.ax.clear()
            self.ax.set_title("No numeric data found")
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")
            self.ax.grid(True, linestyle="--", alpha=0.35)
            self.canvas.draw_idle()
            return

        self.ax.clear()
        self.ax.plot(x_values, y_values, marker="o", linewidth=1.6)
        self.ax.set_title(f"Curve from {path.name}")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True, linestyle="--", alpha=0.35)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def show_first_five_lines(self, lines: list[str]) -> None:
        self.preview.delete("1.0", tk.END)
        first_lines = lines[:5]
        if not first_lines:
            self.preview.insert(tk.END, "(empty file)")
            return

        for idx, line in enumerate(first_lines, start=1):
            self.preview.insert(tk.END, f"{idx:02d}: {line}\n")

    @staticmethod
    def parse_numeric_data(lines: list[str]) -> tuple[list[float], list[float]]:
        x_values: list[float] = []
        y_values: list[float] = []
        single_col_index = 1

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            numbers = [float(num) for num in NUM_PATTERN.findall(stripped)]
            if len(numbers) >= 2:
                x_values.append(numbers[0])
                y_values.append(numbers[1])
            elif len(numbers) == 1:
                x_values.append(float(single_col_index))
                y_values.append(numbers[0])
                single_col_index += 1

        return x_values, y_values


if __name__ == "__main__":
    app = TxtCurveViewer()
    app.mainloop()

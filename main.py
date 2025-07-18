#    Nick Mastroni & Rafael Castro               #
#             Date: 7-14-25                      #
#   Github: nick-mastroni-1718 , slacke101       #
# Natural Gas Withdrawals and Production in Texas #

# Imports #
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import numpy as np

# API Setup #
API_key = "{Enter API Key Here}"
API_url = (
    "https://api.eia.gov/v2/natural-gas/prod/sum/data/?frequency=monthly"
    "&data[0]=value&facets[duoarea][]=STX&sort[0][column]=period"
    "&sort[0][direction]=desc&offset=0&length=5000"
)
headers = {"X-Api-Key": API_key}
response = requests.get(API_url, headers=headers)
response.raise_for_status()
data = response.json()
results = data.get("response", {}).get("data", [])
df = pd.DataFrame(results)

# Clean Data #
df.replace("None", np.nan, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)


# Main App Class #
class MainWindow:
    def __init__(self):
        # Create ttkbootstrap window with vapor theme
        self.root = ttk.Window(themename="vapor")
        self.root.title("Natural Gas Withdrawals and Production in Texas")
        self.root.geometry("1100x650")
        self.root.minsize(900, 600)

        style = ttk.Style()
        print("Active theme:", style.theme_use())  # Should print 'vapor'

        self.mainUI()

    def mainUI(self):
        # Use grid layout for main container
        self.container = ttk.Frame(self.root, padding=10)
        self.container.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing behavior
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Sidebar frame - fixed width, fills vertically
        self.sidebar = ttk.Frame(self.container, width=220, padding=(10, 20))
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)  # Prevent shrinking to contents

        # Sidebar Title
        ttk.Label(
            self.sidebar,
            text="Menu",
            font=("Segoe UI", 18, "bold"),
            bootstyle="info",
        ).pack(pady=(0, 15))

        # Sidebar buttons container (adds consistent spacing)
        self.sidebar_btn_container = ttk.Frame(self.sidebar)
        self.sidebar_btn_container.pack(fill="x", expand=True)

        btn_options = [
            ("Home", self.homeDashboard, "info-outline"),
            ("Bar Chart", self.barchartGraph, "success-outline"),
            ("Line Chart", self.lineGraph, "warning-outline"),
            ("Scatterplots", self.scatterPlots, "warning-outline"),
            ("Histograms", self.histograms, "warning-outline"),
        ]

        for text, cmd, style in btn_options:
            ttk.Button(
                self.sidebar_btn_container,
                text=text,
                command=cmd,
                bootstyle=style,
                width=18,
            ).pack(pady=6)

        ttk.Button(
            self.sidebar,
            text="Quit",
            command=self.root.quit,
            bootstyle="danger",
            width=18,
        ).pack(side="bottom", pady=20)

        # Main content frame - expandable
        self.main_frame = ttk.Frame(self.container, padding=(15, 15))
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Allow main_frame to expand with window resize
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.homeDashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def homeDashboard(self):
        self.clear_main_frame()

        ttk.Label(
            self.main_frame,
            text="Natural Gas Withdrawals and Production in Texas",
            font=("Segoe UI", 26, "bold"),
            bootstyle="primary",
        ).pack(pady=(10, 15), anchor="w")

        ttk.Label(
            self.main_frame,
            text=f"Dataset contains {len(df)} monthly data points for Texas natural gas production and withdrawals.",
            font=("Segoe UI", 14),
            wraplength=800,
            justify="left",
        ).pack(pady=(0, 15), anchor="w")

        project_overview = (
            "This project fetches and visualizes monthly natural gas withdrawal "
            "and production data for Texas from the U.S. Energy Information Administration (EIA) API.\n\n"
            "You can explore different visualizations including bar charts, line charts, scatterplots, "
            "and histograms to analyze trends and patterns in the natural gas industry.\n\n"
            "Use the menu on the left to navigate through available visualizations."
        )

        ttk.Label(
            self.main_frame,
            text=project_overview,
            font=("Segoe UI", 13),
            wraplength=800,
            justify="left",
        ).pack(pady=(0, 20), anchor="w")

    def barchartGraph(self):
        self.clear_main_frame()

        ttk.Label(
            self.main_frame,
            text="Natural Gas Process Types (Count)",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary",
        ).pack(anchor="w", pady=(5, 15))

        counts = df["process"].value_counts().reset_index()
        counts.columns = ["process", "count"]

        fig = Figure(figsize=(9, 5), dpi=100)
        ax = fig.add_subplot(111)
        sns.barplot(data=counts, x="process", y="count", ax=ax)
        ax.set_title("Count of Distinct Values in 'process'")
        ax.set_xlabel("Process")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=40)

        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def lineGraph(self):
        self.clear_main_frame()

        ttk.Label(
            self.main_frame,
            text="(Line chart view coming soon...)",
            font=("Segoe UI", 20, "italic"),
            bootstyle="warning",
        ).pack(pady=50)

    def scatterPlots(self):
        self.clear_main_frame()

        ttk.Label(
            self.main_frame,
            text="(Scatterplots view coming soon...)",
            font=("Segoe UI", 20, "italic"),
            bootstyle="warning",
        ).pack(pady=50)

    def histograms(self):
        self.clear_main_frame()

        ttk.Label(
            self.main_frame,
            text="(Histograms view coming soon...)",
            font=("Segoe UI", 20, "italic"),
            bootstyle="warning",
        ).pack(pady=50)


# Run App #
if __name__ == "__main__":
    app = MainWindow()
    app.root.mainloop()






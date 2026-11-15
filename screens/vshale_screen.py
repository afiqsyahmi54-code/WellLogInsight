# screens/vshale_screen.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.spinner import MDSpinner
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.clock import Clock


import matplotlib.pyplot as plt

from utils.android_file_utils import read_las_file
from utils.calculations import calculate_vshale, detect_reservoir_intervals, gr_cutoff
from utils.plot_utils import create_depth_track
from utils.constants import COLORS


class VshaleScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_figures = []   # ✅ REQUIRED FOR PDF
        self.intervals = []

    def show_loading(self):
        self.ids.loading_spinner.active = True
        self.ids.loading_label.opacity = 1

    def hide_loading(self):
        self.ids.loading_spinner.active = False
        self.ids.loading_label.opacity = 0

    def on_enter(self):
        app = MDApp.get_running_app()

        try:
            well = app.root.get_screen("welllog")
            self.ids.info_label.text = (
                f"Well Name: {well.ids.well_name.text or '-'}\n"
                f"Location: {well.ids.location.text or '-'}\n"
                f"Depth Range: {well.ids.depth_range.text or '-'}"
            )
        except Exception:
            pass

        self.show_loading()
        Clock.schedule_once(
            lambda dt: self._plot_vshale_safe(app.selected_file),
            0.1
        )
    def _plot_vshale_safe(self, file_path):
        try:
            self.plot_vshale(file_path)
        except Exception as e:
            toast(f"Error plotting Vshale: {str(e)}")
        finally:
            self.hide_loading()

    def plot_vshale(self, file_path):
        if not file_path:
            toast("No LAS file selected")
            return

        df = read_las_file(file_path)
        if df is None:
            return

        # ========= CLEAR OLD =========
        box = self.ids.box_area
        box.clear_widgets()

        for fig in self.current_figures:
            try:
                plt.close(fig)
            except Exception:
                pass
        self.current_figures = []

        # ========= DEPTH =========
        depth = df["Depth"]
        depth_min = depth.min()
        depth_max = depth.max()
        depth_range = depth_max - depth_min

        pixels_per_meter = 2
        canvas_height = int(depth_range * pixels_per_meter)
        canvas_height = max(800, min(canvas_height, 20000))
        fig_height = max(8, min(canvas_height / 100, 100))

        # ========= GR CUTOFF =========
        cut_off = gr_cutoff(df["Gamma Ray"])
        if cut_off is None:
            toast("No Gamma Ray data")
            return

        # ========= INTERVALS =========
        intervals = detect_reservoir_intervals(depth, df["Gamma Ray"], cut_off)
        self.intervals = intervals

        # ========= VSHALE =========
        vshale, _, _ = calculate_vshale(df["Gamma Ray"])
        # ========= DEPTH TRACK =========
        fig_depth, ax_depth = create_depth_track(
            depth_min, depth_max, fig_height, intervals
        )

         # ========= GR TRACK =========
        fig_gr, ax_gr = plt.subplots(figsize=(3.5, fig_height))

        ax_gr.plot(
            df["Gamma Ray"], depth,
            color=COLORS["gamma_ray"],
            linewidth=1.5,
            label="Gamma Ray"
        )

        ax_gr.axvline(
            cut_off,
            color=COLORS["cutoff_line"],
            linestyle="--",
            linewidth=2,
            label=f"Cut-off: {cut_off:.1f} gAPI"
        )

        for idx, (top, bottom, _, _) in enumerate(intervals):
            ax_gr.axhspan(
                top, bottom,
                color=COLORS["sand"],
                alpha=0.4,
                label="Reservoir" if idx == 0 else ""
            )

        ax_gr.set_ylim(depth_max, depth_min)
        ax_gr.set_xlim(0, 200)
        ax_gr.set_xticks([0, 50, 100, 150, 200])
        ax_gr.set_title("Gamma Ray\n(gAPI)", fontsize=10, fontweight="bold")

        ax_gr.legend(loc="upper right", fontsize=7, framealpha=0.9)


        # ========= VSHALE TRACK =========
        fig_vsh, ax_vsh = plt.subplots(figsize=(3.5, fig_height))

        ax_vsh.plot(
            vshale * 100, depth,
            color=COLORS["vshale"],
            linewidth=1.5,
            label="Vshale (Vsh)"
        )

        for top, bottom, _, _ in intervals:
            ax_vsh.axhspan(top, bottom, color=COLORS["sand"], alpha=0.4)

        # ---- Reservoir-style cut-offs ----
        ax_vsh.axvline(
            50, color="red", linestyle=":",
            linewidth=1, alpha=0.5,
            label="Shale (>50%)"
        )
        ax_vsh.axvline(
            30, color="orange", linestyle=":",
            linewidth=1, alpha=0.5,
            label="Sandy Shale (30–50%)"
        )
        ax_vsh.axvline(
            10, color="green", linestyle=":",
            linewidth=1, alpha=0.5,
            label="Clean Sand (<10%)"
        )

        ax_vsh.set_ylim(depth_max, depth_min)
        ax_vsh.set_xlim(0, 100)
        ax_vsh.set_xticks([0, 20, 40, 60, 80, 100])
        ax_vsh.set_title("Shale Volume\n(%)", fontsize=10, fontweight="bold")

        ax_vsh.legend(loc="upper right", fontsize=7, framealpha=0.9)

        # ========= STORE FIGURES (🔥 THIS FIXES SAVE) =========
        self.current_figures = [
            fig_depth,
            fig_gr,
            fig_vsh
        ]

        # ========= ADD CANVASES =========
        for fig, width in [
            (fig_depth, 0.15),
            (fig_gr, 0.425),
            (fig_vsh, 0.425),
        ]:
            canvas = FigureCanvasKivyAgg(fig)
            canvas.size_hint_y = None
            canvas.height = canvas_height
            canvas.size_hint_x = width
            box.add_widget(canvas)

    def navigate_back(self):
        MDApp.get_running_app().change_screen("interpretation")

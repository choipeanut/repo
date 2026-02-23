"""Interactive 2D visualization for a rope-like PBD chain using tkinter.

Controls:
- Drag any unfixed particle with left mouse button.
- Press r to reset the simulation.
"""

from __future__ import annotations

from pathlib import Path
import sys
import tkinter as tk

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pbd import DistanceConstraint, PBDSimulator, ParticleSystem


class InteractiveChainApp:
    def __init__(self) -> None:
        self.width = 900
        self.height = 600
        self.scale = 120.0
        self.offset_x = 120.0
        self.offset_y = 120.0
        self.dt = 1.0 / 60.0
        self.substeps = 3
        self.radius = 8

        self.root = tk.Tk()
        self.root.title("PBD Interactive Chain")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#10141a")
        self.canvas.pack(fill="both", expand=True)

        self.drag_index: int | None = None
        self.mouse_x = 0.0
        self.mouse_y = 0.0

        self._build_simulator()
        self._bind_events()
        self._tick()

    def _build_simulator(self) -> None:
        n = 18
        spacing = 0.25
        positions = [[i * spacing, 0.0, 0.0] for i in range(n)]
        masses = [0.0] + [1.0] * (n - 1)
        particles = ParticleSystem.from_positions(positions, masses)
        constraints = [DistanceConstraint(i, i + 1, spacing) for i in range(n - 1)]
        self.sim = PBDSimulator(
            particles,
            constraints,
            gravity=(0.0, 12.0, 0.0),
            iterations=20,
        )

    def _bind_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.root.bind("r", self._on_reset)

    def _world_to_screen(self, point: list[float]) -> tuple[float, float]:
        return (
            self.offset_x + point[0] * self.scale,
            self.offset_y + point[1] * self.scale,
        )

    def _screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        return (
            (sx - self.offset_x) / self.scale,
            (sy - self.offset_y) / self.scale,
        )

    def _nearest_particle(self, sx: float, sy: float) -> int | None:
        best = None
        best_dist2 = (self.radius * 2.5) ** 2
        for i, p in enumerate(self.sim.particles.positions):
            if self.sim.particles.inverse_masses[i] == 0.0:
                continue
            px, py = self._world_to_screen(p)
            dx = px - sx
            dy = py - sy
            dist2 = dx * dx + dy * dy
            if dist2 <= best_dist2:
                best_dist2 = dist2
                best = i
        return best

    def _on_mouse_down(self, event) -> None:
        self.mouse_x = float(event.x)
        self.mouse_y = float(event.y)
        self.drag_index = self._nearest_particle(self.mouse_x, self.mouse_y)

    def _on_mouse_move(self, event) -> None:
        self.mouse_x = float(event.x)
        self.mouse_y = float(event.y)

    def _on_mouse_up(self, _event) -> None:
        self.drag_index = None

    def _on_reset(self, _event) -> None:
        self._build_simulator()

    def _apply_drag(self) -> None:
        if self.drag_index is None:
            return
        wx, wy = self._screen_to_world(self.mouse_x, self.mouse_y)
        p = self.sim.particles.positions[self.drag_index]
        p[0] = wx
        p[1] = wy
        p[2] = 0.0
        self.sim.particles.velocities[self.drag_index] = [0.0, 0.0, 0.0]

    def _step(self) -> None:
        for _ in range(self.substeps):
            self.sim.step(self.dt / self.substeps)
            self._apply_drag()

    def _draw(self) -> None:
        self.canvas.delete("all")
        pos = self.sim.particles.positions

        for i in range(len(pos) - 1):
            x1, y1 = self._world_to_screen(pos[i])
            x2, y2 = self._world_to_screen(pos[i + 1])
            self.canvas.create_line(x1, y1, x2, y2, fill="#80d8ff", width=3)

        for i, p in enumerate(pos):
            x, y = self._world_to_screen(p)
            fixed = self.sim.particles.inverse_masses[i] == 0.0
            color = "#ffca28" if fixed else "#f5f5f5"
            if i == self.drag_index:
                color = "#ef5350"
            self.canvas.create_oval(
                x - self.radius,
                y - self.radius,
                x + self.radius,
                y + self.radius,
                fill=color,
                outline="",
            )

        self.canvas.create_text(
            12,
            18,
            anchor="w",
            fill="#cfd8dc",
            text="Drag particle with mouse • r: reset",
            font=("TkDefaultFont", 12),
        )

    def _tick(self) -> None:
        self._step()
        self._draw()
        self.root.after(int(self.dt * 1000), self._tick)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    InteractiveChainApp().run()

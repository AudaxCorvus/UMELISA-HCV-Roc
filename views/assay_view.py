import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AssayView:
    """Vista principal para mostrar la placa y los resultados del ensayo."""

    def __init__(self, root, assay):
        self.root = root
        self.assay = assay

        # Mapeo de pozo a muestra (para colorear la placa)
        self.well_to_sample = {}
        self._build_well_mapping()

        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Botones de navegación
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Área de contenido dinámico
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Mostrar validación inicial
        self._check_validation()

    def _build_well_mapping(self):
        """Construye un diccionario well_id -> (sample_index, is_first) para acceso rápido."""
        for idx, sample in enumerate(self.assay.samples):
            if "well1" in sample and sample["well1"]:
                self.well_to_sample[sample["well1"]] = (idx, True)
            if "well2" in sample and sample["well2"]:
                self.well_to_sample[sample["well2"]] = (idx, False)

    def refresh_display(self):
        """Refresca la vista actual (útil después de reinterpretar)."""
        # Determinar qué vista está mostrando y volver a dibujar
        # Por simplicidad, mostramos la placa de nuevo.
        self.show_plate()

    # ============================================================
    #   VISTA DE PLACA COMPLETA
    # ============================================================

    def show_plate(self):
        self._clear_content()
        ttk.Label(self.content_frame, text=f"Vista de Placa - Valid: {self.assay.valid}", font=("Arial", 12, "bold")).pack(pady=10)

        # Frame con scroll para la cuadrícula (por si la pantalla es pequeña)
        canvas_container = tk.Frame(self.content_frame)
        canvas_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_container)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        rows = "ABCDEFGH"
        cols = range(1, 13)

        # Colores especiales de controles
        control_colors = {
            "A1": "#FEFEC1",
            "B1": "#FEFEC1",
            "C1": "#84E0F9",
            "D1": "#84E0F9",
            "E1": "#997070",
            "F1": "#997070"
        }

        # ============================
        #   ENCABEZADOS DE COLUMNAS
        # ============================
        for j, col in enumerate(cols):
            lbl = tk.Label(
                scrollable_frame,
                text=str(col),
                bg="#d0d0d0",
                relief="solid",
                bd=1,
                width=8,
                height=2,
                font=("Arial", 10, "bold")
            )
            lbl.grid(row=0, column=j+1, padx=1, pady=1, sticky="nsew")

        # ============================
        #   FILAS + POZOS
        # ============================
        for i, row in enumerate(rows):
            # Etiqueta de fila
            lbl_row = tk.Label(
                scrollable_frame,
                text=row,
                bg="#d0d0d0",
                relief="solid",
                bd=1,
                width=4,
                height=2,
                font=("Arial", 10, "bold")
            )
            lbl_row.grid(row=i+1, column=0, padx=1, pady=1, sticky="nsew")

            # Pozos
            for j, col in enumerate(cols):
                well_id = f"{row}{col}"
                value = self.assay.plate.get_well_value(well_id)

                # Determinar si es control
                if well_id in control_colors:
                    bg_color = control_colors[well_id]
                else:
                    # Buscar resultado usando el mapeo
                    sample_info = self.well_to_sample.get(well_id)
                    if sample_info:
                        sample_idx, is_first = sample_info
                        result = self.assay.samples[sample_idx]["result"]
                    else:
                        result = None

                    bg_color = self._color_for_result(result, value)

                lbl = tk.Label(
                    scrollable_frame,
                    text=f"{value:.1f}",
                    bg=bg_color,
                    relief="solid",
                    bd=1,
                    width=8,
                    height=3,
                    font=("Arial", 9)
                )
                lbl.grid(row=i+1, column=j+1, padx=1, pady=1, sticky="nsew")

        # Expansión dinámica
        for i in range(9):
            scrollable_frame.rowconfigure(i, weight=1)
        for j in range(13):
            scrollable_frame.columnconfigure(j, weight=1)

    # ============================================================
    #   VISTA DE TABLA DE RESULTADOS
    # ============================================================

    def show_results_table(self, cut_factor):
        self._clear_content()

        ttk.Label(self.content_frame, text="Resultados del Ensayo", font=("Arial", 14, "bold")).pack(pady=10)

        # ============================
        #   PANEL SUPERIOR (CONTROLES)
        # ============================
        panel = tk.Frame(self.content_frame, bg="#f0f0f0")
        panel.pack(fill="x", padx=10, pady=10)

        c = self.assay.controls
        cutoff = self.assay._cutoff(cut_factor)
        bl = self.assay._cutoff(cut_factor * 0.85)  # -15% del cutoff para zona gris

        # --- BLOQUE BLANCO ---
        frame_blanco = tk.LabelFrame(panel, text="Blanco", font=("Arial", 10, "bold"))
        frame_blanco.pack(side="left", padx=10)

        tk.Label(frame_blanco, text=f"B1: {c['B1']:.2f}").pack(anchor="w")
        tk.Label(frame_blanco, text=f"B2: {c['B2']:.2f}").pack(anchor="w")
        tk.Label(frame_blanco, text=f"BB: {c['BB']:.2f}").pack(anchor="w")

        # --- CONTROL POSITIVO ---
        frame_pos = tk.LabelFrame(panel, text="Control positivo", font=("Arial", 10, "bold"))
        frame_pos.pack(side="left", padx=10)

        tk.Label(frame_pos, text=f"P1: {c['P1']:.2f}").pack(anchor="w")
        tk.Label(frame_pos, text=f"P2: {c['P2']:.2f}").pack(anchor="w")
        tk.Label(frame_pos, text=f"P:  {c['PP']:.2f}").pack(anchor="w")

        # --- CONTROL NEGATIVO ---
        frame_neg = tk.LabelFrame(panel, text="Control negativo", font=("Arial", 10, "bold"))
        frame_neg.pack(side="left", padx=10)

        tk.Label(frame_neg, text=f"N1: {c['N1']:.2f}").pack(anchor="w")
        tk.Label(frame_neg, text=f"N2: {c['N2']:.2f}").pack(anchor="w")
        tk.Label(frame_neg, text=f"NN: {c['NN']:.2f}").pack(anchor="w")

        # --- RELACIÓN ---
        frame_rel = tk.LabelFrame(panel, text="Relac. (NN-BB)/(P-BB)", font=("Arial", 10, "bold"))
        frame_rel.pack(side="left", padx=10)

        tk.Label(frame_rel, text=f"{c['RELAC']:.2f}").pack(anchor="w")

        # --- NIVEL DE CORTE ---
        frame_cut = tk.LabelFrame(panel, text="Nivel de Corte", font=("Arial", 10, "bold"))
        frame_cut.pack(side="left", padx=10)

        tk.Label(frame_cut, text=f"{cutoff:.2f}").pack(anchor="w")

        # --- BL ---
        frame_bl = tk.LabelFrame(panel, text="BL", font=("Arial", 10, "bold"))
        frame_bl.pack(side="left", padx=10)

        tk.Label(frame_bl, text=f"{bl:.2f}").pack(anchor="w")

        # --- FORMULA CALC ---
        frame_formula = tk.LabelFrame(panel, text="CALC", font=("Arial", 10, "bold"))
        frame_formula.pack(side="left", padx=10)

        tk.Label(frame_formula, text="(Fi - BB) / (P - BB)").pack(anchor="w")

        # Frame para la tabla con scroll
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Tabla
        columns = ("No", "F1", "CALC1", "F2", "CALC2", "Resultado")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                            yscrollcommand=tree_scroll_y.set,
                            xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Estilos de colores
        tree.tag_configure("neg", background="#FFFFFF")   # blanco
        tree.tag_configure("bl",  background="#CCFFCC")   # verde
        tree.tag_configure("pos", background="#FFCCCC")   # rojo
        tree.tag_configure("rep", background="#ABB4FB")   # gris

        for index, sample in enumerate(self.assay.samples):
            result = sample["result"]

            if result == "Negativo":
                tag = "neg"
            elif result == "Positivo":
                tag = "pos"
            elif result == "BL":
                tag = "bl"
            elif result == "Repetir":
                tag = "rep"
            else:
                tag = ""

            tree.insert("", tk.END, values=(
                f"{index + 1}",
                f"{sample['F1']:.2f}",
                f"{sample['CALC1']:.2f}",
                f"{sample['F2']:.2f}",
                f"{sample['CALC2']:.2f}",
                sample["result"]
            ), tags=(tag,))

        tree.pack(fill=tk.BOTH, expand=True)

    # ============================================================
    #   VISTA DE IMAGEN CON VALORES
    # ============================================================

    def show_image(self, cut_factor):
        self._clear_content()
        ttk.Label(self.content_frame, text="Gráfico de Resultados", font=("Arial", 12, "bold")).pack(pady=10)

        # ============================
        #   PREPARAR DATOS
        # ============================
        samples = self.assay.samples

        indices = []
        f1_values = []
        f2_values = []

        for i, s in enumerate(samples):
            # Ignorar muestras vacías (ambos F=0)
            if s["F1"] == 0 and s["F2"] == 0:
                continue

            indices.append(i + 1)  # número de análisis
            f1_values.append(s["F1"])
            f2_values.append(s["F2"])

        if not indices:
            ttk.Label(self.content_frame, text="No hay datos válidos para graficar.").pack()
            return

        # ============================
        #   CALCULAR CORTE
        # ============================
        cutoff = self.assay._cutoff(cut_factor)
        cutoff_low = self.assay._cutoff(cut_factor * 0.85)  # -15%

        # ============================
        #   CREAR FIGURA
        # ============================
        fig, ax = plt.subplots(figsize=(9, 4), dpi=100)

        # Zona gris
        ax.axhspan(cutoff_low, cutoff, color="#E0E0E0", alpha=0.5, label="Zona gris")

        # Líneas de corte
        ax.axhline(cutoff, color="red", linestyle="--", linewidth=1.5, label="Corte")
        ax.axhline(cutoff_low, color="orange", linestyle="--", linewidth=1.5, label="Corte -15%")

        # ============================
        #   GRAFICAR F1 Y F2
        # ============================
        ax.scatter(indices, f1_values, color="blue", s=60, label="F1")
        ax.scatter(indices, f2_values, color="green", s=60, label="F2")

        # Etiquetas
        ax.set_title("Fluorescencia por muestra")
        ax.set_xlabel("Número de análisis")
        ax.set_ylabel("Fluorescencia")

        ax.set_xticks(indices)
        ax.grid(True, linestyle="--", alpha=0.4)

        ax.legend()

        # ============================
        #   MOSTRAR EN TKINTER
        # ============================
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Asegurar que la figura se cierre cuando se destruya el canvas
        def _on_destroy(event):
            plt.close(fig)
        canvas.get_tk_widget().bind("<Destroy>", _on_destroy)

    # ============================================================
    #   VALIDACIÓN DE PLACA
    # ============================================================

    def _check_validation(self):
        if not self.assay.valid:
            messagebox.showwarning("Validación", "La placa NO es válida según criterios SUMA.")

    # ============================================================
    #   UTILIDADES
    # ============================================================

    def _clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _color_for_result(self, result, value):
        """
        Devuelve el color de fondo según el resultado.
        - result: texto ("Negativo", "Positivo", "Borderline", "Repetir")
        - value: valor numérico del pozo
        """
        if value == 0:
            return "#D0D0D0"  # gris para pozos vacíos

        if result is None:
            # Si no es muestra (controles) o no interpretado, usar blanco por defecto
            return "#FFFFFF"

        if result == "Negativo":
            return "#FFFFFF"  # blanco
        if result == "BL":
            return "#CCFFCC"  # verde
        if result == "Positivo":
            return "#FFCCCC"  # rojo
        if result == "Repetir":
            return "#ADD8E6"  # azul claro

        return "#FFFFFF"
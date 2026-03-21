import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
import logging

from views import AssayView
from controllers import ROCController
from controllers import AssayController

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainApplication:  # Nombre corregido (antes MainApplications)
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("UMELISA HCV")
        self.app.configure(bg="#f0f0f0")
        self.app.geometry("1000x700")
        self.app.minsize(800, 600)

        # Guardar último directorio usado para mejorar experiencia de usuario
        self.last_directory = os.getcwd()

        # Crear ROC Controller
        self.roc_controller = ROCController()

        # Controlador principal
        self.controller = AssayController()
        self.assay_view = None

        self.create_widgets()
        self.create_menu()

        self.app.mainloop()

    def create_widgets(self):
        # ===== HEADER =====
        header_frame = tk.Frame(self.app, bg="#1e88e5", padx=10, pady=10)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="UMELISA HCV",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1e88e5"
        )
        header_label.pack()

        # ===== MAIN CONTENT =====
        self.content_frame = tk.Frame(self.app, bg="#f0f0f0", padx=20, pady=20)
        self.content_frame.pack(fill="both", expand=True)

        self.default_label = ttk.Label(
            self.content_frame,
            text="Bienvenido a UMELISA HCV",
            font=("Arial", 16)
        )
        self.default_label.pack(pady=20)

    def create_menu(self):
        menubar = tk.Menu(self.app)

        # ===== ARCHIVO =====
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir placa…", command=self.open_plate)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.app.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # ===== PROCESAMIENTO =====
        process_menu = tk.Menu(menubar, tearoff=0)
        process_menu.add_command(label="Interpretar con cutoff actual", command=self.reinterpret_assay)
        process_menu.add_command(label="Interpretar con cutoff manual…", command=self.interpret_with_manual_cutoff)
        menubar.add_cascade(label="Procesamiento", menu=process_menu)

        # ===== VISUALIZACIÓN =====
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Ver placa completa", command=self.show_plate)
        view_menu.add_command(label="Ver tabla de resultados", command=self.show_results)
        view_menu.add_command(label="Ver imagen valores", command=self.show_image)
        menubar.add_cascade(label="Visualización", menu=view_menu)

        # ===== ROC =====
        roc_menu = tk.Menu(menubar, tearoff=0)
        roc_menu.add_command(label="Actualizar ROC", command=self.use_for_training)
        roc_menu.add_command(label="Ver información del ROC", command=self.show_roc_info)
        roc_menu.add_separator()
        roc_menu.add_command(label="Cargar varios archivos", command=self.load_a_lot_rocs)  # typo corregido
        roc_menu.add_separator()
        roc_menu.add_command(label="Limpiar registro ROC", command=self.delete_roc_data)   # typo corregido
        menubar.add_cascade(label="ROC", menu=roc_menu)

        self.app.config(menu=menubar)

    # ============================================================
    #   ACCIONES DE MENÚ
    # ============================================================

    def open_plate(self):
        filepath = filedialog.askopenfilename(
            title="Abrir archivo de placa",
            initialdir=self.last_directory,  # recordar último directorio
            filetypes=[("Fluorescencia", "*.flu"), ("Todos los archivos", "*.*")]
        )
        if filepath:
            self.last_directory = os.path.dirname(filepath)  # actualizar
            try:
                # El controller carga el archivo y crea el PlateModel
                plate = self.controller.load_flu_file(filepath)
                assay = self.controller.new_assay(plate)

                # Interpretar con cutoff actual
                self._interpret_assay()
                self._init_assay_view(assay)

                messagebox.showinfo("Placa cargada", "Placa cargada correctamente")
            except (IOError, ValueError) as e:  # Excepciones específicas
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
            except Exception as e:
                logging.exception("Error inesperado en open_plate")
                messagebox.showerror("Error inesperado", f"Contacte al soporte. Detalle: {str(e)}")

    def _interpret_assay(self):
        """Interpreta el ensayo actual con el factor de corte del ROC."""
        try:
            self.controller.interpret_assay(self.roc_controller.cut_factor)
            logging.info(f"Ensayo interpretado con cut factor {self.roc_controller.cut_factor:.3f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reinterpret_assay(self):
        """Reinterpreta el ensayo actual (útil después de actualizar ROC)."""
        if not self.controller.current_assay:
            messagebox.showwarning("Sin ensayo", "No hay ningún ensayo cargado.")
            return
        self._interpret_assay()
        # Actualizar vista si existe
        if self.assay_view:
            self.assay_view.refresh_display()  # nuevo método que refresca la vista actual
        messagebox.showinfo("Reinterpretación", f"Ensayo reinterpretado con cutoff {self.roc_controller.cut_factor:.3f}")

    def interpret_with_manual_cutoff(self):
        """Permite al usuario introducir un cutoff manual y reinterpretar."""
        if not self.controller.current_assay:
            messagebox.showwarning("Sin ensayo", "No hay ningún ensayo cargado.")
            return
        try:
            cut = simpledialog.askfloat("Cutoff manual", "Introduzca el factor de corte (ej. 0.3):",
                                        minvalue=0.0, maxvalue=1.0)
            if cut is not None:
                self.controller.interpret_assay(cut)
                if self.assay_view:
                    self.assay_view.refresh_display()
                messagebox.showinfo("Reinterpretación", f"Ensayo reinterpretado con cutoff {cut:.3f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_plate(self):
        if self.assay_view:
            self.assay_view.show_plate()
        else:
            messagebox.showwarning("Sin vista", "No hay ninguna placa cargada.")

    def show_results(self):
        if self.assay_view:
            self.assay_view.show_results_table(self.roc_controller.cut_factor)
        else:
            messagebox.showwarning("Sin vista", "No hay ninguna placa cargada.")

    def show_image(self):
        if self.assay_view:
            self.assay_view.show_image(self.roc_controller.cut_factor)
        else:
            messagebox.showwarning("Sin vista", "No hay ninguna placa cargada.")

    def use_for_training(self):
        if not self.controller.current_assay:
            messagebox.showwarning("ROC", "No hay ensayo cargado.")
            return
        # Permitir agregar aunque no sea válido, pero con advertencia
        if not self.controller.current_assay.valid:
            respuesta = messagebox.askyesno(
                "Ensayo no válido",
                "El ensayo no es válido según criterios SUMA. ¿Desea agregarlo de todos modos al entrenamiento?"
            )
            if not respuesta:
                return
        try:
            self.roc_controller.add_assay(self.controller.current_assay)
            messagebox.showinfo(
                "ROC",
                f"Datos agregados. Nuevo cutoff: {self.roc_controller.cut_factor:.3f}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_roc_info(self):
        cut = self.roc_controller.cut_factor
        total = len(self.roc_controller.calc_values)
        auc = self.roc_controller.auc if hasattr(self.roc_controller, 'auc') else None
        msg = f"Cutoff actual: {cut:.3f}\nMuestras en dataset: {total}"
        if auc is not None:
            msg += f"\nAUC: {auc:.3f}"
        messagebox.showinfo("Información del ROC", msg)

    def load_a_lot_rocs(self):
        """Carga múltiples archivos .flu de una carpeta en un hilo separado para no bloquear la GUI."""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos .flu",
            initialdir=self.last_directory
        )
        if not folder:
            return
        self.last_directory = folder

        files = [f for f in os.listdir(folder) if f.lower().endswith(".flu")]
        if not files:
            messagebox.showerror("Error", "No se encontraron archivos .flu en la carpeta.")
            return

        # Ventana de progreso
        progress_win = tk.Toplevel(self.app)
        progress_win.title("Cargando placas")
        tk.Label(progress_win, text="Procesando archivos...").pack(padx=20, pady=10)
        progress_bar = ttk.Progressbar(progress_win, mode='indeterminate')
        progress_bar.pack(padx=20, pady=10, fill='x')
        progress_bar.start()

        def task():
            count = 0
            errors = []
            for file in files:
                try:
                    temp_controller = AssayController()
                    plate = temp_controller.load_flu_file(os.path.join(folder, file))
                    assay = temp_controller.new_assay(plate)
                    # Si no es válido, preguntar? Mejor omitir y registrar.
                    if assay.valid:
                        self.roc_controller.add_assay(assay)
                        count += 1
                    else:
                        errors.append(f"{file} (no válido)")
                except Exception as e:
                    errors.append(f"{file} ({str(e)})")
            # Actualizar GUI en el hilo principal
            self.app.after(0, self._finish_load_rocs, count, errors, progress_win)

        threading.Thread(target=task, daemon=True).start()

    def _finish_load_rocs(self, count, errors, progress_win):
        progress_win.destroy()
        msg = f"Se cargaron {count} placas correctamente.\n"
        if errors:
            msg += "Errores:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                msg += f"\n... y {len(errors)-5} más."
        messagebox.showinfo("Carga masiva", msg)
        # Actualizar información del ROC
        self.roc_controller.train()  # reentrenar después de agregar lotes

    def delete_roc_data(self):
        filepath = os.path.join("data", "roc_data.json")
        if not os.path.exists(filepath):
            messagebox.showwarning("ROC", "No existe el archivo roc_data.json en la carpeta data.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el archivo de ROC y el factor de corte actual {self.roc_controller.cut_factor:.3f}?"
        )
        if respuesta:
            try:
                os.remove(filepath)
                # Reiniciar ROCController
                self.roc_controller = ROCController()
                messagebox.showinfo("ROC", "Archivo ROC eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el archivo: {str(e)}")
        else:
            messagebox.showinfo("ROC", "Operación cancelada.")
    # ============================================================
    #   INICIALIZAR VISTA DE ENSAYO
    # ============================================================

    def _init_assay_view(self, assay):
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Crear nueva vista
        self.assay_view = AssayView(self.content_frame, assay)
        self.assay_view.show_plate()

if __name__ == "__main__":
    app = MainApplication()
from models import AssayModel
from models.plate_model import PlateModel

class AssayController:
    """Control principal para manejar el estado del ensayo."""

    def __init__(self):
        """Inicializa el control del ensayo con un estado vacío."""
        self.current_assay = None

    # ============================================================
    #   CARGA DE PLACA DESDE ARCHIVO
    # ============================================================

    def load_flu_file(self, filepath: str):
        """
        Carga datos desde un archivo .flu y crea un PlateModel.
        - Si el archivo tiene menos de 96 valores, completa con 0.0.
        - Si tiene más de 96, muestra una advertencia (en logs) y trunca.
        - Si los decimales usan coma, los convierte a punto.
        """
        rows = "ABCDEFGH"
        cols = range(1, 13)

        current_plate = PlateModel(plate_name=filepath)

        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        # Validar que haya al menos 6 líneas (controles mínimos)
        if len(lines) < 6:
            raise ValueError("El archivo debe contener al menos 6 valores para los controles.")

        # Normalizar valores: reemplazar coma por punto
        normalized = []
        for line in lines:
            clean = line.replace(",", ".")
            try:
                value = float(clean)
            except ValueError:
                value = 0.0  # si hay error, asigna 0.0
            normalized.append(value)

        # Si hay más de 96 valores, truncar y advertir
        if len(normalized) > 96:
            import logging
            logging.warning(f"El archivo {filepath} tiene más de 96 valores. Se tomarán los primeros 96.")
            normalized = normalized[:96]

        # Completar hasta 96 valores si es necesario
        while len(normalized) < 96:
            normalized.append(0.0)

        # Asignar a pozos
        index = 0
        for c in cols:
            for r in rows:
                well_id = f"{r}{c}"
                current_plate.set_well_value(well_id, normalized[index])
                index += 1

        return current_plate

    # ============================================================
    #   CREACIÓN DE ENSAYO
    # ============================================================

    def new_assay(self, plate):
        """
        Crea un nuevo modelo de ensayo a partir de una placa ya cargada.
        Args:
            plate (PlateModel): placa con datos ya leídos.
        """
        if plate.is_empty():
            raise ValueError("La placa está vacía. No se puede crear el ensayo.")
        self.current_assay = AssayModel(plate)
        return self.current_assay

    # ============================================================
    #   INTERPRETACIÓN
    # ============================================================

    def interpret_assay(self, cut_factor):
        """
        Interpreta el ensayo actual usando un factor de cutoff.
        Args:
            cut_factor (float): parámetro base (ej. 0.3 UMELISA o ROC).
        Returns:
            list: resultados de las muestras interpretadas.
        """
        if not self.current_assay:
            raise ValueError("No hay un ensayo cargado. Cree un nuevo ensayo antes de interpretarlo.")

        self.current_assay.interpret(cut_factor)
        return self.current_assay.samples

    # ============================================================
    #   RESUMEN DE RESULTADOS
    # ============================================================

    def get_summary(self):
        """
        Devuelve un resumen con controles, validación y resultados.
        Returns:
            dict: resumen del ensayo.
        """
        if not self.current_assay:
            raise ValueError("No hay ensayo disponible para resumir.")

        return {
            "plate": self.current_assay.plate.plate_name,
            "controls": self.current_assay.controls,
            "valid": self.current_assay.valid,
            "samples": self.current_assay.samples
        }
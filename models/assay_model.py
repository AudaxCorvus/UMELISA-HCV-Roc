from models.plate_model import PlateModel

class AssayModel:
    """
    Representa un ensayo UMELISA HCV completo.
    Contiene:
        - La placa cruda (PlateModel)
        - Controles (BB, NN, PP, RELAC)
        - Muestras (pares de pozos)
        - Valores calculados (CALC, resultados)
    """

    # Umbrales para validación (podrían moverse a un archivo de configuración)
    VALIDATION_THRESHOLDS = {
        'B_MAX': 10.0,           # Blanco máximo (ejemplo)
        'N_MIN': 0.0,             # Mínimo para negativo (depende del contexto)
        'P_MIN': 60.0,
        'P_MAX': 180.0,
        'RELAC_MAX': 0.1
    }

    def __init__(self, plate: PlateModel):
        if plate.is_empty():
            raise ValueError("La placa está vacía. Por favor, cargue datos antes de crear el modelo de ensayo.")

        self.plate = plate

        # Controles individuales y combinados
        self.controls = {
            "B1": None, "B2": None,
            "N1": None, "N2": None,
            "P1": None, "P2": None,
            "BB": None, "NN": None,
            "PP": None, "RELAC": None
        }

        # Lista de muestras (pares de pozos)
        self.samples = []

        # Estado de validación
        self.valid = True

        # Ejecuta el proceso completo del ensayo al inicializar
        self._process()

    # ============================================================
    #   PROCESO COMPLETO DEL ENSAYO
    # ============================================================

    def _process(self):
        self._extract_controls()
        self._pair_samples()
        self._compute_calc()
        self._validate()
        self._check_duplicate_consistency()

    # ============================================================
    #   EXTRACCIÓN DE CONTROLES
    # ============================================================

    def _extract_controls(self):
        """Extrae los controles desde posiciones estándar de la placa."""
        self.controls["B1"] = self.plate.get_well_value("A1")
        self.controls["B2"] = self.plate.get_well_value("B1")

        self.controls["P1"] = self.plate.get_well_value("C1")
        self.controls["P2"] = self.plate.get_well_value("D1")

        self.controls["N1"] = self.plate.get_well_value("E1")
        self.controls["N2"] = self.plate.get_well_value("F1")

        # Controles combinados
        self.controls["BB"] = (self.controls["B1"] + self.controls["B2"]) / 2
        self.controls["NN"] = (self.controls["N1"] + self.controls["N2"]) / 2

        # PP = menor de los dos positivos
        self.controls["PP"] = min(self.controls["P1"], self.controls["P2"])

        # Relación NN-BB / PP-BB
        if self.controls["PP"] != self.controls["BB"]:
            self.controls["RELAC"] = (
                (self.controls["NN"] - self.controls["BB"]) / (self.controls["PP"] - self.controls["BB"])
            )
        else:
            self.controls["RELAC"] = 0.0  # Evitar división por cero

    # ============================================================
    #   AGRUPACIÓN DE MUESTRAS
    # ============================================================

    def _pair_samples(self):
        """
        Agrupa pozos en pares consecutivos (duplicados).
        Se asume que después de los 6 controles vienen las muestras por pares.
        Si el número de pozos restantes es impar, se ignora el último.
        """
        wells = list(self.plate.get_all_wells())
        # Saltar los primeros 6 pozos (controles)
        wells = wells[6:]

        # Asegurar que la cantidad de pozos sea par; si no, descartar el último
        if len(wells) % 2 != 0:
            wells = wells[:-1]  # Descartar el último (puede ser un pozo vacío)

        self.samples = []
        for i in range(0, len(wells), 2):
            well_id1, val1 = wells[i]
            well_id2, val2 = wells[i+1]
            self.samples.append({
                "well1": well_id1,          # Guardar ID del pozo para mapeo en vista
                "well2": well_id2,
                "F1": val1,
                "F2": val2,
                "CALC1": None,
                "CALC2": None,
                "result": None
            })

    # ============================================================
    #   CÁLCULO CALC
    # ============================================================

    def _compute_calc(self):
        """Calcula CALC para cada muestra usando los controles BB y PP."""
        BB = self.controls["BB"]
        PP = self.controls["PP"]

        if PP == BB:
            # Si PP == BB, no se puede calcular CALC; se asigna 0.0 y se marca como no válido para ROC
            for sample in self.samples:
                sample["CALC1"] = 0.0
                sample["CALC2"] = 0.0
            return

        for sample in self.samples:
            F1 = sample["F1"]
            F2 = sample["F2"]

            # Se permite CALC=0 si F <= BB
            sample["CALC1"] = (F1 - BB) / (PP - BB) if F1 > BB else 0.0
            sample["CALC2"] = (F2 - BB) / (PP - BB) if F2 > BB else 0.0

    # ============================================================
    #   INTERPRETACIÓN (cutoff como parámetro)
    # ============================================================

    def interpret(self, cut_factor: float, gray_zone_factor: float = 0.85):
        """
        Interpreta cada muestra usando un factor externo (ej. 0.3 UMELISA o ROC).
        Parámetros:
            cut_factor: factor base para el cutoff.
            gray_zone_factor: porcentaje del cutoff para el límite inferior de la zona gris (por defecto 0.85).
        """
        cutoff = self._cutoff(cut_factor)
        cutoff_under = self._cutoff(cut_factor * gray_zone_factor)  # zona gris

        def clasificar(F):
            if F < cutoff_under:
                return "neg"
            elif F > cutoff:
                return "pos"
            else:
                return "gris"

        for sample in self.samples:
            c1 = clasificar(sample["F1"])
            c2 = clasificar(sample["F2"])

            if c1 == c2:
                if c1 == "neg":
                    sample["result"] = "Negativo"
                elif c1 == "pos":
                    sample["result"] = "Positivo"
                else:
                    sample["result"] = "BL"
            elif {"pos", "neg"} == {c1, c2}:
                sample["result"] = "Repetir"
            else:
                # uno gris y el otro pos/neg → se toma el que no es gris
                sample["result"] = "Positivo" if "pos" in (c1, c2) else "Negativo"

    # ============================================================
    #   VALIDACIÓN SUMA
    # ============================================================

    def _validate(self):
        """Valida la placa según criterios SUMA (parametrizados)."""
        BB = self.controls["BB"]
        PP = self.controls["PP"]
        if BB is None or PP is None:
            self.valid = False
            return

        th = self.VALIDATION_THRESHOLDS

        # Condiciones individuales (se pueden ajustar)
        cond1 = (self.controls['B1'] < th['B_MAX'] and self.controls['B2'] < th['B_MAX'])
        # Condición para negativos: ambos deben estar por debajo de BB + algo? Por ahora la mantenemos como estaba.
        cond2 = (self.controls['N1'] < BB + 10 and self.controls['N2'] < BB + 10)
        # Ambos positivos deben estar en rango (antes se usaba OR, ahora AND)
        cond3 = (th['P_MIN'] < self.controls['P1'] < th['P_MAX']) and (th['P_MIN'] < self.controls['P2'] < th['P_MAX'])
        cond4 = (self.controls['RELAC'] < th['RELAC_MAX'])

        self.valid = cond1 and cond2 and cond3 and cond4

    # ============================================================
    #   CUTOFF CALCULATIONS
    # ============================================================

    def _cutoff(self, cut_factor: float):
        """Calcula el cutoff final a partir del factor base."""
        return cut_factor * (self.controls["PP"] - self.controls["BB"]) + self.controls["BB"]

    # ============================================================
    #   MÉTODO DE AYUDA PARA VISTAS
    # ============================================================

    def get_sample_by_well(self, well_id):
        """
        Devuelve el índice de la muestra (y si es el primer o segundo pozo) al que pertenece un well_id.
        Útil para colorear la placa.
        Retorna (sample_index, is_first) o (None, None) si no es muestra.
        """
        for idx, sample in enumerate(self.samples):
            if sample.get("well1") == well_id:
                return idx, True
            if sample.get("well2") == well_id:
                return idx, False
        return None, None

    # ============================================================
    #   REPRESENTACIÓN
    # ============================================================

    def __repr__(self):
        return f"<AssayModel plate={self.plate.plate_name}>"
    
    def _check_duplicate_consistency(self, max_cv=0.20):
        """
        Verifica la consistencia de los duplicados.
        Si el coeficiente de variación (CV) entre F1 y F2 supera max_cv,
        se marca la muestra como "Repetir" (sobrescribe el resultado anterior).
        """
        for sample in self.samples:
            f1 = sample["F1"]
            f2 = sample["F2"]
            if f1 == 0 and f2 == 0:
                continue
            mean = (f1 + f2) / 2
            if mean == 0:
                continue
            cv = abs(f1 - f2) / mean
            if cv > max_cv:
                sample["result"] = "Repetir"    
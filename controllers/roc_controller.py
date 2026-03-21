import json
import os
import numpy as np
from sklearn.metrics import roc_curve, auc
import logging

class ROCController:

    MAX_SAMPLES = 500  # Aumentado de 100 a 500 para mejor estabilidad
    REFERENCE_CUTOFF = 0.3  # Cutoff fijo para generar etiquetas (evita circularidad)

    def __init__(self, path="data/roc_data.json"):
        self.path = path
        self.cut_factor = 0.3  # Valor por defecto, se actualizará al cargar o entrenar

        self.calc_values = []
        self.labels = []
        self.weights = []
        self.auc = None  # Almacenar AUC

        # Asegurar que el directorio data existe
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        self.load()

    # --------------------------
    # Cargar archivo ROC
    # --------------------------
    def load(self):
        if not os.path.exists(self.path):
            self.save()
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.calc_values = data.get("calc_values", [])
            self.labels = data.get("labels", [])
            self.weights = data.get("weights", [])
            self.cut_factor = data.get("cut_factor", 0.3)
            self.auc = data.get("auc", None)
        except Exception as e:
            logging.error(f"Error al cargar ROC: {e}")
            # Si hay error, iniciar vacío
            self.calc_values = []
            self.labels = []
            self.weights = []
            self.cut_factor = 0.3
            self.auc = None

    # --------------------------
    # Guardar archivo ROC
    # --------------------------
    def save(self):
        data = {
            "cut_factor": self.cut_factor,
            "calc_values": self.calc_values,
            "labels": self.labels,
            "weights": self.weights,
            "auc": self.auc
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # --------------------------
    # Generar labels usando cutoff fijo (0.3) para evitar circularidad
    # --------------------------
    def generate_labels(self, calc_list):
        """
        Genera etiquetas binarias (0/1) basadas en un cutoff fijo de referencia (0.3).
        Si calc > 0.3 + margen -> 1 (positivo)
        Si calc < 0.3 - margen -> 0 (negativo)
        Si está en zona gris, se asigna según el lado en que caiga.
        """
        base = self.REFERENCE_CUTOFF
        gris_width = base * 0.15

        labels = []
        weights = []
        temp_calc = []
        
        for v in calc_list:
            # Caso No. 1
            # Descartando borderlines para simplificar y evitar ambigüedades
            # if v > base:
            #     temp_calc.append(v)
            #     labels.append(1)
            #     weights.append(1.0)
            # elif v < base - gris_width:
            #     temp_calc.append(v)
            #     labels.append(0)
            #     weights.append(1.0)
            
            # Caso No. 2
            # Descartando zona gris para simplificar y evitar ambigüedades
            # if v > base + gris_width:
            #     temp_calc.append(v)
            #     labels.append(1)
            #     weights.append(1.0)
            # elif v < base - gris_width:
            #     temp_calc.append(v)
            #     labels.append(0)
            #     weights.append(1.0)
            
            # Caso No. 3
            # Se toman todos los valores teniendo en cuenta el peso 
            if v > base + gris_width:
                temp_calc.append(v)
                labels.append(1)
                weights.append(1.0)  # Peso máximo
            elif v > base:
                temp_calc.append(v)
                labels.append(1)
                weights.append(0.5)          
            elif v >= base - gris_width:  # 0.255 - 0.3
                temp_calc.append(v)
                labels.append(0)
                weights.append(0.3)                
            else:  # < 0.255
                temp_calc.append(v)
                labels.append(0)
                weights.append(1.0)  
            
            # Caso No. 4
            # Tomando todos lo valores por el Nivel de Corte
            # if v > base:
            #     temp_calc.append(v)
            #     labels.append(1)
            #     weights.append(1.0)
            # elif v < base:
            #     temp_calc.append(v)
            #     labels.append(0)
            #     weights.append(1.0)
                    
        # Opcional: normalizar pesos
        weights = np.array(weights)
        weights = weights * (len(weights) / weights.sum())  # Normalizar a media 1
        
        return  temp_calc, labels, weights

    # --------------------------
    # Agregar datos desde un ASSAY
    # --------------------------
    def add_assay(self, assay, use_for_training=True):
        """
        Recibe un objeto Assay.
        Extrae el promedio de CALC1 y CALC2 de cada muestra, solo si ambos > 0.
        """
        calc_list = []
        for s in assay.samples:
            # Ignorar muestras con resultado Repetir o BL (no clasificables)
            if s["result"] == "Repetir":
                continue
            # Tomar solo si ambos CALC son positivos (evitar ceros problemáticos)
            if s["CALC1"] is not None and s["CALC2"] is not None and s["CALC1"] > 0 and s["CALC2"] > 0:
                calc_list.append((s["CALC1"] + s["CALC2"]) / 2)

        if not use_for_training or not calc_list:
            return "ignored"

        temp_calc, labels, weights = self.generate_labels(calc_list)
        
        self.calc_values.extend(temp_calc)
        self.labels.extend(labels)
        self.weights.extend(weights)
        

        # Limitar número de muestras
        if len(self.calc_values) > self.MAX_SAMPLES:
            # Mantener las últimas MAX_SAMPLES
            self.calc_values = self.calc_values[-self.MAX_SAMPLES:]
            self.labels = self.labels[-self.MAX_SAMPLES:]
            self.weights = self.weights[-self.MAX_SAMPLES:]

        logging.info(f"ROC: ahora {len(self.calc_values)} muestras")

        self.train()  # Reentrenar automáticamente
        self.save()

    # --------------------------
    # Entrenar ROC y actualizar cut_factor
    # --------------------------
    def train(self):
        if len(self.calc_values) < 50:
            return None
        
        try:
            fpr, tpr, thresholds = roc_curve(self.labels, self.calc_values, sample_weight=self.weights)
            # Calcular AUC
            self.auc = auc(fpr, tpr)

            # Filtrar thresholds infinitos o nulos
            valid_indices = np.isfinite(thresholds)
            fpr = fpr[valid_indices]
            tpr = tpr[valid_indices]
            thresholds = thresholds[valid_indices]

            if len(thresholds) == 0:
                logging.warning("No hay thresholds válidos después de filtrar.")
                return None

            youden = tpr - fpr
            idx = youden.argmax()
            new_cut = float(thresholds[idx])

            # Actualizar cut_factor
            self.cut_factor = new_cut
            logging.info(f"Nuevo cutoff ROC: {self.cut_factor:.3f}, AUC: {self.auc:.3f}")
            self.save()
            return new_cut
        except Exception as e:
            logging.error(f"Error entrenando ROC: {e}")
            return None

    # --------------------------
    # Exportar datos a CSV
    # --------------------------
    def export_to_csv(self, filepath):
        """Exporta los valores CALC y etiquetas a un archivo CSV."""
        import csv
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['calc_value', 'label', 'weights'])
            for val, lab, wei in zip(self.calc_values, self.labels, self.weights):
                writer.writerow([val, lab, wei])
        logging.info(f"Datos ROC exportados a {filepath}")
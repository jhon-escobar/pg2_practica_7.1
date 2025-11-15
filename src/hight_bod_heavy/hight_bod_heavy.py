from collections import deque
from datetime import datetime
import statistics
from typing import List, Dict, Optional

class CalculadoraIMC:
    """Clase para calcular y clasificar el Índice de Masa Corporal"""
    
    def __init__(self):
        self.historial_imc = []  # LISTA para historial
        self.cola_imc = deque()  # COLA para procesamiento
    
    @staticmethod
    def calcular(peso_kg: float, altura_m: float) -> float:
        if altura_m <= 0:
            raise ValueError("La altura debe ser mayor a cero")
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a cero")
        return peso_kg / (altura_m ** 2)
    
    @staticmethod
    def clasificar(imc: float) -> str:
        if imc < 16:
            return "Bajo peso (delgadez severa)"
        elif 16 <= imc < 17:
            return "Bajo peso (delgadez moderada)"
        elif 17 <= imc < 18.5:
            return "Bajo peso (delgadez leve)"
        elif 18.5 <= imc < 25:
            return "Peso normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        elif 30 <= imc < 35:
            return "Obesidad grado I"
        elif 35 <= imc < 40:
            return "Obesidad grado II"
        else:
            return "Obesidad grado III"
    
    def agregar_historial(self, peso_kg: float, altura_m: float):
        """Agrega cálculo a la lista de historial"""
        imc = self.calcular(peso_kg, altura_m)
        clasificacion = self.clasificar(imc)
        
        registro = {
            'peso_kg': peso_kg,
            'altura_m': altura_m,
            'imc': imc,
            'clasificacion': clasificacion,
            'fecha': datetime.now()
        }
        
        self.historial_imc.append(registro)
    
    def encolar_calculo(self, peso_kg: float, altura_m: float):
        """Encola cálculo para procesamiento posterior"""
        self.cola_imc.append({
            'peso_kg': peso_kg,
            'altura_m': altura_m
        })
    
    def procesar_cola(self):
        """Procesa todos los cálculos en cola"""
        while self.cola_imc:
            calculo = self.cola_imc.popleft()
            self.agregar_historial(calculo['peso_kg'], calculo['altura_m'])
    
    # NUEVAS FUNCIONES AGREGADAS
    def obtener_estadisticas(self) -> Dict:
        """Calcula estadísticas del historial de IMC"""
        if not self.historial_imc:
            return {}
        
        imcs = [registro['imc'] for registro in self.historial_imc]
        
        return {
            'total_registros': len(self.historial_imc),
            'imc_promedio': statistics.mean(imcs),
            'imc_mediano': statistics.median(imcs),
            'imc_minimo': min(imcs),
            'imc_maximo': max(imcs),
            'desviacion_estandar': statistics.stdev(imcs) if len(imcs) > 1 else 0,
            'clasificacion_mas_comun': statistics.mode([r['clasificacion'] for r in self.historial_imc])
        }
    
    def filtrar_por_clasificacion(self, clasificacion: str) -> List[Dict]:
        """Filtra el historial por clasificación de IMC"""
        return [registro for registro in self.historial_imc 
                if registro['clasificacion'] == clasificacion]
    
    def obtener_evolucion(self) -> List[Dict]:
        """Retorna el historial ordenado por fecha (más reciente primero)"""
        return sorted(self.historial_imc, key=lambda x: x['fecha'], reverse=True)
    
    def limpiar_historial(self, confirmacion: bool = False) -> bool:
        """Limpia todo el historial (requiere confirmación)"""
        if confirmacion and self.historial_imc:
            self.historial_imc.clear()
            return True
        return False
    
    def exportar_historial(self, formato: str = 'lista') -> List[Dict]:
        """Exporta el historial en diferentes formatos"""
        if formato == 'lista':
            return self.historial_imc
        elif formato == 'simplificado':
            return [{'imc': r['imc'], 'clasificacion': r['clasificacion'], 'fecha': r['fecha']} 
                    for r in self.historial_imc]
        else:
            raise ValueError("Formato no válido. Use 'lista' o 'simplificado'")
    
    def peso_ideal_rango(self, altura_m: float) -> Dict[str, float]:
        """Calcula el rango de peso ideal para una altura dada"""
        imc_min_ideal = 18.5
        imc_max_ideal = 24.9
        
        peso_min = imc_min_ideal * (altura_m ** 2)
        peso_max = imc_max_ideal * (altura_m ** 2)
        
        return {
            'peso_min_ideal_kg': peso_min,
            'peso_max_ideal_kg': peso_max,
            'rango_recomendado': f"{peso_min:.1f} - {peso_max:.1f} kg"
        }


class CalculadoraGrasaCorporal:
    """Clase para calcular el porcentaje de grasa corporal"""
    
    def __init__(self):
        self.registros_grasa = []  # LISTA para registros
        self.cola_grasa = deque()  # COLA para cálculos
    
    @staticmethod
    def calcular(imc: float, edad: int, sexo: str) -> float:
        if edad <= 0 or edad > 120:
            raise ValueError("La edad debe estar entre 1 y 120 años")
        if sexo.upper() not in ['M', 'F']:
            raise ValueError("El sexo debe ser 'M' o 'F'")
            
        if sexo.upper() == 'M':
            return (1.20 * imc) + (0.23 * edad) - 16.2
        else:  # 'F'
            return (1.20 * imc) + (0.23 * edad) - 5.4
    
    @staticmethod
    def clasificar_grasa(porcentaje_grasa: float, sexo: str, edad: int) -> str:
        """Clasifica el porcentaje de grasa corporal según sexo y edad"""
        sexo = sexo.upper()
        
        if sexo == 'M':
            if edad < 30:
                if porcentaje_grasa < 8: return "Grasa esencial"
                elif 8 <= porcentaje_grasa < 19: return "Atleta"
                elif 19 <= porcentaje_grasa < 24: return "Fitness"
                elif 24 <= porcentaje_grasa < 26: return "Aceptable"
                else: return "Obeso"
            else:
                if porcentaje_grasa < 11: return "Grasa esencial"
                elif 11 <= porcentaje_grasa < 21: return "Atleta"
                elif 21 <= porcentaje_grasa < 26: return "Fitness"
                elif 26 <= porcentaje_grasa < 28: return "Aceptable"
                else: return "Obeso"
        else:  # 'F'
            if edad < 30:
                if porcentaje_grasa < 14: return "Grasa esencial"
                elif 14 <= porcentaje_grasa < 20: return "Atleta"
                elif 20 <= porcentaje_grasa < 24: return "Fitness"
                elif 24 <= porcentaje_grasa < 29: return "Aceptable"
                else: return "Obeso"
            else:
                if porcentaje_grasa < 16: return "Grasa esencial"
                elif 16 <= porcentaje_grasa < 22: return "Atleta"
                elif 22 <= porcentaje_grasa < 26: return "Fitness"
                elif 26 <= porcentaje_grasa < 31: return "Aceptable"
                else: return "Obeso"
    
    def agregar_registro(self, imc: float, edad: int, sexo: str):
        """Agrega cálculo a la lista de registros"""
        porcentaje_grasa = self.calcular(imc, edad, sexo)
        clasificacion = self.clasificar_grasa(porcentaje_grasa, sexo, edad)
        
        registro = {
            'imc': imc,
            'edad': edad,
            'sexo': sexo,
            'porcentaje_grasa': porcentaje_grasa,
            'clasificacion_grasa': clasificacion,
            'fecha': datetime.now()
        }
        
        self.registros_grasa.append(registro)
    
    def encolar_calculo(self, imc: float, edad: int, sexo: str):
        """Encola cálculo para procesamiento posterior"""
        self.cola_grasa.append({
            'imc': imc,
            'edad': edad,
            'sexo': sexo
        })
    
    def procesar_cola(self):
        """Procesa todos los cálculos en cola"""
        while self.cola_grasa:
            calculo = self.cola_grasa.popleft()
            self.agregar_registro(calculo['imc'], calculo['edad'], calculo['sexo'])
    
    # NUEVAS FUNCIONES AGREGADAS
    def obtener_tendencia_grasa(self) -> Dict:
        """Analiza la tendencia del porcentaje de grasa en el tiempo"""
        if len(self.registros_grasa) < 2:
            return {'tendencia': 'insuficientes_datos', 'mensaje': 'Se necesitan al menos 2 registros'}
        
        registros_ordenados = sorted(self.registros_grasa, key=lambda x: x['fecha'])
        primer_registro = registros_ordenados[0]['porcentaje_grasa']
        ultimo_registro = registros_ordenados[-1]['porcentaje_grasa']
        diferencia = ultimo_registro - primer_registro
        
        if diferencia < -2:
            tendencia = "mejorando"
        elif diferencia > 2:
            tendencia = "empeorando"
        else:
            tendencia = "estable"
        
        return {
            'tendencia': tendencia,
            'cambio_porcentual': diferencia,
            'primer_registro': primer_registro,
            'ultimo_registro': ultimo_registro,
            'total_registros': len(self.registros_grasa)
        }
    
    def filtrar_por_sexo(self, sexo: str) -> List[Dict]:
        """Filtra registros por sexo"""
        return [registro for registro in self.registros_grasa 
                if registro['sexo'].upper() == sexo.upper()]
    
    def obtener_promedio_por_edad(self) -> Dict[int, float]:
        """Calcula el promedio de grasa por grupo de edad"""
        grupos = {}
        for registro in self.registros_grasa:
            grupo_edad = (registro['edad'] // 10) * 10  # Agrupa por década
            if grupo_edad not in grupos:
                grupos[grupo_edad] = []
            grupos[grupo_edad].append(registro['porcentaje_grasa'])
        
        return {edad: statistics.mean(valores) for edad, valores in grupos.items()}
    
    def recomendar_objetivo(self, porcentaje_actual: float, sexo: str, edad: int) -> Dict:
        """Recomienda un objetivo saludable de grasa corporal"""
        clasificacion_actual = self.clasificar_grasa(porcentaje_actual, sexo, edad)
        objetivo = None
        
        if "Obeso" in clasificacion_actual:
            objetivo = porcentaje_actual * 0.85  # Reducir 15%
        elif "Aceptable" in clasificacion_actual:
            objetivo = porcentaje_actual * 0.92  # Reducir 8%
        elif "Fitness" in clasificacion_actual:
            objetivo = porcentaje_actual  # Mantener
        else:
            objetivo = porcentaje_actual  # Ya está en rango excelente
        
        return {
            'clasificacion_actual': clasificacion_actual,
            'porcentaje_actual': porcentaje_actual,
            'objetivo_recomendado': objetivo,
            'reduccion_necesaria': porcentaje_actual - objetivo,
            'mensaje': f"Objetivo recomendado: {objetivo:.1f}%"
        }


class CalculadoraMasaMuscular:
    """Clase para calcular la masa muscular y composición corporal"""
    
    def __init__(self):
        self.composiciones = []  
        self.cola_composiciones = deque()  
    
    @staticmethod
    def calcular(peso_kg: float, porcentaje_grasa: float) -> dict:
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a cero")
        if porcentaje_grasa < 0 or porcentaje_grasa > 100:
            raise ValueError("El porcentaje de grasa debe estar entre 0 y 100")
            
        grasa_kg = (porcentaje_grasa / 100) * peso_kg
        masa_magra_kg = peso_kg - grasa_kg
        porcentaje_muscular = (masa_magra_kg / peso_kg) * 100
        
        return {
            'peso_total_kg': peso_kg,
            'grasa_corporal_kg': grasa_kg,
            'masa_magra_kg': masa_magra_kg,
            'porcentaje_grasa': porcentaje_grasa,
            'porcentaje_muscular': porcentaje_muscular
        }
    
    def agregar_composicion(self, peso_kg: float, porcentaje_grasa: float):
        """Agrega composición a la lista"""
        composicion = self.calcular(peso_kg, porcentaje_grasa)
        composicion['fecha'] = datetime.now()
        
        self.composiciones.append(composicion)
    
    def encolar_analisis(self, peso_kg: float, porcentaje_grasa: float):
        """Encola análisis para procesamiento posterior"""
        self.cola_composiciones.append({
            'peso_kg': peso_kg,
            'porcentaje_grasa': porcentaje_grasa
        })
    
    def procesar_cola(self):
        """Procesa todos los análisis en cola"""
        while self.cola_composiciones:
            analisis = self.cola_composiciones.popleft()
            self.agregar_composicion(analisis['peso_kg'], analisis['porcentaje_grasa'])
    
    # NUEVAS FUNCIONES AGREGADAS
    def calcular_indice_muscular(self) -> float:
        """Calcula un índice de calidad muscular (masa magra / peso total)"""
        if not self.composiciones:
            return 0.0
        
        ultima_composicion = self.composiciones[-1]
        return (ultima_composicion['masa_magra_kg'] / ultima_composicion['peso_total_kg']) * 100
    
    def obtener_progreso_muscular(self) -> Dict:
        """Analiza el progreso de masa muscular en el tiempo"""
        if len(self.composiciones) < 2:
            return {'progreso': 'insuficientes_datos'}
        
        composiciones_ordenadas = sorted(self.composiciones, key=lambda x: x['fecha'])
        masa_inicial = composiciones_ordenadas[0]['masa_magra_kg']
        masa_final = composiciones_ordenadas[-1]['masa_magra_kg']
        cambio = masa_final - masa_inicial
        porcentaje_cambio = (cambio / masa_inicial) * 100
        
        if cambio > 1:
            progreso = "ganancia_significativa"
        elif cambio > 0.1:
            progreso = "ganancia_moderada"
        elif cambio < -1:
            progreso = "perdida_significativa"
        elif cambio < -0.1:
            progreso = "perdida_moderada"
        else:
            progreso = "estable"
        
        return {
            'progreso': progreso,
            'cambio_kg': cambio,
            'porcentaje_cambio': porcentaje_cambio,
            'masa_inicial_kg': masa_inicial,
            'masa_actual_kg': masa_final,
            'periodo_dias': (composiciones_ordenadas[-1]['fecha'] - composiciones_ordenadas[0]['fecha']).days
        }
    
    def recomendar_entrenamiento(self) -> str:
        """Recomienda tipo de entrenamiento basado en composición corporal"""
        if not self.composiciones:
            return "No hay datos suficientes para recomendación"
        
        ultima = self.composiciones[-1]
        porcentaje_muscular = ultima['porcentaje_muscular']
        
        if porcentaje_muscular < 70:
            return "Enfoque en entrenamiento de fuerza y hipertrofia"
        elif 70 <= porcentaje_muscular < 80:
            return "Entrenamiento mixto: fuerza y definición"
        else:
            return "Enfoque en mantenimiento y tonificación"
    
    def predecir_composicion(self, peso_objetivo: float, porcentaje_grasa_objetivo: float) -> Dict:
        """Predice la composición corporal para un peso y porcentaje de grasa objetivo"""
        return self.calcular(peso_objetivo, porcentaje_grasa_objetivo)
    
    def calcular_deficit_calorico(self, peso_objetivo: float, porcentaje_grasa_objetivo: float, 
                                semanas: int = 12) -> Dict:
        """Calcula el déficit calórico necesario para alcanzar objetivos"""
        composicion_actual = self.composiciones[-1] if self.composiciones else None
        if not composicion_actual:
            return {'error': 'No hay composición actual disponible'}
        
        composicion_objetivo = self.predecir_composicion(peso_objetivo, porcentaje_grasa_objetivo)
        
        grasa_a_perder = composicion_actual['grasa_corporal_kg'] - composicion_objetivo['grasa_corporal_kg']
        calorias_totales_deficit = grasa_a_perder * 7700  # 7700 kcal por kg de grasa
        deficit_diario = calorias_totales_deficit / (semanas * 7)
        
        return {
            'grasa_a_perder_kg': grasa_a_perder,
            'deficit_calorico_diario': deficit_diario,
            'semanas_estimadas': semanas,
            'perdida_semanal_kg': grasa_a_perder / semanas,
            'es_saludable': (grasa_a_perder / semanas) <= 1.0  # Máximo 1kg por semana
        }
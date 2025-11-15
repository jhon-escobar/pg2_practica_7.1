from hight_bod_heavy import CalculadoraIMC, CalculadoraGrasaCorporal, CalculadoraMasaMuscular
import time
import sys

def test_calculadora_imc():
    """Pruebas completas para CalculadoraIMC"""
    print("\n" + "="*60)
    print("TEST CALCULADORA IMC")
    print("="*60)
    
    calc = CalculadoraIMC()
    tests_pasados = 0
    total_tests = 0
    
    # Test 1: Cálculo básico
    try:
        imc = calc.calcular(70, 1.75)
        expected = 22.86
        assert abs(imc - expected) < 0.1
        print(f" Cálculo básico: {imc:.2f}")
        tests_pasados += 1
    except Exception as e:
        print(f" Cálculo básico falló: {e}")
    total_tests += 1
    
    # Test 2: Clasificaciones
    try:
        test_cases = [
            (16.5, "Bajo peso (delgadez moderada)"),
            (18.0, "Bajo peso (delgadez leve)"),
            (22.0, "Peso normal"),
            (27.0, "Sobrepeso"),
            (32.0, "Obesidad grado I"),
            (37.0, "Obesidad grado II"),
            (42.0, "Obesidad grado III")
        ]
        
        for imc_val, expected in test_cases:
            result = calc.clasificar(imc_val)
            assert result == expected, f"Esperado: {expected}, Obtenido: {result}"
        
        print(" Todas las clasificaciones correctas")
        tests_pasados += 1
    except Exception as e:
        print(f" Clasificaciones fallaron: {e}")
    total_tests += 1
    
    # Test 3: Historial y cola
    try:
        calc.agregar_historial(70, 1.75)
        calc.agregar_historial(65, 1.70)
        calc.encolar_calculo(80, 1.80)
        calc.encolar_calculo(75, 1.78)
        calc.procesar_cola()
        
        assert len(calc.historial_imc) == 4
        assert len(calc.cola_imc) == 0
        print("Historial y cola funcionando")
        tests_pasados += 1
    except Exception as e:
        print(f" Historial/cola falló: {e}")
    total_tests += 1
    
    # Test 4: Nuevas funciones - Estadísticas
    try:
        stats = calc.obtener_estadisticas()
        assert stats['total_registros'] == 4
        print(f" Estadísticas: {stats['total_registros']} registros, promedio: {stats['imc_promedio']:.2f}")
        tests_pasados += 1
    except Exception as e:
        print(f" Estadísticas fallaron: {e}")
    total_tests += 1
    
    # Test 5: Nuevas funciones - Peso ideal
    try:
        peso_ideal = calc.peso_ideal_rango(1.75)
        assert 'peso_min_ideal_kg' in peso_ideal
        print(f" Peso ideal para 1.75m: {peso_ideal['rango_recomendado']}")
        tests_pasados += 1
    except Exception as e:
        print(f" Peso ideal falló: {e}")
    total_tests += 1
    
    # Test 6: Filtrado y evolución
    try:
        normales = calc.filtrar_por_clasificacion("Peso normal")
        evolucion = calc.obtener_evolucion()
        print(f" Filtrado: {len(normales)} registros normales, Evolución: {len(evolucion)} registros")
        tests_pasados += 1
    except Exception as e:
        print(f" Filtrado/evolución falló: {e}")
    total_tests += 1
    
    print(f"\n IMC: {tests_pasados}/{total_tests} pruebas exitosas")
    return tests_pasados, total_tests

def test_calculadora_grasa_corporal():
    """Pruebas completas para CalculadoraGrasaCorporal"""
    print("\n" + "="*60)
    print("TEST CALCULADORA GRASA CORPORAL")
    print("="*60)
    
    calc = CalculadoraGrasaCorporal()
    tests_pasados = 0
    total_tests = 0
    
    # Test 1: Cálculo básico
    try:
        grasa = calc.calcular(25.0, 30, 'M')
        print(f" Cálculo básico grasa: {grasa:.2f}%")
        tests_pasados += 1
    except Exception as e:
        print(f" Cálculo básico grasa falló: {e}")
    total_tests += 1
    
    # Test 2: Clasificación de grasa
    try:
        clasificacion = calc.clasificar_grasa(15.0, 'M', 25)
        assert "Atleta" in clasificacion or "Fitness" in clasificacion
        print(f" Clasificación grasa: {clasificacion}")
        tests_pasados += 1
    except Exception as e:
        print(f" Clasificación grasa falló: {e}")
    total_tests += 1
    
    # Test 3: Registros y cola
    try:
        calc.agregar_registro(25.0, 30, 'M')
        calc.agregar_registro(22.0, 25, 'F')
        calc.encolar_calculo(28.0, 35, 'M')
        calc.encolar_calculo(24.0, 28, 'F')
        calc.procesar_cola()
        
        assert len(calc.registros_grasa) == 4
        assert len(calc.cola_grasa) == 0
        print(" Registros y cola funcionando")
        tests_pasados += 1
    except Exception as e:
        print(f" Registros/cola falló: {e}")
    total_tests += 1
    
    
    try:
        # Agregar más datos para tendencia
        calc.agregar_registro(26.0, 31, 'M')
        tendencia = calc.obtener_tendencia_grasa()
        print(f" Tendencia: {tendencia['tendencia']}")
        tests_pasados += 1
    except Exception as e:
        print(f" Tendencia falló: {e}")
    total_tests += 1
    
    
    try:
        recomendacion = calc.recomendar_objetivo(25.0, 'M', 30)
        assert 'objetivo_recomendado' in recomendacion
        print(f" Recomendación: {recomendacion['mensaje']}")
        tests_pasados += 1
    except Exception as e:
        print(f" Recomendación falló: {e}")
    total_tests += 1
    
    # Test 6: Filtrado por sexo
    try:
        hombres = calc.filtrar_por_sexo('M')
        mujeres = calc.filtrar_por_sexo('F')
        print(f"Filtrado: {len(hombres)} hombres, {len(mujeres)} mujeres")
        tests_pasados += 1
    except Exception as e:
        print(f" Filtrado falló: {e}")
    total_tests += 1
    
    print(f"\n Grasa Corporal: {tests_pasados}/{total_tests} pruebas exitosas")
    return tests_pasados, total_tests

def test_calculadora_masa_muscular():
    """Pruebas completas para CalculadoraMasaMuscular"""
    print("\n" + "="*60)
    print("TEST CALCULADORA MASA MUSCULAR")
    print("="*60)
    
    calc = CalculadoraMasaMuscular()
    tests_pasados = 0
    total_tests = 0
    
    # Test 1: Cálculo básico
    try:
        composicion = calc.calcular(70, 18.5)
        assert 'masa_magra_kg' in composicion
        assert 'grasa_corporal_kg' in composicion
        print(f" Cálculo básico: Masa magra {composicion['masa_magra_kg']:.2f}kg")
        tests_pasados += 1
    except Exception as e:
        print(f" Cálculo básico falló: {e}")
    total_tests += 1
    
    # Test 2: Composiciones y cola
    try:
        calc.agregar_composicion(70, 18.5)
        calc.agregar_composicion(85, 25.0)
        calc.encolar_analisis(68, 20.0)
        calc.encolar_analisis(72, 22.0)
        calc.procesar_cola()
        
        assert len(calc.composiciones) == 4
        assert len(calc.cola_composiciones) == 0
        print(" Composiciones y cola funcionando")
        tests_pasados += 1
    except Exception as e:
        print(f" Composiciones/cola falló: {e}")
    total_tests += 1
    
    # Test 3: Nuevas funciones - Índice muscular
    try:
        indice = calc.calcular_indice_muscular()
        print(f" Índice muscular: {indice:.2f}%")
        tests_pasados += 1
    except Exception as e:
        print(f" Índice muscular falló: {e}")
    total_tests += 1
    
 
    try:
        
        calc.agregar_composicion(69, 17.5)
        progreso = calc.obtener_progreso_muscular()
        print(f" Progreso: {progreso['progreso']}, cambio: {progreso['cambio_kg']:.2f}kg")
        tests_pasados += 1
    except Exception as e:
        print(f" Progreso falló: {e}")
    total_tests += 1
    
    # Test 5: Nuevas funciones - Recomendación entrenamiento
    try:
        recomendacion = calc.recomendar_entrenamiento()
        print(f" Entrenamiento recomendado: {recomendacion}")
        tests_pasados += 1
    except Exception as e:
        print(f" Recomendación entrenamiento falló: {e}")
    total_tests += 1
    
    # Test 6: Nuevas funciones - Déficit calórico
    try:
        if calc.composiciones:
            deficit = calc.calcular_deficit_calorico(65, 15.0, 10)
            if 'error' not in deficit:
                print(f" Déficit calórico: {deficit['deficit_calorico_diario']:.0f} kcal/día")
                tests_pasados += 1
            else:
                print("  Déficit calórico: no aplicable")
                tests_pasados += 1
    except Exception as e:
        print(f" Déficit calórico falló: {e}")
    total_tests += 1
    
    print(f"\n Masa Muscular: {tests_pasados}/{total_tests} pruebas exitosas")
    return tests_pasados, total_tests

def test_integracion_completa():
    """Prueba de integración entre todas las calculadoras"""
    print("\n" + "="*60)
    print("TEST INTEGRACIÓN COMPLETA")
    print("="*60)
    
    tests_pasados = 0
    total_tests = 0
    
    try:
        calc_imc = CalculadoraIMC()
        calc_grasa = CalculadoraGrasaCorporal()
        calc_muscular = CalculadoraMasaMuscular()
        
        # Flujo integrado completo
        peso = 70
        altura = 1.75
        edad = 30
        sexo = 'M'
        
        # 1. Calcular IMC
        imc = calc_imc.calcular(peso, altura)
        calc_imc.agregar_historial(peso, altura)
        
        # 2. Calcular grasa corporal usando IMC
        grasa = calc_grasa.calcular(imc, edad, sexo)
        calc_grasa.agregar_registro(imc, edad, sexo)
        
        # 3. Calcular composición muscular usando grasa
        composicion = calc_muscular.calcular(peso, grasa)
        calc_muscular.agregar_composicion(peso, grasa)
        
        print(f" Flujo integrado completo:")
        print(f"   IMC: {imc:.2f}")
        print(f"   Grasa corporal: {grasa:.2f}%")
        print(f"   Masa muscular: {composicion['masa_magra_kg']:.2f}kg")
        
        tests_pasados += 1
    except Exception as e:
        print(f" Flujo integrado falló: {e}")
    total_tests += 1
    
    # Test 2: Evolución temporal integrada
    try:
        print("\n--- Simulación evolución 3 meses ---")
        datos_evolucion = [
            (75, 1.75, 35, 'M', "Mes 1"),
            (72, 1.75, 32, 'M', "Mes 2"), 
            (70, 1.75, 30, 'M', "Mes 3")
        ]
        
        for peso, altura, edad, sexo, periodo in datos_evolucion:
            imc_evo = calc_imc.calcular(peso, altura)
            grasa_evo = calc_grasa.calcular(imc_evo, edad, sexo)
            composicion_evo = calc_muscular.calcular(peso, grasa_evo)
            
            print(f"   {periodo}: IMC={imc_evo:.1f}, Grasa={grasa_evo:.1f}%, Músculo={composicion_evo['masa_magra_kg']:.1f}kg")
        
        print(" Evolución temporal integrada")
        tests_pasados += 1
    except Exception as e:
        print(f" Evolución temporal falló: {e}")
    total_tests += 1
    
    # Test 3: Análisis completo de usuario
    try:
        print("\n--- Análisis completo de usuario ---")
        stats_imc = calc_imc.obtener_estadisticas()
        tendencia_grasa = calc_grasa.obtener_tendencia_grasa()
        progreso_muscular = calc_muscular.obtener_progreso_muscular()
        
        print(f"   Estadísticas IMC: {stats_imc['total_registros']} registros")
        print(f"   Tendencia grasa: {tendencia_grasa['tendencia']}")
        print(f"   Progreso muscular: {progreso_muscular['progreso']}")
        
        tests_pasados += 1
    except Exception as e:
        print(f" Análisis completo falló: {e}")
    total_tests += 1
    
    print(f"\n Integración: {tests_pasados}/{total_tests} pruebas exitosas")
    return tests_pasados, total_tests

def test_rendimiento():
    """Pruebas de rendimiento"""
    print("\n" + "="*60)
    print("TEST RENDIMIENTO")
    print("="*60)
    
    calc_imc = CalculadoraIMC()
    start_time = time.time()
    
  
    for i in range(50):
        calc_imc.encolar_calculo(70 + i, 1.75 + i/100)
    
    calc_imc.procesar_cola()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f" Procesados 50 cálculos en {duration:.4f} segundos")
    print(f" Historial final: {len(calc_imc.historial_imc)} registros")
    
    return 1, 1

def main():
    """Función principal"""
    print(" INICIANDO TEST COMPLETO HIGHT BOD HEAVY")
    print(f" {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    start_time = time.time()
    total_pasados = 0
    total_tests = 0
    
    # Ejecutar todas las pruebas
    resultados = []
    
    resultados.append(test_calculadora_imc())
    resultados.append(test_calculadora_grasa_corporal())
    resultados.append(test_calculadora_masa_muscular())
    resultados.append(test_integracion_completa())
    resultados.append(test_rendimiento())
    
    # Calcular totales
    for pasados, total in resultados:
        total_pasados += pasados
        total_tests += total
    
 
    end_time = time.time()
    duracion = end_time - start_time
    
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"⏱  Duración total: {duracion:.2f} segundos")
    print(f" Total pruebas: {total_tests}")
    print(f" Pruebas exitosas: {total_pasados}")
    print(f" Pruebas fallidas: {total_tests - total_pasados}")
    print(f" Tasa de éxito: {(total_pasados/total_tests)*100:.1f}%")
    
    if total_pasados == total_tests:
        print("\n ¡TODAS LAS PRUEBAS EXITOSAS!")
        return 0
    else:
        print(f"\n {total_tests - total_pasados} prueba(s) fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
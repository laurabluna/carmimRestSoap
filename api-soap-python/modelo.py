import joblib
import numpy as np

modelo = joblib.load("modelo.pkl")

MAPA_DIAGNOSTICO = {
    0: ("Nenhuma alteração significativa detectada", "Mantenha uma alimentação equilibrada e observe novos sintomas."),
    1: ("TPM leve", "Beba bastante água, evite cafeína e pratique exercícios leves."),
    2: ("Cólica menstrual comum", "Use analgésicos sob orientação médica e aplique compressas mornas."),
    3: ("Possível virose", "Descanse, hidrate-se e, se persistirem os sintomas, procure um clínico."),
    4: ("Alta chance de endometriose", "Procure um ginecologista para exames como ultrassonografia transvaginal com preparo intestinal.")
}

def prever_diagnostico_e_recomendacao(sintomas_dict):
    sintomas_em_ordem = [
        sintomas_dict.get("dor_abdominal", 0),
        sintomas_dict.get("ciclo_irregular", 0),
        sintomas_dict.get("fadiga", 0),
        sintomas_dict.get("dor_durante_sexo", 0),
        sintomas_dict.get("intestino_preso", 0)
    ]

    X = np.array([sintomas_em_ordem])
    classe = modelo.predict(X)[0]

    diagnostico, recomendacao = MAPA_DIAGNOSTICO.get(classe, ("Diagnóstico indefinido", "Consulte um profissional de saúde."))
    return diagnostico, recomendacao

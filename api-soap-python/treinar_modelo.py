from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

X = np.array([
    [1, 0, 1, 0, 0],  # TPM leve
    [1, 0, 0, 0, 0],  # Cólica
    [0, 0, 1, 0, 1],  # Virose
    [1, 1, 1, 1, 1],  # Endometriose
    [0, 0, 0, 0, 0]   # Nenhum
])

y = np.array([1, 2, 3, 4, 0])  

modelo = RandomForestClassifier()
modelo.fit(X, y)

joblib.dump(modelo, 'modelo.pkl')

print("Modelo treinado e salvo em modelo.pkl")

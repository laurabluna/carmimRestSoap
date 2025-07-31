
<script setup>
import capa from '@/assets/capa.png';
import { ref } from 'vue';


const sintomasSelecionados = ref([])

const sintomasMapeados = [
  'dor_abdominal',
  'ciclo_irregular',
  'fadiga',
  'dor_durante_o_sexo',
  'intestino_preso'
]


function toggleSintoma(sintoma) {
  if (sintomasSelecionados.value.includes(sintoma)) {
    sintomasSelecionados.value = sintomasSelecionados.value.filter(s => s !== sintoma)
  } else {
    sintomasSelecionados.value.push(sintoma)
  }
}

async function enviarSintomas() {
  try {
    const response = await fetch('http://localhost:3001/api/diagnostico', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sintomas: sintomasSelecionados.value })
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Erro ${response.status}: ${errorText}`)
    }

    const data = await response.json()
    alert(`✅ Diagnóstico: ${data.diagnostico}\n💡 Recomendação: ${data.recomendacao}`)

    sintomasSelecionados.value = [];
  } catch (error) {
    console.error('Erro ao enviar sintomas:', error)
    alert('Erro ao enviar sintomas: ' + error.message)
  }
}
</script>

<template>
  <div class>
    <div class="imagem-container">
        <img :src="capa" alt="capa" style="width:780px" />
    </div>

    <div class="titulo">
        <p class="text-2xl font-sembold mb-1 ">Como você está hoje?</p>
        <p class="mb-4 text-gray-700">Selecione os sintomas que você está sentindo hoje </p>
    </div>

      <div class="sintomas-grid">
        <button
            v-for="sintoma in sintomasMapeados"
            :key="sintoma"
            :class="['sintoma-btn', sintomasSelecionados.includes(sintoma) ? 'ativo' : '']"
            @click="toggleSintoma(sintoma)"
        >
            {{ sintoma.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
        </button>
        </div>

        <button
        class="enviar-btn"
        :disabled="sintomasSelecionados.length === 0"
        @click="enviarSintomas"
        >
        Enviar sintomas
        </button>
  </div>

  

</template>

<style scoped>

.sintomas-grid {
  display: flex;
  flex-wrap: wrap;           
  justify-content: center;  
  gap: 1rem;  
  min-height: 160px; /* altura mínima para evitar encolher */
  margin-bottom: 2rem;               
}

.sintoma-btn {
  background-color: #f0f4f8; 
  color: #333;
  border: 2px solid #b0c4de; 
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
  max-width: 200px;
  text-align: center;
}

.sintoma-btn:hover {
  background-color: #d0e2f2; 
}

.sintoma-btn.ativo {
  background-color: #007b8a; 
  color: white;
  border-color: #007b8a;
}

.btn-danger {
    background-color: #d9534f; 
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    cursor: pointer;
    transition: box-shadow 0.2s ease;
  }

  .btn-danger:active {
    box-shadow: none;
  }

.enviar-btn {
  margin-top: 1.5rem;
  background-color: #960018;
  color: white;
  border: none;
  padding: 1rem 3rem;
  border-radius: 28px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.25s ease;
  display: block;
  margin: 0 auto 3rem;
  margin-top: 2rem;
}

.enviar-btn:disabled {
  background-color: #f2a6a6;
  cursor: not-allowed;
  margin-top: 4.5rem;
}

.enviar-btn:not(:disabled):hover {
  background-color: #b52b27;
}

.imagem-container {
  display: flex;
  justify-content: center;
  padding-top: 2rem;
  background-color: #960018;
}

.imagem-container img {
  width: 100%;
  max-width: 780px;
  height: auto;
  display: block;
  border-radius: 4px;
}

.titulo {
  font-family: 'Montserrat', sans-serif;
  font-size: 20px;
  text-align: center;
  margin-bottom: 1.5rem 1rem 2rem;
  color: #333;

}

.titulo p:first-child {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.titulo p:last-child {
  font-size: 1rem;
  color: #555;
}

@media (max-width: 768px) {
  .titulo p:first-child {
    font-size: 1.5rem;
  }

  .titulo p:last-child {
    font-size: 0.9rem;
  }

  .sintoma-btn {
    min-width: 120px;
    max-width: 150px;
    padding: 0.6rem 1rem;
  }

  .enviar-btn {
    padding: 0.9rem 2rem;
    max-width: 180px;
  }
}

@media (max-width: 480px) {
  .titulo p:first-child {
    font-size: 1.25rem;
  }

  .titulo p:last-child {
    font-size: 0.85rem;
  }

  .sintoma-btn {
    min-width: 100px;
    max-width: 140px;
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
  }

  .enviar-btn {
    padding: 0.8rem 1.5rem;
    max-width: 160px;
  }
}


  
</style>
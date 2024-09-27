<template>
  <div> 
    <div class="mt-10 px-4 sm:px-6 lg:px-8">
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-base font-semibold leading-6 text-gray-900">Prédictions des Biens</h1>
        </div>
      </div>
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <table class="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">Surface</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Prix</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Note Prédite</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(prediction, index) in predictions" :key="index">
                  <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">{{ prediction.surface }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ prediction.prix }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ prediction.note }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const predictions = ref([])

const people = [
  { name: 'Lindsay Walton', title: 'Front-end Developer', email: 'lindsay.walton@example.com', role: 'Member' },
]

const nbRooms = 2
const surface = 50
const nbWindows = 4
const price = 100000

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:5001/training-note', {
        method: 'POST',
        body: JSON.stringify({
        chambres: nbRooms,
        surface: surface,
        fenetres: nbWindows,
        prix: price
        })
    })
  if (response.ok) {
      const result = await response.json()
      predictions.value.push({
        surface: 50,
        prix: 100000,
        note: result.predicted_note
      })
    } else {
      console.error('Erreur lors de la requête API', await response.text())
    }
  } catch (error) {
    console.error('Erreur lors de la requête API', error)
  }
})
</script>
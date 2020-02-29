<template>
  <div class="q-pa-md">
    <q-table
      title="Patients"
      :data="data"
      :columns="columns"
      row-key="name"
    />
  </div>
</template>


<script>
export default {
  data () {
    return {
      columns: [
        {
          name: 'name',
          required: true,
          label: 'Patients',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'Register date', align: 'center', label: 'Register date', field: 'date', sortable: true },
        { name: 'protein', label: 'Protein (g)', field: 'protein' },
        { name: 'sodium', label: 'Sodium (mg)', field: 'sodium' },

      ],
      data: [
        {
          name: 'Mark',
          date: '11-11-2020',
          protein: 4.0,
          sodium: 87,

        },
        {
          name: 'Ana',
          date: '10-02-2020',
          protein: 4.3,
          sodium: 129,
        }
      ]
    }
  }
}
</script>

<template>
  <div class="q-pa-md">
    <q-table
      title="Patients"
      :data="data"
      :columns="columns"
      row-key="name"
      :filter="filter"
    >

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="accent" round dense @click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'" />
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">
              <q-btn color="primary" label="Select patient" class="q-mt-md">
                <q-tooltip content-class="bg-accent">See {{ props.row.name }} data </q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>
</template>




<script>
export default {
  data () {
    return {
      filter: '',
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
        { name: 'age', label: 'Age', field: 'age' },

      ],
      data: [
        {
          name: 'Mark',
          date: '11-11-2020',
          age: 23,
        },
        {
          name: 'Ana',
          date: '10-02-2020',
          age: 45,
        }
      ]
    }
  }
}
</script>

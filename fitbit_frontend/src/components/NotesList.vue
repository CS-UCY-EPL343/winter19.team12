<template>
  <q-card class='bg-yellow-2'>
    <q-card-section>
      <div class="text-h6">Notes</div>
    </q-card-section>
    <q-separator />
    <q-card-section class='no-padding'>
      <q-list separator>
        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Note 1</q-item-label>
            <q-item-label caption>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Note 2</q-item-label>
            <q-item-label caption>Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple>
          <q-item-section>
            <q-item-label>Note 3</q-item-label>
            <q-item-label caption>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'NotesList'
}
</script>

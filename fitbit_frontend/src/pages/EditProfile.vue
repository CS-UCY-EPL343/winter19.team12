<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('Edit Profile')}}</div>
      </q-card-section>
  <div class="q-pa-xl" style="max-width: 100%">
    <q-input
      ref="input"
      filled
      v-model="model"
      label="Name"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='account_circle' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Surname"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='account_circle' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Date of birth"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='cake' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Height"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='height' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Gender"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='wc' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Username"
      :rules="[ myRule ]"
      >
      <template v-slot:prepend>
        <q-icon name='face' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Email"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='email' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Password"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='vpn_key' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Telephone"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='phone' />
      </template>
    </q-input>

    <q-input
      ref="input"
      filled
      v-model="model"
      label="Address"
      :rules="[ myRule ]"
    >
      <template v-slot:prepend>
        <q-icon name='home_work' />
      </template>
    </q-input>

    <q-btn class="q-mt-sm" label="Update Profile" @click="onsubmit" color="primary"/>
  </div>
    </q-card>
  </q-page>
</template>

<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('Edit Profile')}}</div>
      </q-card-section>
      <q-separator />
      <q-card-section class='q-col-gutter-sm q-py-lg'>
      <q-input :label="$t('username')"
                 :hint="$t('username_hint')"
                 type='text'
                 v-model='username'
                 ref='username'
                 autofocus
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='face' />
          </template>
        </q-input>
        <q-input :label="$t('change_password')"
                 :hint="$t('change_password_hint')"
                 type='change_password'
                 v-model='change_password'
                 ref='change_password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
        <q-input :label="$t('retype_change_password')"
                 :hint="$t('retype_change_password_hint')"
                 type='retype_change_password'
                 v-model='retype_change_password'
                 ref='retype_change_password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
        <q-input :label="$t('name')"
                 :hint="$t('name_hint')"
                 type='name'
                 v-model='name'
                 ref='name'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='account_circle' />
          </template>
        </q-input>
        <q-input :label="$t('surname')"
                 :hint="$t('surname_hint')"
                 type='surname'
                 v-model='surname'
                 ref='surname'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='account_circle' />
          </template>
       </q-input>
       <q-input :label="$t('email')"
                 :hint="$t('email_hint')"
                 type='email'
                 v-model='email'
                 ref='email'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='email' />
          </template>
       </q-input>
       <q-input :label="$t('birth')"
                 :hint="$t('birth_hint')"
                 type='birth'
                 v-model='birth'
                 ref='birth'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='cake' />
          </template>
       </q-input>
       <q-input :label="$t('height')"
                 :hint="$t('height_hint')"
                 type='height'
                 v-model='height'
                 ref='height'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='height' />
          </template>
       </q-input>
       <q-input :label="$t('gender')"
                 :hint="$t('gender_hint')"
                 type='gender'
                 v-model='gender'
                 ref='gender'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='wc' />
          </template>
       </q-input>
       <q-input :label="$t('phone')"
                 :hint="$t('phone_hint')"
                 type='phone'
                 v-model='phone'
                 ref='phone'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='phone' />
          </template>
       </q-input>
       <q-input :label="$t('address')"
                 :hint="$t('address_hint')"
                 type='address'
                 v-model='address'
                 ref='address'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='home' />
          </template>
       </q-input>
      </q-card-section>
      <q-separator />
      <q-card-actions class='bg-grey-1 q-pl-none'>
        <div class='row full-width q-col-gutter-sm'>
          <div class='col-xs-12 col-sm-12'>
            <q-btn
              @click='submit'
              :label='$t("Update Profile Data")'
              icon='exit_to_app' color='primary' no-caps v-ripple
              class='full-width'
            />
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Register',
  data () {
    return {
      username: '',
      email: '',
      change_password: '',
      retype_change_password: '',
      name: '',
      surname: '',
      birth: '',
      height: '',
      gender: '',
      phone: '',
      address: ''
    }
  },  
  methods: {
    filldata () {
      axios.post('http://52.186.12.191/get_user_info', {
        'username': 'infouser2'
      }).then(response => {
        this.name = response.data.first_name
        this.surname = response.data.last_name
        this.email = response.data.email
        this.birth = response.data.birthdate
        this.height = response.data.height
        this.gender = response.data.gender
        this.phone = response.data.telephone
        this.address = response.data.address
      })  
    },
    submit () {
      if ((this.change_password !== '' && this.retype_change_password === '') || (this.change_password === '' && this.retype_change_password !== '')) {
        this.$q.notify('Please fill both passwords if you want to change.')
      } else if (this.password !== this.retype_password) {
        this.$q.notify('Passwords not match.')
      } else {
        this.$q.notify(`Data Updated!`)
        axios.post('http://52.186.12.191/edit_profile_api', {
          'username': this.username,
          'password': this.change_password,
          'name': this.name,
          'surname': this.surname,
          'birthday': this.birth,
          'height': this.height,
          'gender': this.gender,
          'email': this.email,
          'telephone': this.phone,
          'address': this.address
        }).then(response => {
          this.info = response
        })
      }
    }
  },
  created () {
    this.filldata()
  }
}
</script>

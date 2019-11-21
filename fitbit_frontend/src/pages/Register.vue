<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('Register')}}</div>
      </q-card-section>
      <q-separator />
      <q-card-section class='q-col-gutter-xl q-py-lg'>
      <q-input :label="$t('username')"
                 :hint="$t('username_hint')"
                 :rules='usernameRules'
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
        <q-input :label="$t('Name')"
                 :hint="$t('name_hint')"
                 :rules='nameRules'
                 type='text'
                 v-model='name'
                 ref='name'
                 autofocus
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='perm_identity' />
          </template>
        </q-input>
        <q-input :label="$t('Surname')"
                 :hint="$t('surname_hint')"
                 :rules='nameRules'
                 type='text'
                 v-model='surname'
                 ref='surname'
                 autofocus
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='perm_identity' />
          </template>
        </q-input>
        <q-input :label="$t('Email')"
                 :hint="$t('email_hint')"
                 :rules='emailRules'
                 type='text'
                 v-model='email'
                 ref='email'
                 autofocus
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='email' />
          </template>
        </q-input>
        <q-input :label="$t('password')"
                 :hint="$t('password_hint')"
                 :rules='passwordRules'
                 type='password'
                 v-model='password'
                 ref='password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
        <q-input :label="$t('retype_password')"
                 :hint="$t('retype_password_hint')"
                 :rules='passwordRules'
                 type='password'
                 v-model='retype_password'
                 ref='retype_password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
       <div class='row full-width q-col-gutter-sm'>
          <div class="q-gutter-sm">
             <q-radio dense v-model="type" val="user_select" label="Fitbit User" />
             <q-radio dense v-model="type" val="specialist_select" label="Specialist" />
          </div>
       </div>
       <q-slide-transition>
       <div v-show="type === 'user_select'">
       <q-input :label="$t('serial_number')"
                 :hint="$t('serial_number_hint')"
                 type='serial_number'
                 v-model='serial_number'
                 ref='serial_number'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='watch' />
          </template>
        </q-input>   
       </div>
       </q-slide-transition>
      </q-card-section>
      <q-separator />
      <q-card-actions class='bg-grey-1 q-pl-none'>
        <div class='row full-width q-col-gutter-sm'>
          <div class='col-xs-12 col-sm-12'>
            <q-btn
              @click='submit'
              :label='$t("Register")'
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
      password: '',
      retype_password: '',
      type: 'user_select',
      serial_number: ''
    }
  },
  methods: {
    submit () {
      if (this.username === '' || this.name === '' || this.surname === '' || this.password === '' || this.email === '' || this.retype_password === '') {
        this.$q.notify('Please fill in all the fields in the form.')
      } else if (this.password !== this.retype_password) {
        this.$q.notify('Passwords not match.')
      } else if (this.type === 'user_select' && this.serial_number === '') {
        this.$q.notify('Please enter Fitbit Device Serial Number.')
      } else {
        this.$q.notify(`${this.username} submitted the form.`)
        axios.post('http://104.214.238.252/register', {
          username: this.username,
          passwrod1: this.password
        }).then((response) => {})
          .catch((e) => {
            console.error(e)
          })        
      }      
    }
  }
}

</script>

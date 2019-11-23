<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('Register')}}</div>
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
        <q-input :label="$t('password')"
                 :hint="$t('password_hint')"
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
      if (this.username === '' || this.password === '' || this.retype_password === '') {
        this.$q.notify('Please fill in all the fields in the form.')
      } else if (this.password !== this.retype_password) {
        this.$q.notify('Passwords not match.')
      } else {
        this.$q.notify(`${this.username} submitted the register form.`)
        axios.post('http://52.186.12.191/register_api', {
          'username': this.username,
          'password': this.password,
          'repeat_password': this.retype_password
        }).then(response => {
          this.info = response
        })
      }
    }
  }  
}
</script>

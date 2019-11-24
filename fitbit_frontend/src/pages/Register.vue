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
        <q-input :label="$t('password')"
                 :hint="$t('password_hint')"
                 :rules='passwordRules'
                 v-model='password'
                 :type="isPwd1 ? 'password' : 'text'"
                 ref='password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:append>
            <q-icon
              :name="isPwd1 ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd1 = !isPwd1"
            />
          </template>
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
        <q-input :label="$t('retype_password')"
                 :hint="$t('retype_password_hint')"
                 :rules='passwordRules'
                 v-model='retype_password'
                 :type="isPwd2 ? 'password' : 'text'"
                 ref='retype_password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:append>
            <q-icon
              :name="isPwd2 ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd2 = !isPwd2"
            />
          </template>
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
          <div class='col-xs-12 col-sm-6'>
            <q-btn
              @click='submit'
              :label='$t("Register")'
              icon='add_box' color='primary' no-caps v-ripple
              class='full-width'
            />
          </div>
          <div class='col-xs-12 col-sm-6'>
              <q-btn
                :to='{name: "login"}'
                :label='$t("Already have an account? Login")'
                icon='exit_to_app' color='secondary' no-caps v-ripple
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
      isPwd1: true,
      isPwd2: true,
      type: 'user_select',
      serial_number: '',
      usernameRules: [
        val => !!val || this.$t('field_required')
      ],
      passwordRules: [
        val => !!val || this.$t('field_required')
      ]
    }
  },
  methods: {
    submit () {
      if (this.username === '' || this.password === '' || this.retype_password === '') {
        this.$q.notify('Some fields are empty!')
      } else if (this.password !== this.retype_password) {
        this.$q.notify('Passwords not match.')
      } else {
        axios.post('http://' + this.$t('domain') + '/register_api', {
          'username': this.username,
          'password': this.password,
          'repeat_password': this.retype_password
        }).then(response => {
          if (response.data.error === 'username already exists') {
            this.$q.notify(`Username '${this.username}' already exists! Enter a new one.`)
          } else {
            this.$q.notify(`User '${this.username}' created!`)
          }
        })
      }
    }
  }  
}
</script>

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
                 v-model='change_password'
                 :type="isPwd1 ? 'password' : 'text'"
                 ref='change_password'
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
        <q-input :label="$t('retype_change_password')"
                 :hint="$t('retype_change_password_hint')"
                 v-model='retype_change_password'
                 :type="isPwd2 ? 'password' : 'text'"
                 ref='retype_change_password'
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
        <q-input :label="$t('name')"
                 :hint="$t('name_hint')"
                 type='text'
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
                 type='text'
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
                 type='text'
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
                 type='text'
                 v-model='birth'
                 ref='birth'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='event' />
          </template>
       </q-input>
       <q-input :label="$t('height')"
                 :hint="$t('height_hint')"
                 type='number'
                 v-model='height'
                 suffix="centimeters"
                 ref='height'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='height' />
          </template>
       </q-input>
       <q-select outlined v-model="gender" :options="options" label="Gender" :hint="$t('gender_hint')"/>
       <q-input :label="$t('phone')"
                 :hint="$t('phone_hint')"
                 type='tel'
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
                 type='text'
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
          <div class='col-xs-12 col-sm-7'>
            <q-btn
              @click='submit'
              :label='$t("Update Profile Data")'
              icon='exit_to_app' color='primary' no-caps v-ripple
              class='full-width'
            />
          </div>
          <div class='col-xs-12 col-sm-5'>
              <q-btn
                :to='{name: "dashboard"}'
                :label='$t("Return to Dashboard")'
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
      change_password: '',
      retype_change_password: '',
      isPwd1: true,
      isPwd2: true,
      name: '',
      surname: '',
      birth: '',
      height: '',
      options: [
        'Male', 'Female'
      ],
      gender: '',
      phone: '',
      address: ''
    }
  },  
  methods: {
    filldata () {
      axios.post('http://' + this.$t('domain') + '/get_user_info', {
        'username': 'info7'
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
        this.$q.notify('Please fill both passwords if you want to change your password.')
      } else if (this.password !== this.retype_password) {
        this.$q.notify('Passwords not match.')
      } else {
        this.$q.notify(`Data Updated Successfully!`)
        axios.post('http://' + this.$t('domain') + '/edit_profile_api', {
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

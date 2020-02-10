<template>
  <q-page padding class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('edit_profile')}}</div>
      </q-card-section>
      <q-separator />
      <q-form @submit='submit' spellcheck='false'>
        <q-card-section class='q-col-gutter-lg q-py-lg'>
          <div>Leave the password fields empty if you do not want to change your password.</div>
          <q-input :label="$t('change_password')"
                   :hint="$t('change_password_hint')"
                   v-model='password'
                   :type="isPwd1 ? 'password' : 'text'"
                   ref='password'
                   outlined bottom-slots
                   dense
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
                   v-model='confirmPassword'
                   :type="isPwd2 ? 'password' : 'text'"
                   ref='confirmPassword'
                   :rules='confirmPasswordRules'
                   outlined bottom-slots
                   dense
                   lazy-rules
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
                   outlined bottom-slots
                   dense
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
                   outlined bottom-slots
                   dense
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
                   outlined bottom-slots
                   dense
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
                   outlined bottom-slots
                   dense
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
                   outlined bottom-slots
                   dense
          >
            <template v-slot:prepend>
              <q-icon name='height' />
            </template>
          </q-input>
          <q-select outlined dense v-model="gender" :options="options" label="Gender" :hint="$t('gender_hint')"/>
          <q-input :label="$t('phone')"
                   :hint="$t('phone_hint')"
                   type='tel'
                   v-model='phone'
                   ref='phone'
                   outlined bottom-slots
                   dense
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
                   outlined bottom-slots
                   dense
          >
            <template v-slot:prepend>
              <q-icon name='home' />
            </template>
          </q-input>
        </q-card-section>
        <q-separator />
        <q-card-actions class='bg-grey-1 q-pl-none'>
          <div class='row full-width q-col-gutter-sm'>
            <div class='col-12'>
              <q-btn
                type='submit'
                :label='$t("update_profile")'
                icon='exit_to_app' color='primary' no-caps v-ripple
                class='full-width'
              />
            </div>
          </div>
        </q-card-actions>
      </q-form>

    </q-card>
  </q-page>
</template>

<script>
import store from 'src/store/index'

export default {
  name: 'Register',
  data () {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      isPwd1: true,
      isPwd2: true,
      name: '',
      surname: '',
      birth: '1997-05-04',
      height: '',
      options: [
        'Male', 'Female'
      ],
      gender: '',
      phone: '',
      address: '',
      confirmPasswordRules: [
        val => this.password === val || 'Passwords do not match.'
      ]
    }
  },
  methods: {
    fetchUserData () {
      this.$q.loading.show()
      this.$axios.post(this.$store.state.main.domain + '/get_user_info', {
        'username': this.$store.state.main.username
      }).then(response => {
        this.name = response.data.first_name
        this.surname = response.data.last_name
        this.email = response.data.email
        this.birth = response.data.birthdate
        this.height = response.data.height
        this.gender = response.data.gender
        this.phone = response.data.telephone
        this.address = response.data.address
        this.$q.loading.hide()
      })
    },
    submit () {
      this.$q.loading.show()
      this.$axios.post(this.$store.state.main.domain + '/edit_profile_api', {
        'username': this.$store.state.main.username,
        'password': this.password,
        'name': this.name,
        'surname': this.surname,
        'birthday': this.birth,
        'height': this.height,
        'gender': this.gender,
        'email': this.email,
        'telephone': this.phone,
        'address': this.address
      }).then(response => {
        if (response.data.status === '1') {
          this.$q.notify(`User information updated successfully!`)
        }
        this.$q.loading.hide()
      })
    }
  },
  mounted () {
    this.fetchUserData()
  },
  beforeRouteEnter (to, from, next) {
    if (store().state.main.username === '') {
      if (from.path === '/login') {
        next('/ulogin')
      }
      next('/login')
    }
    next()
  }
}
</script>

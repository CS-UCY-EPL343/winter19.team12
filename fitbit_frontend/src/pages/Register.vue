htm<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('register')}}</div>
      </q-card-section>
      <q-separator />
      <q-form @submit='submit' spellcheck='false'>
        <q-card-section class='q-col-gutter-lg q-py-lg'>
          <q-input :label="$t('username')"
                   :hint="$t('username_hint')"
                   :rules='usernameRules'
                   type='text'
                   v-model='username'
                   ref='username'
                   outlined bottom-slots
                   lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name='face' />
            </template>
          </q-input>

          <q-input :label="$t('email')"
                   :hint="$t('email_hint')"
                   type='text'
                   v-model='email'
                   ref='email'
                   :rules="[val => !!val || 'Email is missing', isValidEmail]"
                   outlined bottom-slots
          >
            <template v-slot:prepend>
              <q-icon name='email' />
            </template>
          </q-input>


          <q-input :label="$t('password')"
                   :hint="$t('password_hint')"
                   :rules='passwordRules'
                   v-model='password'
                   :type="isPwd1 ? 'password' : 'text'"
                   ref='password'
                   outlined bottom-slots
                   lazy-rules
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
                   :rules='confirmPasswordRules'
                   v-model='retypePassword'
                   :type="isPwd2 ? 'password' : 'text'"
                   ref='retypePassword'
                   outlined bottom-slots
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
          <div class='row full-width q-col-gutter-sm'>
            <div class="q-gutter-sm">
              <q-radio dense v-model="type" val="user_select" label="Fitbit User" />
              <q-radio dense v-model="type" val="specialist_select" label="Specialist" />
            </div>
          </div>

          <div class="q-gutter-sm">
            <q-checkbox
              v-model="customModel"
              color="primary"
              label=""
              true-value="yes"
              false-value="no"
            />
              I acknowledge that i agree to the<a href='TermsAndConditions'>Terms of Use</a> and have read the<a href='PrivacyPolicy'>Privacy Policy</a> and<a href='CookiesPolicy'>Cookies Policy</a> .
          </div>
        </q-card-section>
        <q-separator />
        <q-card-actions class='bg-grey-1 q-pl-none'>
          <div class='row full-width q-col-gutter-sm'>
            <div class='col-xs-12 col-sm-6'>
              <q-btn
                type='submit'
                :label='$t("register")'
                icon='add_box' color='primary' no-caps v-ripple
                class='full-width'
                :disable="clickable"
              />
            </div>
            <div class='col-xs-12 col-sm-6'>
              <q-btn
                :to='{name: "login"}'
                label='Already have an account? Login'
                icon='exit_to_app' color='secondary' no-caps v-ripple
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
      customModel: 'no',
      username: '',
      email: '',
      password: '',
      retypePassword: '',
      isPwd1: true,
      isPwd2: true,
      type: 'user_select',
      serial_number: '',
      usernameRules: [
        val => !!val || this.$t('field_required')
      ],
      passwordRules: [
        val => !!val || this.$t('field_required')
      ],
      confirmPasswordRules: [
        val => !!val || this.$t('field_required'),
        val => this.password === val || 'Passwords do not match.'
      ]
    }
  },
  computed: {
    clickable(){
      if(this.customModel=='no'){
        return true
      }else
        return false
    }
  },
  mounted () {
    this.$refs.username.focus()
  },
  methods: {
    submit () {
      this.$q.loading.show()

      let config = {
          headers:{
            'Content-Type': 'application/json',
            Authorization:"Bearer "+store().state.main.token
          }
      }

      let data = {
        username: this.username,
        password: this.password,
        repeat_password: this.retypePassword,
        email: this.email,
        type: this.type
      }

      this.$axios.post(this.$store.state.main.domain + '/register_api',data).then(response => {
        if (response.data.error === 'username already exists') {
          this.$q.notify(`Username '${this.username}' already exists! Enter a new one.`)
          this.$refs.username.focus()
        } else {
          this.$q.notify(`Your account was created successfully`)
          this.$axios.post(this.$store.state.main.domain + '/get_token', {
            'username': this.username,
            'password': this.password
          }).then(response => {
            if (response.data.access) {
              if (this.type == 'specialist_select') {
                this.$store.commit('main/login', {'username':this.username,'token':response.data.access,'is_specialist':true})
                this.$router.push({ name: 'monitor' }) // Redirect to monitor
              }
              else {
                this.$store.commit('main/login', {'username':this.username,'token':response.data.access,'is_specialist':false})
                this.$router.push({ name: 'dashboard' }) // Redirect to dashboard
              }
            }
          })
        }
        this.$q.loading.hide()
      })
    },
    isValidEmail () {
      const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return emailPattern.test(this.email) || 'Invalid email';
  }
  },
  beforeRouteEnter (to, from, next) {
    if (store().state.main.username !== '') {
      if (from.path === '/') {
        next('/index')
      }
      next('/')
    }
    next()
  }
}
</script>

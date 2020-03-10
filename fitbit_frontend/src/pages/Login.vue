<template>
  <q-page padding class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('login')}}</div>
      </q-card-section>
      <q-separator />
      <q-form @submit='submit' spellcheck='false'>
        <q-card-section class='q-col-gutter-xl q-py-lg'>
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
          <q-input :label="$t('password')"
                   :hint="$t('password_hint')"
                   :rules='passwordRules'
                   v-model='password'
                   :type="isPwd ? 'password' : 'text'"
                   ref='password'
                   outlined bottom-slots
                   lazy-rules
          >
            <template v-slot:append>
              <q-icon
                :name="isPwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="isPwd = !isPwd"
              />
            </template>
            <template v-slot:prepend>
              <q-icon name='vpn_key' />
            </template>
          </q-input>
        </q-card-section>
        <q-separator />
        <q-card-actions class='bg-grey-1 q-pl-none'>
          <div class='row full-width q-col-gutter-sm'>
            <div class='col-xs-12 col-sm-6'>
              <q-btn
                type='submit'
                :label='$t("login")'
                icon='exit_to_app' color='primary' no-caps v-ripple
                class='full-width'
              />
            </div>
            <div class='col-xs-12 col-sm-6'>
              <q-btn
                :to='{name: "register"}'
                :label='$t("create_account")'
                icon='add_box' color='secondary' no-caps v-ripple
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
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      isPwd: true,
      usernameRules: [
        val => !!val || this.$t('field_required')
      ],
      passwordRules: [
        val => !!val || this.$t('field_required')
      ]
    }
  },
  mounted () {
    this.$refs.username.focus()
    this.$refs.username.resetValidation()
    this.$refs.password.resetValidation()
  },
  methods: {
    submit () {
      this.$q.loading.show()
      this.$axios.post(this.$store.state.main.domain + '/get_token', {
        'username': this.username,
        'password': this.password
      }).then(response => {
        if (response.data.access) {
          let access = response.data.access
          this.$axios.post(this.$store.state.main.domain + '/is_specialist', {
            'username': this.username}).then(response => {
              if (response.data.error === '-1') {
                alert("Error")
              }
              else {
                let is_specialist = response.data.is_specialist;
                if (is_specialist) {
                  this.$store.commit('main/login', {'username':this.username,'token':access,'is_specialist':is_specialist})
                  this.$router.push({ path: '/specialist', name: 'monitor'})
                  this.$q.notify(`You have logged in successfully as Specialist.`)
                }
                else {
                  this.$store.commit('main/login', {'username':this.username,'token':access,'is_specialist':is_specialist})
                  // this.$router.push('/apoel')
                  this.$router.push({ name: 'dashboard' })
                  this.$q.notify(`You have logged in successfully as Patient.`)
                }
              }
            })
        } else {
          this.$q.notify(`Wrong username or password!`)
        }
        this.$q.loading.hide()
      }).catch(response =>{
        this.$q.notify(`Wrong username or password!`)
        this.$q.loading.hide()
      })
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

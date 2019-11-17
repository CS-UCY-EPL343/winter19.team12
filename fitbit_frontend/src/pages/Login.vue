<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('login')}}</div>
      </q-card-section>
      <q-separator />
      <q-card-section class='q-col-gutter-xl q-py-lg'>
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
      </q-card-section>
      <q-separator />
      <q-card-actions class='bg-grey-1 q-pl-none'>
        <div class='row full-width q-col-gutter-sm'>
          <div class='col-xs-12 col-sm-7'>
            <q-btn
              @click='submit'
              :label='$t("login")'
              icon='exit_to_app' color='primary' no-caps v-ripple
              class='full-width'
            />
          </div>
          <div class='col-xs-12 col-sm-5'>
            <q-btn
              :to='{name: "register"}'
              :label='$t("create_account")'
              icon='add_box' color='secondary' no-caps v-ripple
              class='full-width'
            />
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submit () {
      console.log(this.username)
      console.log(this.password)

      if (this.username === '' || this.password === '') {
        this.$q.notify('Please fill in all the fields in the form.')
      } else {
        this.$q.notify(`${this.username} submitted the form.`)
      }
    }
  }
}
</script>

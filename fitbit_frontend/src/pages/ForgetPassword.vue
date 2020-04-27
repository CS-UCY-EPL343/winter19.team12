<template>
  <q-page class="flex flex-center">
    <q-card class='full-width' style='max-width: 700px'>
      <q-card-section class='bg-grey-1'>
        <div class='text-h6'>{{$t('Forget Password')}}</div>
      </q-card-section>
      <q-separator />
      <q-form @submit='submit' spellcheck='false'>
        <q-card-section class='q-col-gutter-lg q-py-lg'>

          <q-input :label="$t('email')"
                   :hint="$t('email_hint')"
                   type='text'
                   v-model='email'
                   ref='email'
                   outlined bottom-slots
          >
            <template v-slot:prepend>
              <q-icon name='email' />
            </template>
          </q-input>

          <q-input :label="$t('Verification code')"
                   :hint="$t('Verification code')"
                   type='text'
                   v-model='code'
                   ref='code'
                   outlined bottom-slots
                   lazy-rules
          >
          <template v-slot:prepend>
            <q-icon name='developer_mode' />
          </template>
          </q-input>

          <q-input :label="$t('New password')"
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

        </q-card-section>
        <q-separator />
        <q-card-actions class='bg-grey-1 q-pl-none'>
          <div class='row full-width q-col-gutter-sm'>
            <div class='col-xs-12 col-sm-6'>
              <q-btn
                type='submit'
                :label='$t("Change Password")'
                icon='add_box' color='primary' no-caps v-ripple
                class='full-width'
                :disable="clickable"
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
import axios from 'axios'

export default {
  name: 'forgetPassword',
  data () {
    return {
      email:'',
      code: '',
      password: '',
      retypePassword: '',
      isPwd1: true,
      isPwd2: true,

      passwordRules: [
        val => !!val || this.$t('field_required')
      ],
      confirmPasswordRules: [
        val => !!val || this.$t('field_required'),
        val => this.password === val || 'Passwords do not match.'
      ]
    }
  },
  methods: {
    submit () {

      let data={
        email: this.email,
        reset_code: this.code,
        password: this.password,
      }

      this.$axios.post(this.$store.state.main.domain + '/reset_password',data).then(response => {
        console.log(response);
        if (response.data.status == '1') {
          this.$q.notify(`Password reseted successfully!`)
        }
      })

    }
  }
}
</script>

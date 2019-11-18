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
        <q-input :label="$t('Email')"
                 :hint="$t('Enter your email.')"
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
        <q-input :label="$t('Retype Password')"
                 :hint="$t('password_hint')"
                 type='password'
                 v-model='password'
                 ref='retype_password'
                 spellcheck='false'
                 outlined bottom-slots
        >
          <template v-slot:prepend>
            <q-icon name='vpn_key' />
          </template>
        </q-input>
        <template>
           <div class='row full-width q-col-gutter-sm'>
              <div class="q-gutter-sm">
                 <q-radio dense v-model="shape" val="user_select" label="Fitbit User" />
                 <q-radio dense v-model="shape" val="specialist-select" label="Specialist" />
              </div>
           </div>
    </template>
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
export default {
  name: 'Register'
}

</script>

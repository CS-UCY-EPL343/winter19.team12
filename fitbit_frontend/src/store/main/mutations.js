import LocalStorage from 'quasar/src/plugins/LocalStorage'

export function login (state, obj) {
  LocalStorage.set('username', obj.username)
  LocalStorage.set('token',obj.token)
  state.username = obj.username
  state.token=obj.token
  state.loggedIn = true
}

export function logout (state) {
  LocalStorage.remove('username')
  LocalStorage.remove('token')
  state.username = ''
  state.token=''
  state.loggedIn = false
}

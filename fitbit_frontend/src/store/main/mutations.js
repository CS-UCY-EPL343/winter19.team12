import LocalStorage from 'quasar/src/plugins/LocalStorage'

export function login (state, username) {
  LocalStorage.set('username', username)
  state.username = username
  state.loggedIn = true
}

export function logout (state) {
  LocalStorage.remove('username')
  state.username = ''
  state.loggedIn = false
}

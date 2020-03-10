import LocalStorage from 'quasar/src/plugins/LocalStorage'

export function login (state, obj) {
  if(!LocalStorage.getItem('username')){//check if there isn't any session
    console.log(obj);
    LocalStorage.set('username', obj.username);
    LocalStorage.set('token',obj.token);
    LocalStorage.set('is_specialist',obj.is_specialist);
    state.username = obj.username
    state.token=obj.token
    state.loggedIn = true
    state.is_specialist = obj.is_specialist
  }

}

export function logout (state) {
  LocalStorage.remove('username')
  LocalStorage.remove('token')
  state.username = ''
  state.token=''
  state.loggedIn = false
}

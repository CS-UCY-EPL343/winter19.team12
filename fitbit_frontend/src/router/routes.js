
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { name: 'dashboard', path: '', alias: 'index', component: () => import('pages/Dashboard.vue') },
      { name: 'history', path: 'history', alias: 'uhistory', component: () => import('pages/History.vue') },
      { name: 'monitor', path: 'monitor', alias: 'umonitor', component: () => import('pages/Monitor_Screen.vue') },
      { name: 'login', path: 'login', alias: 'ulogin', component: () => import('pages/Login.vue') },
      { name: 'select_doctor', path: 'select_doctor', alias: 'uselect_doctor', component: () => import('pages/SelectDoctor.vue') },
      { name: 'register', path: 'register', alias: 'uregister', component: () => import('pages/Register.vue') },
      { name: 'help', path: 'help', component: () => import('pages/Help.vue') },
      { name: 'edit', path: 'edit', component: () => import('pages/EditProfile.vue') }
    ]
  },
  {
    path: '/specialist',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { name: 'dashboard', path: 'dashboard', alias: 'index', component: () => import('pages/Dashboard.vue') },
      { name: 'history', path: '', alias: 'uhistory', component: () => import('pages/History.vue') },
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes

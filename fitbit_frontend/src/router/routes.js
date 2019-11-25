
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { name: 'dashboard', path: '', alias: 'index', component: () => import('pages/Dashboard.vue') },
      { name: 'login', path: 'login', alias: 'ulogin', component: () => import('pages/Login.vue') },
      { name: 'register', path: 'register', alias: 'uregister', component: () => import('pages/Register.vue') },
      { name: 'help', path: 'help', component: () => import('pages/Help.vue') },
      { name: 'edit', path: 'edit', component: () => import('pages/EditProfile.vue') }
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

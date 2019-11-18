
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { name: 'dashboard', path: '', component: () => import('pages/Dashboard.vue') },
      { name: 'login', path: 'login', component: () => import('pages/Login.vue') },
      { name: 'register', path: 'register', component: () => import('pages/Register.vue') },
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

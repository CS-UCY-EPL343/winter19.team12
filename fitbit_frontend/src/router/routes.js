
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { name: 'dashboard', path: 'dashboard', alias: 'index', component: () => import('pages/Dashboard.vue') },
      { name: 'monitor', path: 'monitor', alias: 'umonitor', component: () => import('pages/Monitor_Screen.vue') },
      { name: 'history', path: 'history', alias: 'uhistory', component: () => import('pages/History.vue') },
      { name: 'login', path: 'login', alias: 'ulogin', component: () => import('pages/Login.vue') },
      { name: 'select_doctor', path: 'select_doctor', alias: 'uselect_doctor', component: () => import('pages/SelectDoctor.vue') },
      { name: 'register', path: 'register', alias: 'uregister', component: () => import('pages/Register.vue') },
      { name: 'help', path: 'help', component: () => import('pages/Help.vue') },
      { name: 'edit', path: 'edit', component: () => import('pages/EditProfile.vue') },
      { name: 'error', path: 'error', component: () => import('pages/Error404.vue') },
      { name: 'TermsAndConditions', path: 'TermsAndConditions', component: () => import('pages/TermsAndConditions.vue') },
      { name: 'CookiesPolicy', path: 'CookiesPolicy', component: () => import('pages/CookiesPolicy.vue') },
      { name: 'PrivacyPolicy', path: 'PrivacyPolicy', component: () => import('pages/PrivacyPolicy.vue') },
      { name: 'activity', path: 'activity', component: () => import('pages/Activity.vue') },
      { name: 'forgetPassword', path: 'forgetPassword', component: () => import('pages/ForgetPassword.vue') },
    ]
  },
  {
    path: '/track_user',
    component: () => import('layouts/SpecialistLayout.vue'),
    children: [
      { name: 'track_user/dashboard', path: 'dashboard', alias: 'index', component: () => import('pages/Dashboard.vue') },
      { name: 'track_user/history', path: 'history', alias: 'uhistory', component: () => import('pages/History.vue') },
      { name: 'track_user/help', path: 'help', component: () => import('pages/Help.vue') },
      { name: 'track_user/error', path: 'error', component: () => import('pages/Error404.vue') },
    ]
  },
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes

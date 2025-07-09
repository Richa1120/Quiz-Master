import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'
import router from '../routes'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_id: localStorage.getItem('user_id') || null,
    token: localStorage.getItem('token') || null,
    userType:  localStorage.getItem('user_type') || null,
  },
  getters: {
    USER_ID(state) {
      return state.user_id
    },
    TOKEN(state) {
      return state.token
    },
    USER_TYPE(state) {
      return state.userType
    }
  },
  mutations: {
    SIGNUP_MUTATION(state, payload) {
      state.token = payload.data.token
      state.user_id = payload.data.userId
    },
    LOGIN_MUTATION(state, payload) {
      state.token = payload.data.token
      state.user_id = payload.data.userId
      state.userType = payload.data?.userType
    },
    AdminLOGIN_MUTATION(state, payload){
      state.token = payload.data.token
      state.userType = payload.data?.userType
    },
    LOGOUT_MUTATION(state) {
      state.token = null
      state.userType = null
    },
  },
  actions: {
    async SIGNUP_ACTION({ commit }, payload) {
      try {
        const { data } = await axios.post('http://localhost:5000/register', payload)
        localStorage.setItem('token', data.token)
        localStorage.setItem('user_type', data.userType)
        localStorage.setItem('user_id', data.userId)
        router.push('/login')
        commit('SIGNUP_MUTATION', {data})
      } catch (error) {
        if (error.response && error.response.status === 409) {
          alert('Error:'+ error.response.data.message);
          console.log(error.response.data.message);
        } else {
          alert('Error during sign-up:'+ error);
          console.log(error);
        }
      }
    },
    async LOGIN_ACTION({ commit }, payload) {
      try {
        const { data } = await axios.post('http://localhost:5000/login', payload)
        if (data.message === 'Invalid') {
          alert('Invalid Credentials')
          return
        }
        localStorage.setItem('token', data.token)
        localStorage.setItem('user_type', data.userType)
        localStorage.setItem('user_id', data.userId)
        localStorage.setItem("username", data.username)
        console.log(data)
        router.push('/home')
        commit('LOGIN_MUTATION', {data})
      } catch (error) {
        console.log(error)
      }
    },


      async AdminLOGIN_ACTION({ commit }, payload) {
        try {
          const { data } = await axios.post('http://localhost:5000/admin/login', payload)
          if (data.message === 'Invalid') {
            alert('Invalid Credentials')
            return
          }
          localStorage.setItem('token', data.token)
          localStorage.setItem('user_type', data.userType)
          console.log(data)
          router.push('/admin/dashboard')
          commit('AdminLOGIN_MUTATION', { data })
        } catch (error) {
          console.log(error)
        }
      },
    LOGOUT_ACTION({ commit }) {
      commit('LOGOUT_MUTATION')
      localStorage.setItem('token','null')
      localStorage.setItem('user_type','null')
      router.push('/')
    },
  },
  modules: {
  }
})

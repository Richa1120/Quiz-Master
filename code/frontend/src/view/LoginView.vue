<template>
  <div>
    <userLogin />
    
  </div>
</template>






<script>

// import axios from 'axios'
import userLogin from '../components/userLogin.vue'

export default {
    name: 'logIn',
    components: {userLogin},
    data() {
      return {
        form: {
          name: '',
          password:'',
          
        },
        show: true
      }
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        let payload = {"name":this.form.name,"password":this.form.password}
        console.log(payload)
        // axios.post('http://127.0.0.1:5000/login', payload)
        this.$router.push('/')
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.name = ''
        this.form.password=''
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }



</script>


<template>
  <div>
    <SignUp />
    <!-- <img alt="Quiz Master Logo" src="../assets/quiz-master.png">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show" class="register">
      <b-form-group
        
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          
                id="input-1"
                v-model="form.email"
                type="email"
                placeholder="Enter email"
                required
            
        
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.email"
          placeholder="Enter name"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Password:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>


      

      <b-button type="submit" variant="primary">Submit</b-button>
      <br> <br>
      <b-button type="reset" variant="danger">Reset</b-button>

            <p style="margin: 2% 0">Already have an account? <router-link to="/" >Login here</router-link></p>


    </b-form> -->

  </div>
</template>






<script>

// import axios from 'axios'
import SignUp from '../components/SignUp.vue'

export default {
    
    components:{SignUp},
    data() {
      return {
        form: {
          email: '',
          password:'',
          
        },
        show: true
      }
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        let payload = {"email":this.form.email, "password":this.form.password}
        console.log(payload)
        // axios.post('http://127.0.0.1:5000/register', payload)
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.email = ''
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

<style scoped>
.register input{
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border: 3px solid skyblue;
}



.register button{
    width: 320px;
    height: 40px;
    border: 3px solid black;
    background: skyblue;
    color: black;
    cursor: pointer;
}
</style>

<template>
  <div class="login-container">
    <br>
    <img alt="Quiz Master Logo" src="../assets/quiz-logo.png" class="logo">
    <h2 style="color:black">Create a new account</h2>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show" class="login-form">
      <b-form-group label="Your Name:" label-for="input-name">
        <b-form-input
          id="input-name"
          v-model="form.name"
          placeholder="Enter name"
          required
          class="login-input"
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Your Email:" label-for="input-email">
        <b-form-input
          id="input-email"
          v-model="form.email"
          placeholder="Enter email"
          type="email"
          required
          class="login-input"
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Your Password:" label-for="input-password">
        <b-form-input
          id="input-password"
          v-model="form.password"
          placeholder="Enter password"
          type="password"
          required
          class="login-input"
        ></b-form-input>
      </b-form-group>

    <b-button type="reset" variant="danger" class="login-btn">Reset</b-button>
      <b-button type="submit" variant="primary" class="login-btn">Submit</b-button>

      <p class="signup-link">Already have an account? <router-link to="/login">Login here</router-link></p>
      <p class="signup-link">Not a User? <router-link to="/">Click here</router-link></p>
    </b-form>
  </div>
</template>


<script>

import { mapActions } from 'vuex';

export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
      },
      show: true,
    };
  },
  created(){document.title='Register';},
    methods: {
      ...mapActions({
        signUp: 'SIGNUP_ACTION'
      }),
      onSubmit(event) {
        event.preventDefault()
        let payload = {"name":this.form.name,"email":this.form.email, "password":this.form.password}
        console.log(payload)
        this.signUp(payload)
        .then(() => {
          // Reset form after successful signup
          this.onReset(event);
          // Show success message or redirect if needed
        })
        .catch((error) => {
          // Handle error messages from backend
          if (error.response && error.response.data && error.response.data.message) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = 'An error occurred during sign-up.';
          }
          // You can display the error message to the user or handle it as needed
          console.error('Signup error:', error);
        });
      },

      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.name = ''
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

.logo{
  width: 210px;
  height: 167px;
  border-radius: 30px;
  margin:2px;
}
.login-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  /* Set the background image */
  background-image: url("@/assets/gradient.jpg");
  background-size: cover;
  background-position: center;
}

.login-form {
  max-width: 400px;
  padding: 20px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.9); /* Set background color with transparency */
}

.login-input {
  width: 100%;
  height: 40px;
  padding-left: 20px;
  margin-bottom: 10px;
  border: 2px solid #973f3f;
  border-radius: 5px;
  font-size: 16px;
  border: 2px solid #b63b3b;
  background-color: rgba(222, 192, 192, 0.8);
}

.login-btn {
  width: 30%;
  margin: 10px;
}

.signup-link{
  text-align: center;
}

.signup-link a{
  color: #007bff;
  text-decoration: none;
}

/* Media queries for responsiveness */
@media screen and (max-width: 480px) {
.login-form {
    max-width: 90%;
  }
}
</style>
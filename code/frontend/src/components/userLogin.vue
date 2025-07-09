<template>
  <div class="login-container">
    <img alt="Shopzee Logo" src="../assets/quiz-logo.png" class="logo" >
    <h2 style="color:black">Login</h2>
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

      <p class="signup-link">Don't have an account? <router-link to="/register">Create one</router-link></p>
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
        password: '',
      },
      show: true,
    };
  },
  created(){document.title='Login';},
  methods: {
    ...mapActions({
        login: 'LOGIN_ACTION'
    }),
 

    onSubmit(event) {
      event.preventDefault();
      let payload = { name: this.form.name, password: this.form.password };
      console.log(payload);
      this.login(payload)
      this.form.email = '';
      this.form.password = '';

    },

    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.name = '';
      this.form.password = '';
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
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
  height: 100vh;
  background-color: #f9f9f9;
  /* Set the background image */
  background-image: url("@/assets/gradient.jpg");
  background-size: cover;
  background-position: center;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5; /* Adjust opacity as desired */
  z-index: -1;
}

.login-form {
  max-width: 400px;
  padding: 20px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 2px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.9); /* Set background color with transparency */
}

.login-input {
  width: 100%;
  height: 40px;
  padding-left: 20px;
  margin-bottom: 30px;
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


.signup-link,
.admin-link {
  text-align: center;
  margin-top: 20px;
}

.signup-link a,
.admin-link a {
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
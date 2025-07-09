<template>
    <div class="landing-page">
      <b-card class="landing-card">
      <img alt="Quiz-Master Logo" src="../assets/quiz-logo.png" class="logo" style="width: 210px; height: 167px;border-radius: 30px; margin:10px;">
      <h1>Quiz Master</h1>
      <h3>Who's using the app?</h3>
      <div>
        <b-button @click="redirectToLogin('admin')" class="role-buttons" type="primary">Admin</b-button>
        <b-button @click="redirectToLogin('user')" class="role-buttons" type="primary">User</b-button>
      </div>
    </b-card>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LandingPage',
    created(){document.title="shopzee-Home";},
    methods: {
      redirectToLogin(role) {
        if (role === 'user') {
          this.$router.push('/login');
        } else if (role === 'admin') {
          this.$router.push('/admin/login');
        }
      },
    },
  };
  </script>
  
  <style scoped>
/* Landing Page Styling */

.landing-page {
  text-align: center;
  padding: 50px;
  align-self: center;
  background: url("@/assets/dark.jpg") center/cover no-repeat; /* Replace with the actual path to your dark.jpeg */
  height: 100vh; /* Ensure the landing page takes up the full viewport height */
  display: flex;
  align-items: center;
  justify-content: center;
}
.landing-card {
  background-color: rgba(255, 255, 255, 0.8); /* Adjust the alpha channel for card transparency */
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
h1 {
  font-size: 36px;
  margin-bottom: 20px;
}

.role-buttons{
  padding: 10px 20px;
  border-radius: 20px;
  margin: 10px;
  font-size: 18px;
  cursor: pointer;
  background-color: lightblue;
  color: black;
}

.role-buttons:hover {
  background-color: #2980b9;
}

</style>
<template>
  <div class="login-container">
  <b-container class="d-flex justify-content-center align-items-center min-vh-100">
    <b-row class="w-100 justify-content-center">
      <b-col md="6" lg="4">
        <div class="text-center">
          <img alt="Quiz Master Logo" src="../assets/quiz-logo.png" class="logo mb-3"
            style="width: 200px; height: 150px; border-radius: 20px;">
        </div>

        <b-card class="p-4 shadow">
          <h3 class="text-center">Admin Login</h3>

          <b-form @submit="onSubmit" @reset="onReset" v-if="show">
            <b-form-group label="Admin Name:" label-for="input-name">
              <b-form-input
                id="input-name"
                v-model="form.name"
                type="text"
                placeholder="Enter name"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group label="Password:" label-for="input-password">
              <b-form-input
                id="input-password"
                v-model="form.password"
                type="password"
                placeholder="Enter password"
                required
              ></b-form-input>
            </b-form-group>

            <b-alert v-if="errorMessage" variant="danger" show>{{ errorMessage }}</b-alert>

            <div class="d-grid gap-2">
              <b-button type="submit" variant="primary" :disabled="loading">
                {{ loading ? "Logging in..." : "Login" }}
              </b-button>
              <b-button type="reset" variant="danger">Reset</b-button>
            </div>

            <p class="text-center mt-3">
              Not an Admin? <router-link to="/">Click here</router-link>
            </p>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      form: {
        name: "",
        password: "",
      },
      show: true,
      loading: false,
      errorMessage: "",
    };
  },
  created() {
    document.title = "Admin Login";
  },
  methods: {
    ...mapActions({
      login: "AdminLOGIN_ACTION",
    }),

    async onSubmit(event) {
      event.preventDefault();
      this.loading = true;
      this.errorMessage = "";

      let payload = {
        name: this.form.name,
        password: this.form.password,
      };

      try {
        await this.login(payload);
      } catch (error) {
        this.errorMessage = "Invalid credentials. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    onReset(event) {
      event.preventDefault();
      this.form.name = "";
      this.form.password = "";
      this.errorMessage = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style scoped>
.min-vh-100 {
  min-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto;
}

.shadow {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
</style>

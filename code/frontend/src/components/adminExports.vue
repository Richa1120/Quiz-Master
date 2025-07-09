<template>
  <div class="export-container">
    <!-- Navbar -->
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/admin/subjects">Subject Management</b-nav-item>
          <b-nav-item to="/admin/chapters">Chapter Management</b-nav-item>
          <b-nav-item to="/admin/quizzes">Quizzes</b-nav-item>
          <b-nav-item to="/admin/users">User Management</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <!-- Export Section -->
    <div class="export-section">
      <h2>Export All Users' Quiz Data</h2>

      <b-button variant="success" @click="exportAdminQuizData" :disabled="isLoading">
        {{ isLoading ? "Exporting..." : "Export All Users' Data" }}
      </b-button>

      <p v-if="downloadReady">
        Export ready: <a :href="downloadLink" download>Download CSV</a>
      </p>

      <b-alert v-if="errorMessage" variant="danger" show>{{ errorMessage }}</b-alert>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      downloadLink: "",
      errorMessage: "",
      isLoading: false,
      downloadReady: false
    };
  },
  methods: {
    async exportAdminQuizData() {
      try {
        this.isLoading = true;

        // Trigger export task
        await axios.post("http://127.0.0.1:5000/admin/export_quiz_data");

        // Simulate processing delay
        setTimeout(() => {
          this.downloadReady = true;
          this.downloadLink = `http://127.0.0.1:5000/admin/download_quiz_data`;
          this.isLoading = false;
        }, 5000);
      } catch (error) {
        this.errorMessage = "Error exporting admin data!";
        this.isLoading = false;
      }
    },
    logout() {
      axios.post("http://127.0.0.1:5000/admin/logout")
        .then(() => {
          localStorage.removeItem("token");
          localStorage.removeItem("usertype");
          this.$router.push("/");
        })
        .catch(error => console.error("Error logging out:", error));
    },
    goToHome() {
      this.$router.push("/admin/dashboard");
    }
  }
};
</script>

<style scoped>
.export-container {
  text-align: center;
  background-image: url('@/assets/dark.jpg');
  background-size: cover;
  min-height: 100vh;
}

.export-section {
  margin-top: 20px;
  padding: 20px;
}

.gradient-nav {
  background-image: url('@/assets/card.jpeg');
  background-size: cover;
  color: white;
}

.navbar-logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
}
</style>

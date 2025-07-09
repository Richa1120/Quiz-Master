<template>
  <div class="admin-dashboard">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-form @submit.prevent="searchContent">
            <b-form-input
              v-model="searchQuery"
              class="search-input"
              placeholder="Search subjects, chapters, quizzes"
            ></b-form-input>
            <b-button type="submit" variant="info" class="search-button">Search</b-button>
          </b-nav-form>
          <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-container fluid>
      <div v-if="searchResults">
        <h2 class="section-title">Search Results</h2>

        <b-row v-if="searchSubjects.length || searchChapters.length || searchQuizzes.length">
          <!-- Subjects -->
          <b-col v-for="subject in searchSubjects" :key="subject.id" md="4" class="search-card">
            <b-card class="search-card-inner">
              <b-card-title>{{ subject.name }}</b-card-title>
              <b-button variant="info" to="/admin/subjects">Manage Subjects</b-button>
            </b-card>
          </b-col>

          <!-- Chapters -->
          <b-col v-for="chapter in searchChapters" :key="chapter.id" md="4" class="search-card">
            <b-card class="search-card-inner">
              <b-card-title>{{ chapter.title }}</b-card-title>
              <b-card-text><strong>Subject:</strong> {{ chapter.subject_name }}</b-card-text>
              <b-button variant="info" to="/admin/chapters">Manage Chapters</b-button>
            </b-card>
          </b-col>

          <!-- Quizzes -->
          <b-col v-for="quiz in searchQuizzes" :key="quiz.id" md="4" class="search-card">
            <b-card class="search-card-inner">
              <b-card-title>{{ quiz.title }}</b-card-title>
              <b-card-text><strong>Chapter:</strong> {{ quiz.chapter_name }}</b-card-text>
              <b-card-text><strong>Chapter:</strong> {{ quiz.subject_name }}</b-card-text>
              <b-button variant="primary" to="/admin/quizzes">Manage Quizzes</b-button>
            </b-card>
          </b-col>
        </b-row>

        <p v-else class="no-data">No results found.</p>
      </div>

      <!-- ✅ Normal Dashboard when NOT searching -->
      <div v-else>
        <b-row>
          <b-col md="4">
            <b-card title="Subjects Management" class="dashboard-card">
              <b-button variant="primary" to="/admin/subjects">Manage Subjects</b-button>
            </b-card>
          </b-col>
          <b-col md="4">
            <b-card title="Chapters Management" class="dashboard-card">
              <b-button variant="primary" to="/admin/chapters">Manage Chapters</b-button>
            </b-card>
          </b-col>
          <b-col md="4">
            <b-card title="Quiz Management" class="dashboard-card">
              <b-button variant="primary" to="/admin/quizzes">Manage Quizzes</b-button>
            </b-card>
          </b-col>
        </b-row>

        <b-row>
          <b-col md="6">
            <b-card title="User Management" class="dashboard-card">
              <b-button variant="primary" to="/admin/users">Manage Users</b-button>
            </b-card>
          </b-col>
          <b-col md="6">
            <b-card title="Summary & Reports" class="dashboard-card">
              <b-button variant="primary" to="/admin/exports">View Reports</b-button>
            </b-card>
          </b-col>
        </b-row>
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchQuery: "",
      searchSubjects: [],
      searchChapters: [],
      searchQuizzes: [],
      searchResults: false
    };
  },
  methods: {
    async searchContent() {
      if (!this.searchQuery.trim()) {
        this.searchSubjects = [];
        this.searchChapters = [];
        this.searchQuizzes = [];
        this.searchResults = false;
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/admin/search", {
          params: { query: this.searchQuery }
        });

        this.searchSubjects = response.data.subjects;
        this.searchChapters = response.data.chapters;
        this.searchQuizzes = response.data.quizzes;
        this.searchResults = true;
      } catch (error) {
        console.error("Error fetching search results:", error);
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
      this.$router.replace("/admin/dashboard");
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 0px;
  background-image: url("@/assets/dark.jpg");
  background-size: cover;
  min-height: 100vh;
}

.gradient-nav {
  background-image: url("@/assets/card.jpeg");
  background-size: cover;
  color: white;
}

.navbar-logo {
  font-size: 24px;
  font-weight: bold;
}

.logout-button {
  border-radius: 20px;
  background-color: #f55;
  color: white;
  font-weight: bold;
}

.dashboard-card {
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* ✅ Search Section */
.search-input {
  margin-right: 10px;
  width: 250px;
}

.search-button {
  border-radius: 5px;
  font-weight: bold;
  background-color: #17a2b8;
  color: white;
}

.search-card {
  margin-bottom: 20px;
  padding: 0 20px;
}

.search-card-inner {
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  padding: 15px;
}

.no-data {
  text-align: center;
  color: white;
  font-weight: bold;
  margin-top: 20px;
}
</style>

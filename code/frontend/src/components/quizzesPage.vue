<template>
    <div class="chapters-page">
      <!-- ✅ Navbar (Same as Dashboard) -->
      <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
        <b-navbar-brand class="navbar-logo">
          <router-link to="/home">Quiz Master</router-link>
        </b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav class="ml-auto">
            <b-button variant="secondary" class="logout-button" @click="logout">Logout</b-button>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
  
      <br />
  
      <!-- ✅ Chapters & Their Quizzes -->
      <b-container fluid>
              <b-row>
                <b-col v-for="quiz in quizzes" :key="quiz.id" md="4" class="quiz-card">
                  <b-card class="quiz-card-inner">
                    <b-card-title>{{ quiz.title }}</b-card-title>
                    <b-card-text>
                      <strong>Duration:</strong> {{ quiz.duration }} minutes
                    </b-card-text>
                    <b-button variant="primary" class="start-quiz-btn" :to="`/user/quiz/${quiz.id}`">
                      Start Quiz
                    </b-button>
                    <p v-if="quizzes.length === 0" class="no-data">No quizzes available</p>
                  </b-card>
                </b-col>
              </b-row>
  
      </b-container>
  
      <!-- ✅ Back Button -->
      <div class="extra-buttons">
        <b-button variant="info" class="nav-btn" @click="$router.push('/home')">Back to Home</b-button>
      </div>
    </div>
  </template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      chapterId: null,
      chapterName: "",
      quizzes: []
    };
  },
  mounted() {
    this.chapterId = this.$route.params.chapterId;
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/user/quizzes/${this.chapterId}`);
        this.quizzes = response.data.quizzes;
      } catch (error) {
        console.error("Error fetching chapters and quizzes:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("user_id");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.chapters-page {
  padding: 20px;
  background-image: url("@/assets/dark.jpg");
  background-size: cover;
  min-height: 100vh;
}

.section-title {
  color: white;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.chapter-section {
  margin-bottom: 20px;
}

.chapter-card {
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  background-color: #ffffff;
}

.chapter-title {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
}

.quiz-card {
  margin: 15px 0;
}

.quiz-card-inner {
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  background-image: url("@/assets/card.jpeg");
  background-size: cover;
  padding: 15px;
}

.start-quiz-btn {
  width: 100%;
  background-color: #007bff;
}

.gradient-nav {
  background-image: url("@/assets/card.jpeg");
  background-size: cover;
}

.logout-button {
  background-color: #f55;
  color: white;
}

.nav-btn {
  margin-top: 20px;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background 0.3s;
}

.nav-btn:hover {
  opacity: 0.8;
}

.no-data {
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}
</style>

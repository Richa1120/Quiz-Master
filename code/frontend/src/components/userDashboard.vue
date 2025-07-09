<template>
  <div class="user-dashboard">
    <!-- ✅ Navbar -->
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo">
        <router-link to="/home">Quiz Master</router-link>
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
        <b-nav-form @submit.prevent>
          <b-form-input
            v-model="searchQuery"
            class="search-input"
            placeholder="Search subjects, chapters, quizzes"
            @input="searchContent"
          ></b-form-input>
        </b-nav-form>
        <b-navbar-nav>
            <b-button variant="success" class="link-btn" @click="goToQuizHistory">View Quiz History</b-button>
            <b-button variant="primary" class="link-btn" @click="goToPerformanceSummary">Performance Summary</b-button>
          </b-navbar-nav>
        <b-button variant="secondary" class="logout-button" @click="logout">Logout</b-button>
      </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <br />

    <!-- ✅ Show Search Results ONLY when there's a search query -->
    <div v-if="searchQuery">
      <h2 class="section-title">Search Results</h2>

      <b-row v-if="searchSubjects.length || searchChapters.length || searchQuizzes.length">
        <!-- Subjects -->
        <b-col v-for="subject in searchSubjects" :key="subject.id" md="4" class="quiz-card">
          <b-card class="quiz-card-inner">
            <b-card-title>{{ subject.name }}</b-card-title>
            <b-button variant="info" class="view-chapters-btn" @click="viewChapters(subject.id)">
              View Chapters
            </b-button>
          </b-card>
        </b-col>

        <!-- Chapters -->
        <b-col v-for="chapter in searchChapters" :key="chapter.id" md="4" class="quiz-card">
          <b-card class="quiz-card-inner">
            <b-card-title>{{ chapter.title }}</b-card-title>
            <b-card-text><strong>Subject:</strong> {{ chapter.subject_name }}</b-card-text>
            <b-button variant="info" class="view-quizzes-btn" @click="viewQuizzes(chapter.id)">
              View Quizzes
            </b-button>
          </b-card>
        </b-col>

        <!-- Quizzes -->
        <b-col v-for="quiz in searchQuizzes" :key="quiz.id" md="4" class="quiz-card">
          <b-card class="quiz-card-inner">
            <b-card-title>{{ quiz.title }}</b-card-title>
            <b-card-text>
              <strong>Chapter:</strong> {{ quiz.chapter_name }}
            </b-card-text>
            <b-button variant="primary" class="start-quiz-btn" :to="`/user/quiz/${quiz.id}`">
              Start Quiz
            </b-button>
          </b-card>
        </b-col>
      </b-row>

      <p v-else class="no-data">No results found.</p>
    </div>

    <!-- ✅ Normal Display when NOT searching -->
    <div v-else>
      <!-- ✅ Subject Cards -->
      <h2 class="section-title">Subjects</h2>
      <b-row v-if="subjects.length > 0">
        <b-col v-for="subject in subjects" :key="subject.id" md="4" class="quiz-card">
          <b-card class="quiz-card-inner">
            <b-card-title>{{ subject.name }}</b-card-title>
            <b-button variant="info" class="view-chapters-btn" @click="viewChapters(subject.id)">
              View Chapters
            </b-button>
          </b-card>
        </b-col>
      </b-row>
      <p v-else class="no-data">No subjects available</p>

      <!-- ✅ Quiz Cards -->
      <h2 class="section-title">Available Quizzes</h2>
      <b-row v-if="quizzes.length > 0">
        <b-col v-for="quiz in quizzes" :key="quiz.id" md="4" class="quiz-card">
          <b-card class="quiz-card-inner">
            <b-card-title>{{ quiz.title }}</b-card-title>
            <b-card-text>
              <strong>Subject:</strong> {{ quiz.subject_name }}<br />
              <strong>Chapter:</strong> {{ quiz.chapter_name || "N/A" }}<br />
              <strong>Duration:</strong> {{ quiz.duration }} minutes
            </b-card-text>
            <b-button variant="primary" class="start-quiz-btn" :to="`/user/quiz/${quiz.id}`">
              Start Quiz
            </b-button>
          </b-card>
        </b-col>
      </b-row>
      <p v-else class="no-data">No quizzes available</p>
    </div>

    <!-- ✅ Extra Buttons -->
    <div class="extra-buttons">
      <b-button variant="info" class="nav-btn" to="/user/quiz-history">View Quiz History</b-button>
      <b-button variant="success" class="nav-btn" to="/user/performance">View Performance Summary</b-button>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  data() {
    return {
      searchQuery: "",
      quizzes: [],
      subjects: [],
      searchSubjects: [],
      searchChapters: [],
      searchQuizzes: [],
      username: localStorage.getItem("username") || "User",
    };
  },
  mounted() {
    this.fetchSubjects();
    this.fetchQuizzes();
    document.title = "User Dashboard";
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/user/subjects");
        this.subjects = response.data;
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },
    async fetchQuizzes() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/user/quizzes");
        this.quizzes = response.data;
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
    async searchContent() {
      if (!this.searchQuery.trim()) {
        this.searchSubjects = [];
        this.searchChapters = [];
        this.searchQuizzes = [];
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/user/search", {
          params: { query: this.searchQuery }
        });

        this.searchSubjects = response.data.subjects;
        this.searchChapters = response.data.chapters;
        this.searchQuizzes = response.data.quizzes;
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    viewChapters(subjectId) {
      this.$router.push(`/user/chapters/${subjectId}`);
    },
    viewQuizzes(chapterId) {
      this.$router.push(`/user/quizzes/${chapterId}`);
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("user_id");
      this.$router.push("/login");
    },
    goToPerformanceSummary() {
      this.$router.push("/user/performance");
    },
    goToQuizHistory() {
      this.$router.push("/user/quiz-history");
    }
  }
};
</script>



<style scoped>
.user-dashboard {
  padding: 20px;
  background-image: url("@/assets/dark.jpg");
  background-size: cover;
  min-height: 100vh;
}

.section-title {
  color: white;
  margin-top: 20px;
  font-weight: bold;
  text-align: center;
}

.link-btn {
  margin: 10px;
  font-weight: bold;
  border-radius: 20px;
}

.quiz-card {
  margin-bottom: 20px;
  padding: 0 20px;
}

.quiz-card-inner {
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgb(0, 0, 0);
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

.navbar-logo {
  font-size: 24px;
  font-weight: bold;
}

.profile-button, .logout-button {
  margin-left: 10px;
  border-radius: 20px;
  font-weight: bold;
}

.logout-button {
  background-color: #f55;
  color: white;
}

.search-input {
  border-radius: 20px;
  padding: 8px 12px;
}

.search-button {
  border-radius: 20px;
  margin-left: 10px;
  background-color: #007bff;
  color: white;
}

.extra-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.nav-btn {
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
  color: white;
  font-weight: bold;
  margin-top: 20px;
}
</style>

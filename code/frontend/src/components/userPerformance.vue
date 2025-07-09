<template>
  <div>
    <!-- Navbar -->
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo">
        <router-link to="/home">Quiz Master</router-link>
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-navbar-nav>
            <b-button variant="primary" class="link-btn" @click="goToHome">Home</b-button>
            <b-button variant="success" class="link-btn" @click="goToQuizHistory">View Quiz History</b-button>
          </b-navbar-nav>
          <b-button variant="secondary" class="logout-button" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <!-- Main Content -->
          <div class="performance-summary">
            <h2>Performance Summary</h2>

            <!-- Subject, Chapter, and Quiz Filters -->
            <div class="filters">
              <b-form-select v-model="selectedSubject" @change="fetchChapters" :options="subjectOptions"></b-form-select>
              <b-form-select v-model="selectedChapter" @change="fetchQuizzes" :options="chapterOptions"></b-form-select>
              <b-form-select v-model="selectedQuiz" @change="fetchPerformanceData" :options="quizOptions"></b-form-select>
            </div>

            <!-- Chart Display -->
            <apexchart
              v-if="chartData.series.length > 0"
              type="line"
              height="300"
              :options="chartOptions"
              :series="chartData.series">
            </apexchart>
            <p v-else>No performance data available</p>
          </div>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      subjectOptions: [{ value: null, text: "Select Subject" }],
      chapterOptions: [{ value: null, text: "Select Chapter" }],
      quizOptions: [{ value: null, text: "Select Quiz" }],
      selectedSubject: null,
      selectedChapter: null,
      selectedQuiz: null,
      chartData: { series: [] },
      chartOptions: {
        chart: { type: "line" },
        xaxis: { categories: [] },
        stroke: { curve: "smooth" },
        title: { text: "Quiz Performance Over Time" }
      },
      searchQuery: ""
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
      async fetchSubjects() {
        try {
          const response = await axios.get("http://127.0.0.1:5000/user/subjects");
          this.subjectOptions = [
            { value: null, text: "Select Subject" },
            ...response.data.map(sub => ({ value: sub.id, text: sub.name }))
          ];
        } catch (error) {
          console.error("Error fetching subjects:", error);
        }
      },

      async fetchChapters() {
        if (!this.selectedSubject) return;
        try {
          const response = await axios.get(`http://127.0.0.1:5000/user/chapters?subject_id=${this.selectedSubject}`);
          this.chapterOptions = [
            { value: null, text: "Select Chapter" },
            ...response.data.map(chap => ({ value: chap.id, text: chap.title }))
          ];
        } catch (error) {
          console.error("Error fetching chapters:", error);
        }
      },

      async fetchQuizzes() {
        if (!this.selectedSubject || !this.selectedChapter) return;
        try {
          const response = await axios.get("http://127.0.0.1:5000/user/quiz", {
            params: {
              subject_id: this.selectedSubject,
              chapter_id: this.selectedChapter
            }
          });

          this.quizOptions = [
            { value: null, text: "Select Quiz" },
            ...response.data.map(quiz => ({ value: quiz.id, text: quiz.title }))
          ];
        } catch (error) {
          console.error("Error fetching quizzes:", error);
        }
      },
      async fetchPerformanceData() {
        const userId = localStorage.getItem("user_id");
        if (!userId || !this.selectedQuiz) return;

        try {
          const response = await axios.get("http://127.0.0.1:5000/user/performance", {
            params: { user_id: userId, quiz_id: this.selectedQuiz }
          });

          this.chartData = {
            series: [{ name: "Score", data: response.data.scores }],
          };

          this.chartOptions = {
            ...this.chartOptions, // Preserve existing chart options
            xaxis: { categories: response.data.dates }, // Set quiz attempt dates
          };
        } catch (error) {
          console.error("Error fetching performance data:", error);
        }
      },
    onSearch(event) {
      event.preventDefault();
    },
    goToHome() {
      this.$router.push("/home");
    },
    goToQuizHistory() {
      this.$router.push("/user/quiz-history");
    },
    logout() {
      const user_id = localStorage.getItem("user_id"); // Retrieve user ID from localStorage

      axios.post("http://127.0.0.1:5000/logout", { user_id })
        .then(() => {
          localStorage.removeItem("token");
          localStorage.removeItem("username");
          localStorage.removeItem("user_id");
          this.$router.push("/login"); // Redirect to login page
        })
        .catch(error => console.error("Error logging out:", error));
    }
  }
};
</script>


<style scoped>
.performance-summary {
  padding: 20px;
  background-image: url("@/assets/dark.jpg");
  background-size: cover;
  min-height: 100vh;
  text-align: center;
}

.gradient-nav {
  background-image: url('@/assets/card.jpeg');
  background-size: cover;
  color: white;
}

.filters {
  margin-bottom: 20px;
}

.section-title {
  color: white;
  font-weight: bold;
}

.no-data {
  text-align: center;
  color: white;
  font-weight: bold;
  margin-top: 20px;
}

.extra-links {
  margin-top: 20px;
}

.link-btn {
  margin: 10px;
  font-weight: bold;
  border-radius: 20px;
}

.logout-button {
  border-radius: 20px;
  background-color: #f55;
  color: white;
  font-weight: bold;
}
</style>

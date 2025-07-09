<template>
  <div class="quiz-history">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo">
        <router-link to="/home">Quiz Master</router-link>
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-navbar-nav>
            <b-button variant="primary" class="link-btn" @click="goToHome">Home</b-button>
            <b-button variant="success" class="link-btn" @click="goToPerformanceSummary">View Performance Summary</b-button>
          </b-navbar-nav>
          <b-button variant="secondary" class="logout-button" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <h2 class="section-title">Your Quiz History</h2>
    <b-table striped hover :items="filteredQuizHistory" :fields="quizFields"></b-table>
    <p v-if="quizHistory.length === 0" class="no-data">No quiz history available</p>

    <!-- ✅ Export Button & Download Link -->
    <div class="export-section">
      <b-button variant="info" class="export-btn" @click="exportUserQuizData" :disabled="isLoading">
        {{ isLoading ? "Exporting..." : "Export My Quiz Data" }}
      </b-button>

      <p v-if="downloadLink">
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
      quizHistory: [],
      searchQuery: "",
      quizFields: [
        { key: "quiz_name", label: "Quiz" },
        { key: "subject", label: "Subject" },
        { key: "chapter_name", label: "Chapter" },
        { key: "score", label: "Score" },
        { key: "attempt_date", label: "Attempt Date" }
      ],
      downloadLink: "",
      errorMessage: "",
      isLoading: false
    };
  },
  computed: {
    filteredQuizHistory() {
      if (!this.searchQuery) return this.quizHistory;
      const query = this.searchQuery.toLowerCase();
      return this.quizHistory.filter(
        quiz =>
          quiz.quiz_name.toLowerCase().includes(query) ||
          quiz.subject.toLowerCase().includes(query) ||
          quiz.chapter_name.toLowerCase().includes(query)
      );
    }
  },
  mounted() {
    this.fetchQuizHistory();
  },
  methods: {
    fetchQuizHistory() {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        console.error("User ID is missing.");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/user/quiz-history?user_id=${userId}`)
        .then(response => {
          this.quizHistory = response.data;
        })
        .catch(error => console.error("Error fetching quiz history:", error));
    },
    onSearch(event) {
      event.preventDefault();
    },
    logout() {
      const user_id = localStorage.getItem("user_id");

      axios.post("http://127.0.0.1:5000/logout", { user_id })
        .then(() => {
          localStorage.removeItem("token");
          localStorage.removeItem("username");
          localStorage.removeItem("user_id");
          this.$router.push("/login");
        })
        .catch(error => console.error("Error logging out:", error));
    },
    goToHome() {
      this.$router.push("/home");
    },
    goToPerformanceSummary() {
      this.$router.push("/user/performance");
    },

    // ✅ EXPORT FUNCTION
    async exportUserQuizData() {
      try {
        this.isLoading = true;
        const userId = localStorage.getItem("user_id");

        // Start export
        await axios.post("http://127.0.0.1:5000/user/export_quiz_data", { user_id: userId });

        // Poll for download link
        this.pollForDownload(userId);
      } catch (error) {
        this.errorMessage = "Error exporting quiz data!";
        this.isLoading = false;
      }
    },

    async pollForDownload(userId) {
      console.log("⏳ Polling export status..."); // Debug log
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/export/status/${userId}`);
          console.log("📌 Poll Response:", response.data); // Debugging API response

          if (response.data.filename) {
            console.log("✅ Export is ready! Stopping poll.");
            
            this.downloadLink = `http://127.0.0.1:5000/user/download_quiz_data/${userId}`;
            clearInterval(interval); // Stop polling ✅
            this.isLoading = false;
          }
        } catch (error) {
          console.error("🚨 Polling error:", error);
          clearInterval(interval); // Stop on error
          this.isLoading = false;
        }
      }, 3000); // Poll every 3 seconds
    }
  }
};
</script>

<style scoped>
.quiz-history {
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

.export-section {
  margin-top: 20px;
}

.export-btn {
  margin-top: 10px;
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

.profile-button {
  margin-left: 10px;
  border-radius: 20px;
  font-weight: bold;
}
</style>

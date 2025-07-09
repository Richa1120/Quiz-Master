<template>
  <div class="admin-dashboard">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/admin/subjects">Subject Management</b-nav-item>
          <b-nav-item to="/admin/quizzes">Quiz Management</b-nav-item>
          <b-nav-item to="/admin/chapters">Chapter Management</b-nav-item>
          <b-nav-item to="/admin/exports">Reports</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-container fluid>
      <h2 class="text-center text-white mt-4">Manage Users</h2>

      <b-row class="justify-content-center">
        <b-col md="8">
          <b-card title="User List" class="dashboard-card">
            <b-table striped hover :items="users" :fields="fields">
              <template #cell(actions)="row">
                <b-button @click="viewAttempts(row.item.id)" variant="info" size="sm" class="mr-2">
                  View Attempts
                </b-button>
              </template>
            </b-table>
          </b-card>
        </b-col>
      </b-row>

      <!-- Quiz Attempts Modal -->
      <b-modal v-model="showAttemptsModal" title="User Quiz Attempts" hide-footer size="xl" centered>
      <b-container>
        <b-table striped hover :items="quizAttempts" :fields="attemptFields" class="text-center">
          <template #cell(subject_name)="row">
            <strong>{{ row.item.subject_name }}</strong>
          </template>

          <template #cell(chapter_name)="row">
            <span>{{ row.item.chapter_name }}</span>
          </template>

          <template #cell(quiz_name)="row">
            <span class="quiz-name">{{ row.item.quiz_name }}</span>
          </template>

          <template #cell(score)="row">
            <b-badge variant="success" class="score-badge">{{ row.item.score }}</b-badge>
          </template>

          <template #cell(attempt_time)="row">
            {{ formatDate(row.item.attempt_time) }}
          </template>

          <template #cell(attempt_count)="row">
            {{ row.item.attempt_count }}
          </template>
        </b-table>
      </b-container>
      <b-button variant="secondary" block @click="showAttemptsModal = false">Close</b-button>
      </b-modal>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      users: [],
      quizAttempts: [],
      showAttemptsModal: false,
      fields: [
        { key: "id", label: "ID" },
        { key: "name", label: "Username" },
        { key: "email", label: "Email" },
        { key: "actions", label: "Actions" }
      ],
      attemptFields: [
        { key: "subject_name", label: "Subject" },
        { key: "chapter_name", label: "Chapter" },
        { key: "quiz_name", label: "Quiz" },
        { key: "score", label: "Score" },
        { key: "attempt_date", label: "Date" },
        { key: "duration", label: "Duration" },
        { key: "attempt_count", label: "Attempts" }
      ]
    };
  },
  methods: {
    ...mapActions({
      signOut: "LOGOUT_ACTION"
    }),
    goToHome() {
      this.$router.push("/admin/dashboard");
    },
    logout() {
      this.signOut();
    },
    fetchUsers() {
      axios.get("http://127.0.0.1:5000/admin/users")
        .then(response => {
          this.users = response.data;
        })
        .catch(error => console.error("Error fetching users:", error));
    },
    viewAttempts(userId) {
      axios.get(`http://127.0.0.1:5000/admin/users/${userId}/attempts`)
        .then(response => {
          this.quizAttempts = response.data;
          this.showAttemptsModal = true;
        })
        .catch(error => console.error("Error fetching attempts:", error));
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString();
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 0px;
  background-image: url('@/assets/dark.jpg');
  background-size: cover;
  min-height: 100vh;
}

.gradient-nav {
  background-image: url('@/assets/card.jpeg');
  background-size: cover;
  color: white;
}

.navbar-logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer; /* Makes it look clickable */
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

.b-table {
  text-align: center;
}

.score-badge {
  font-size: 14px;
  padding: 5px 10px;
}

.b-table th,
.b-table td {
  vertical-align: middle !important;
}

.b-table td {
  white-space: nowrap;
  text-align: center;
}

.quiz-name {
  white-space: nowrap; /* Prevents wrapping */
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px; /* Adjust width if needed */
  display: inline-block;
}
</style>

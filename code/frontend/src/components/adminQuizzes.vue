<template>
  <div class="admin-dashboard">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/admin/subjects" active>Subject Management</b-nav-item>
          <b-nav-item to="/admin/chapters">Chapter Management</b-nav-item>
          <b-nav-item to="/admin/users">User Management</b-nav-item>
          <b-nav-item to="/admin/exports">Reports</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-container fluid>
      <h2 class="text-center text-white mt-4">Manage Quizzes</h2>

      <!-- Add/Edit Quiz Form -->
      <b-row class="justify-content-center">
        <b-col md="6">
          <b-card :title="editMode ? 'Edit Quiz' : 'Add New Quiz'" class="dashboard-card">
            <b-form @submit.prevent="editMode ? updateQuiz() : addQuiz()">
              <b-form-group label="Quiz Title">
                <b-input v-model="newQuiz.title" placeholder="Enter Quiz Title" required></b-input>
              </b-form-group>

              <!-- Subject Dropdown -->
              <b-form-group label="Select Subject">
                <b-form-select 
                  v-model="newQuiz.subject_id" 
                  :options="subjects" 
                  value-field="id" 
                  text-field="name"
                  @change="fetchChapters(newQuiz.subject_id)"
                  required
                ></b-form-select>
              </b-form-group>

              <!-- Chapter Dropdown -->
              <b-form-group label="Select Chapter">
                <b-form-select 
                  v-model="newQuiz.chapter_id" 
                  :options="chapters" 
                  value-field="id" 
                  text-field="name"
                  :disabled="!newQuiz.subject_id || chapters.length === 0"
                  required
                ></b-form-select>
              </b-form-group>

              <b-form-group label="Total Marks">
                <b-input v-model="newQuiz.total_marks" type="number" placeholder="Enter Total Marks" required></b-input>
              </b-form-group>

              <b-form-group label="Duration (minutes)">
                <b-input v-model="newQuiz.duration" type="number" placeholder="Enter Duration" required></b-input>
              </b-form-group>

              <b-button type="submit" variant="primary" class="mt-2">
                {{ editMode ? "Update Quiz" : "Add Quiz" }}
              </b-button>
              <b-button v-if="editMode" variant="warning" class="mt-2 ml-2" @click="cancelEdit">Cancel</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>

      <!-- Quiz List -->
      <b-row v-if="quizzes.length > 0" class="justify-content-center">
        <b-col md="8">
          <b-card title="Quiz List" class="dashboard-card">
            
            <!-- Filter Dropdown (Copied from adminChapters) -->
            <b-form-group label="Filter by Subject">
              <b-form-select v-model="selectedSubjectFilter" :options="subjectOptions"></b-form-select>
              <b-form-select v-model="selectedChapterFilter" :options="chapterOptions"></b-form-select>
            </b-form-group>

            <b-list-group>
              <b-list-group-item v-for="quiz in filteredQuizzes" :key="quiz.id" class="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ quiz.title }}</strong> ({{ quiz.subject_name }} - {{ quiz.chapter_name }})
                  - {{ quiz.total_marks }} Marks - {{ quiz.duration }} mins
                </div>
                <div>
                  <b-button @click="editQuiz(quiz)" variant="info" size="sm" class="mr-2">Edit</b-button>
                  <b-button @click="deleteQuiz(quiz.id)" variant="danger" size="sm">Delete</b-button>
                  <b-button @click="manageQuestions(quiz.id)" variant="secondary" size="sm">Manage Questions</b-button>
                </div>
              </b-list-group-item>
            </b-list-group>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      quizzes: [],
      subjects: [],
      chapters: [],
      selectedSubjectFilter: null,
      selectedChapterFilter: null,
      newQuiz: { id: null, title: "", subject_id: "", chapter_id: "", total_marks: "", duration: "" },
      editMode: false
    };
  },

  computed: {
    subjectOptions() {
      return [{ value: null, text: "All Subjects" }, ...this.subjects.map(s => ({ value: s.id, text: s.name }))];
    },
    chapterOptions() {
      const filteredChapters = this.chapters.filter(chapter => chapter.subject_id === this.selectedSubjectFilter);
      return [{ value: null, text: "All Chapters" }, ...filteredChapters.map(c => ({ value: c.id, text: c.title }))];
    },
    filteredQuizzes() {
      return this.selectedSubjectFilter
        ? this.quizzes.filter(quiz =>
          (!this.selectedSubjectFilter || quiz.subject_id === this.selectedSubjectFilter) &&
          (!this.selectedChapterFilter || quiz.chapter_id === this.selectedChapterFilter)
        )
        : this.quizzes;
    }
  },
  
  methods: {
    ...mapActions({
      signOut: "LOGOUT_ACTION"
    }),
    goToHome() {
      this.$router.push("/admin/dashboard");
    },
    logout() {
      axios.post("http://127.0.0.1:5000/admin/logout")
      .then(() => {
          localStorage.removeItem("token");
          localStorage.removeItem("usertype");
          this.$router.push("/"); // Redirect to login page
        })
        .catch(error => console.error("Error logging out:", error));
    },

    async fetchData() {
      try {
        console.log("Fetching subjects...");
        await this.fetchSubjects();
        console.log("Subjects loaded:", this.subjects);

        console.log("Fetching chapters...");
        await this.fetchAllChapters();
        console.log("Chapters loaded:", this.chapters);

        console.log("Fetching quizzes...");
        await this.fetchQuizzes();
        console.log("Quizzes loaded:", this.quizzes);
      } catch (error) {
        console.error("Error in fetchData:", error);
      }
    },

    async fetchQuizzes() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/admin/quizzes");
        console.log("Raw quizzes:", response.data);

        this.quizzes = response.data.map(quiz => {
          const subject = this.subjects.find(sub => sub.id === quiz.subject_id) || { name: "Unknown" };
          const chapter = this.chapters.find(chap => chap.id === quiz.chapter_id) || { name: "Unknown" };

          return {
            ...quiz,
            subject_name: subject.name,
            chapter_name: chapter.title
          };
        });

        console.log("Processed quizzes:", this.quizzes);
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },

    async fetchSubjects() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/admin/subjects");
        this.subjects = response.data;
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },

    async fetchAllChapters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/admin/chapters");
        this.chapters = response.data;
      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },

    fetchChapters(subjectId) {
      if (!subjectId) {
        this.chapters = [];
        return;
      }

      axios.get(`http://127.0.0.1:5000/admin/subjects/${subjectId}/chapters`)
        .then(response => {
          this.chapters = response.data;
        })
        .catch(error => { console.error("Error fetching chapters:", error); });
    },

    addQuiz() {
      axios.post("http://127.0.0.1:5000/admin/quizzes", this.newQuiz)
        .then(() => {
          this.fetchQuizzes();
          this.resetForm();
        })
        .catch(error => { console.error("Error adding quiz:", error); });
    },

    editQuiz(quiz) {
      this.newQuiz = { ...quiz };
      this.editMode = true;
      this.fetchChapters(quiz.subject_id);
    },

    updateQuiz() {
      axios.put(`http://127.0.0.1:5000/admin/quizzes/${this.newQuiz.id}`, this.newQuiz)
        .then(() => {
          this.fetchQuizzes();
          this.resetForm();
          this.editMode = false;
        })
        .catch(error => { console.error("Error updating quiz:", error); });
    },

    deleteQuiz(id) {
      axios.delete(`http://127.0.0.1:5000/admin/quizzes/${id}`)
        .then(() => this.fetchQuizzes())
        .catch(error => { console.error("Error deleting quiz:", error); });
    },

    cancelEdit() {
      this.resetForm();
      this.editMode = false;
    },

    resetForm() {
      this.newQuiz = { id: null, title: "", subject_id: "", chapter_id: "", total_marks: "", duration: "" };
      this.chapters = [];
    },

    manageQuestions(quizId) {
      this.$router.push(`/admin/quiz/${quizId}/questions`);
    }
  },

  async mounted() {
    await this.fetchData();
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

.dashboard-card {
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
}

.navbar-logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
}

.logout-button {
  border-radius: 20px;
  background-color: #f55;
  color: white;
  font-weight: bold;
}
</style>

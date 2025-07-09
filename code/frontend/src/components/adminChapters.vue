<template>
  <div class="admin-dashboard">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/admin/subjects">Subject Management</b-nav-item>
          <b-nav-item to="/admin/quizzes">Quiz Management</b-nav-item>
          <b-nav-item to="/admin/users">User Management</b-nav-item>
          <b-nav-item to="/admin/reports">Reports</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-container fluid>
      <h2 class="text-center text-white mt-4">Manage Chapters</h2>

      <b-row class="justify-content-center">
        <b-col md="6">
          <b-card title="Add New Chapter" class="dashboard-card">
            <b-form @submit.prevent="addChapter">
              <b-form-group label="Select Subject">
                <b-form-select v-model="selectedSubject" :options="subjectOptions" required></b-form-select>
              </b-form-group>

              <b-form-group label="Chapter Name">
                <b-input v-model="newChapter.title" placeholder="Enter chapter name" required></b-input>
              </b-form-group>

              <b-form-group label="Description (Optional)">
                <b-input v-model="newChapter.description" placeholder="Enter chapter description"></b-input>
              </b-form-group>

              <b-button type="submit" variant="primary" class="mt-2">Add Chapter</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>

      <b-row v-if="chapters.length > 0" class="justify-content-center">
        <b-col md="8">
          <b-card title="Chapters List" class="dashboard-card">
            <b-form-group label="Filter by Subject">
              <b-form-select v-model="selectedSubjectFilter" :options="subjectOptions"></b-form-select>
            </b-form-group>

            <b-list-group>
              <b-list-group-item v-for="chapter in filteredChapters" :key="chapter.id" class="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ chapter.title }}</strong> - {{ chapter.description || "No description" }}
                  <b-badge variant="info" class="ml-2">{{ getSubjectName(chapter.subject_id) }}</b-badge>
                </div>
                <div>
                  <b-button @click="editChapter(chapter)" variant="warning" size="sm" class="mr-2">Edit</b-button>
                  <b-button @click="deleteChapter(chapter.id)" variant="danger" size="sm">Delete</b-button>
                </div>
              </b-list-group-item>
            </b-list-group>
          </b-card>
        </b-col>
      </b-row>
    </b-container>

    <!-- Edit Chapter Modal -->
    <b-modal v-model="showEditModal" title="Edit Chapter" hide-footer>
      <b-form @submit.prevent="updateChapter">
        <b-form-group label="Chapter Name">
          <b-input v-model="editChapterData.title" required></b-input>
        </b-form-group>

        <b-form-group label="Description">
          <b-input v-model="editChapterData.description"></b-input>
        </b-form-group>

        <b-form-group label="Select Subject">
          <b-form-select v-model="editChapterData.subject_id" :options="subjectOptions" required></b-form-select>
        </b-form-group>

        <b-button type="submit" variant="success">Save Changes</b-button>
        <b-button variant="secondary" class="ml-2" @click="showEditModal = false">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      chapters: [],
      subjects: [],
      selectedSubject: null,
      selectedSubjectFilter: null,
      newChapter: { title: "", description: "", subject_id: null },
      searchQuery: "",
      showEditModal: false,
      editChapterData: { id: null, title: "", description: "", subject_id: null },
    };
  },
  computed: {
    subjectOptions() {
      return [{ value: null, text: "Select a Subject" }, ...this.subjects.map(s => ({ value: s.id, text: s.name }))];
    },
    filteredChapters() {
      let filtered = this.selectedSubjectFilter
        ? this.chapters.filter(chapter => chapter.subject_id === this.selectedSubjectFilter)
        : this.chapters;

      if (this.searchQuery) {
        filtered = filtered.filter(chapter =>
          chapter.title.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      return filtered;
    },
  },
  methods: {
    ...mapActions({
      signOut: "LOGOUT_ACTION",
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
    fetchChapters() {
      axios.get("http://127.0.0.1:5000/admin/chapters")
        .then(response => {
          this.chapters = response.data;
        })
        .catch(error => console.error("Error fetching chapters:", error));
    },
    fetchSubjects() {
      axios.get("http://127.0.0.1:5000/admin/subjects")
        .then(response => {
          this.subjects = response.data;
        })
        .catch(error => console.error("Error fetching subjects:", error));
    },
    addChapter() {
      if (!this.selectedSubject) {
        alert("Please select a subject!");
        return;
      }

      axios.post("http://127.0.0.1:5000/admin/chapters", {
        title: this.newChapter.title,
        description: this.newChapter.description,
        subject_id: this.selectedSubject,
      }).then(() => {
        this.fetchChapters();
        this.newChapter = { title: "", description: "", subject_id: null };
      }).catch(error => console.error("Error adding chapter:", error));
    },
    editChapter(chapter) {
      this.editChapterData = { ...chapter };
      this.showEditModal = true;
    },
    updateChapter() {
      axios.put(`http://127.0.0.1:5000/admin/chapters/${this.editChapterData.id}`, {
        title: this.editChapterData.title,
        description: this.editChapterData.description,
        subject_id: this.editChapterData.subject_id,
      })
        .then(() => {
          this.fetchChapters();
          this.showEditModal = false;
        })
        .catch(error => console.error("Error updating chapter:", error));
    },
    deleteChapter(id) {
      axios.delete(`http://127.0.0.1:5000/admin/chapters/${id}`)
        .then(() => this.fetchChapters())
        .catch(error => console.error("Error deleting chapter:", error));
    },
    getSubjectName(subject_id) {
      const subject = this.subjects.find(s => s.id === subject_id);
      return subject ? subject.name : "Unknown";
    },
  },
  mounted() {
    this.fetchSubjects();
    this.fetchChapters();

    const subjectId = this.$route.query.subject;
    if (subjectId) {
      this.selectedSubjectFilter = parseInt(subjectId);
    }
  },
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
  cursor: pointer;
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
</style>

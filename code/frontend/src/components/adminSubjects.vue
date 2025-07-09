<template>
  <div class="admin-dashboard">
    <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
      <!-- Clickable Navbar Logo -->
      <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!-- Navigation Links -->
          <b-nav-item to="/admin/quizzes">Quiz Management</b-nav-item>
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
      <h2 class="text-center text-white mt-4">Manage Subjects</h2>

      <b-row class="justify-content-center">
        <b-col md="6">
          <b-card :title="editMode ? 'Edit Subject' : 'Add New Subject'" class="dashboard-card">
            <b-form @submit.prevent="editMode ? updateSubject() : addSubject()">
              <b-input v-model="newSubject.name" placeholder="Enter subject name" required></b-input>
              <b-input v-model="newSubject.description" placeholder="Enter subject description" required class="mt-2"></b-input>
              <b-button type="submit" variant="primary" class="mt-2">
                {{ editMode ? "Update Subject" : "Add Subject" }}
              </b-button>
              <b-button v-if="editMode" variant="warning" class="mt-2 ml-2" @click="cancelEdit">Cancel</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>

      <b-row v-if="subjects.length > 0" class="justify-content-center">
        <b-col md="8">
          <b-card title="Subject List" class="dashboard-card">
            <b-list-group>
              <b-list-group-item v-for="subject in subjects" :key="subject.id" class="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ subject.name }}</strong> - {{ subject.description }}
                </div>
                <div>
                  <b-button @click="editSubject(subject)" variant="info" size="sm" class="mr-2">Edit</b-button>
                  <b-button @click="deleteSubject(subject.id)" variant="danger" size="sm">Delete</b-button>
                  <b-button @click="viewChapters(subject.id)" variant="success" size="sm" class="ml-2">View Chapters</b-button>
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
      subjects: [],
      newSubject: { id: null, name: "", description: "" },
      editMode: false
    };
  },
  methods: {
    viewChapters(subjectId) {
      this.$router.push({ path: "/admin/chapters", query: { subject: subjectId } });
    },
    ...mapActions({
      signOut: "LOGOUT_ACTION"
    }),
    goToHome() {
      this.$router.push("/admin/dashboard"); // Redirect to home page
    },
    logout() {
      this.signOut();
    },
    fetchSubjects() {
      axios.get("http://127.0.0.1:5000/admin/subjects")
        .then(response => {
          this.subjects = response.data;
        })
        .catch(error => {
          console.error("Error fetching subjects:", error);
        });
    },
    addSubject() {
      axios.post("http://127.0.0.1:5000/admin/subjects", this.newSubject)
        .then(() => {
          this.fetchSubjects();
          this.newSubject = { id: null, name: "", description: "" };
        })
        .catch(error => {
          console.error("Error adding subject:", error);
        });
    },
    editSubject(subject) {
      this.newSubject = { ...subject };
      this.editMode = true;
    },
    updateSubject() {
      axios.put(`http://127.0.0.1:5000/admin/subjects/${this.newSubject.id}`, this.newSubject)
        .then(() => {
          this.fetchSubjects();
          this.newSubject = { id: null, name: "", description: "" };
          this.editMode = false;
        })
        .catch(error => {
          console.error("Error updating subject:", error);
        });
    },
    deleteSubject(id) {
      axios.delete(`http://127.0.0.1:5000/admin/subjects/${id}`)
        .then(() => this.fetchSubjects())
        .catch(error => {
          console.error("Error deleting subject:", error);
        });
    },
    cancelEdit() {
      this.newSubject = { id: null, name: "", description: "" };
      this.editMode = false;
    }
  },
  mounted() {
    this.fetchSubjects();
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
</style>

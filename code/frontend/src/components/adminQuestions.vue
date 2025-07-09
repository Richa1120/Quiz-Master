<template>
    <div class="admin-dashboard">
      <b-navbar toggleable="lg" type="light" variant="dark" class="gradient-nav">
        <b-navbar-brand class="navbar-logo" @click="goToHome">Quiz Master - Admin</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/admin/subjects">Subject Management</b-nav-item>
            <b-nav-item to="/admin/chapters">Chapter Management</b-nav-item>
            <b-nav-item to="/admin/quizzes">Quiz Management</b-nav-item>
            <b-nav-item to="/admin/users">User Management</b-nav-item>
            <b-nav-item to="/admin/exports">Reports</b-nav-item>
          </b-navbar-nav>
  
          <b-navbar-nav class="ml-auto">
            <b-button variant="secondary" class="logout-button" size="sm" @click="logout">Logout</b-button>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
  
      <b-container fluid>
        <h2 class="text-center text-white mt-4">Manage Questions for {{ quizTitle }}</h2>
  
        <!-- Add/Edit Question Form -->
        <b-row class="justify-content-center">
          <b-col md="8">
            <b-card :title="editMode ? 'Edit Question' : 'Add New Question'" class="dashboard-card">
              <b-form @submit.prevent="editMode ? updateQuestion() : addQuestion()">
                <b-form-group label="Question Text">
                  <b-textarea v-model="newQuestion.text" placeholder="Enter question" required></b-textarea>
                </b-form-group>
  
                <b-form-group label="Option A">
                  <b-input v-model="newQuestion.option_a" placeholder="Enter option A" required></b-input>
                </b-form-group>
  
                <b-form-group label="Option B">
                  <b-input v-model="newQuestion.option_b" placeholder="Enter option B" required></b-input>
                </b-form-group>
  
                <b-form-group label="Option C">
                  <b-input v-model="newQuestion.option_c" placeholder="Enter option C" required></b-input>
                </b-form-group>
  
                <b-form-group label="Option D">
                  <b-input v-model="newQuestion.option_d" placeholder="Enter option D" required></b-input>
                </b-form-group>
  
                <b-form-group label="Correct Option">
                  <b-form-select v-model="newQuestion.correct_option" :options="correctOptions" required></b-form-select>
                </b-form-group>
  
                <b-form-group label="Marks">
                  <b-input v-model="newQuestion.marks" type="number" placeholder="Enter marks" required></b-input>
                </b-form-group>
  
                <b-button type="submit" variant="primary" class="mt-2">
                  {{ editMode ? "Update Question" : "Add Question" }}
                </b-button>
                <b-button v-if="editMode" variant="warning" class="mt-2 ml-2" @click="cancelEdit">Cancel</b-button>
              </b-form>
            </b-card>
          </b-col>
        </b-row>
  
        <!-- Question List -->
        <b-row v-if="questions.length > 0" class="justify-content-center">
          <b-col md="8">
            <b-card title="Question List" class="dashboard-card">
              <b-list-group>
                <b-list-group-item v-for="question in questions" :key="question.id" class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ question.text }}</strong> ({{ question.marks }} Marks)
                    <br />
                    A: {{ question.option_a }} | B: {{ question.option_b }} | C: {{ question.option_c }} | D: {{ question.option_d }}
                    <br />
                    <b>Correct Option:</b> {{ question.correct_option.toUpperCase() }}
                  </div>
                  <div>
                    <b-button @click="editQuestion(question)" variant="info" size="sm" class="mr-2">Edit</b-button>
                    <b-button @click="deleteQuestion(question.id)" variant="danger" size="sm">Delete</b-button>
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
        questions: [],
        quizTitle: "",
        newQuestion: {
          id: null,
          text: "",
          option_a: "",
          option_b: "",
          option_c: "",
          option_d: "",
          correct_option: "",
          marks: "",
        },
        editMode: false,
        quizId: null, // Store quizId
        correctOptions: [
          { value: "a", text: "Option A" },
          { value: "b", text: "Option B" },
          { value: "c", text: "Option C" },
          { value: "d", text: "Option D" },
        ],
      };
    },
    methods: {
      ...mapActions({ signOut: "LOGOUT_ACTION" }),
      
      goToHome() {
        this.$router.push("/admin/dashboard");
      },
      
      logout() {
        this.signOut();
      },
  
      fetchQuestions() {
        if (!this.quizId) {
          console.error("Quiz ID is missing in route parameters");
          alert("Error: Quiz ID is missing!");
          return;
        }
  
        axios.get(`http://127.0.0.1:5000/admin/quiz/${this.quizId}/questions`)
          .then(response => {
            this.questions = response.data.questions;
            this.quizTitle = response.data.quiz_title;
          })
          .catch(error => { 
            console.error("Error fetching questions:", error);
            alert("Error fetching questions. Please try again.");
          });
      },
  
      addQuestion() {
        if (!this.quizId) return;
  
        axios.post(`http://127.0.0.1:5000/admin/quiz/${this.quizId}/questions`, this.newQuestion)
          .then(() => {
            this.fetchQuestions();
            this.resetForm();
          })
          .catch(error => { 
            console.error("Error adding question:", error);
            alert("Failed to add question.");
          });
      },
  
      editQuestion(question) {
        this.newQuestion = { ...question };
        this.editMode = true;
      },
  
      updateQuestion() {
        axios.put(`http://127.0.0.1:5000/admin/questions/${this.newQuestion.id}`, this.newQuestion)
          .then(() => {
            this.fetchQuestions();
            this.resetForm();
            this.editMode = false;
          })
          .catch(error => { 
            console.error("Error updating question:", error);
            alert("Failed to update question.");
          });
      },
  
      deleteQuestion(id) {
        axios.delete(`http://127.0.0.1:5000/admin/questions/${id}`)
          .then(() => this.fetchQuestions())
          .catch(error => { 
            console.error("Error deleting question:", error);
            alert("Failed to delete question.");
          });
      },
  
      cancelEdit() {
        this.resetForm();
        this.editMode = false;
      },
  
      resetForm() {
        this.newQuestion = { id: null, text: "", option_a: "", option_b: "", option_c: "", option_d: "", correct_option: "", marks: "" };
      }
    },
  
    mounted() {
      this.quizId = this.$route.params.quizId; // Correct extraction of quizId
      if (!this.quizId) {
        console.error("Quiz ID is missing in route parameters");
        alert("Error: No quiz ID found!");
      } else {
        this.fetchQuestions();
      }
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
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
            <b-button variant="success" class="link-btn" @click="goToQuizHistory">View Quiz History</b-button>
            <b-button variant="success" class="link-btn" @click="goToPerformanceSummary">View Performance Summary</b-button>
          </b-navbar-nav>
          <b-button variant="secondary" class="logout-button" @click="logout">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  
      <b-container class="mt-4">
        <b-row>
          <b-col md="8" class="mx-auto">
            <b-card no-body class="shadow-sm">
              <b-card-header class="bg-primary text-white text-center">
                <h3>{{ quizTitle }}</h3>
                <p><strong>Duration:</strong> {{ quizDuration }} mins</p>
              </b-card-header>
  
              <b-card-body>
                <div v-if="questions.length">
                  <b-list-group>
                    <b-list-group-item v-for="(question, index) in questions" :key="question.id">
                      <p><strong>Q{{ index + 1 }}:</strong> {{ question.text }}</p>
                      <b-form-group>
                        <b-form-radio v-for="(option, key) in question.options"
                          :key="key"
                          v-model="userAnswers[question.id]"
                          :value="key">
                          {{ option }}
                        </b-form-radio>
                      </b-form-group>
                    </b-list-group-item>
                  </b-list-group>
  
                  <b-button variant="success" class="mt-3" block @click="submitQuiz">
                    Submit Quiz
                  </b-button>
                </div>
  
                <b-alert v-else variant="danger" show>No questions available.</b-alert>
              </b-card-body>
            </b-card>
  
            <b-card v-if="showResults" class="mt-4 shadow-sm">
              <b-card-header class="bg-success text-white text-center">
                <h4>Quiz Results</h4>
              </b-card-header>
              <b-card-body>
                <p><strong>Score:</strong> {{ score }} / {{ totalMarks }}</p>
                <p><strong>Time Taken:</strong> {{ timeTaken }} seconds</p>

                <b-list-group>
                  <b-list-group-item v-for="(question, index) in questions" :key="question.id">
                    <p><strong>Q{{ index + 1 }}:</strong> {{ question.text }}</p>

                    <p>
                      <strong>Your Answer:</strong>
                      <span :class="{ 'text-success': userAnswers[question.id] === correctAnswers[question.id],
                                      'text-danger': userAnswers[question.id] !== correctAnswers[question.id] }">
                        {{ question.options[userAnswers[question.id]] || "Not Answered" }}
                      </span>
                    </p>
                    <p><strong>Correct Answer:</strong> {{ question.options[correctAnswers[question.id]] }}</p>
                  </b-list-group-item>
                </b-list-group>
              </b-card-body>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
      <br>
      <b-button variant="primary" class="link-btn" @click="goToHome">Home</b-button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        quizTitle: "",
        quizDuration: 0,
        questions: [],
        userAnswers: {},
        correctAnswers: {},
        score: 0,
        totalMarks: 0,
        showResults: false
      };
    },
    mounted() {
      this.fetchQuizQuestions();
    },
    methods: {
      fetchQuizQuestions() {
        const quizId = this.$route.params.quizId;

        axios.get(`http://127.0.0.1:5000/user/quiz/${quizId}`, {
            headers: { Authorization: localStorage.getItem("token") }
        })
        .then(response => {
            this.quizTitle = response.data.title;
            this.quizDuration = response.data.duration;
            this.startTime = Date.now();  // Store quiz start time
            this.questions = response.data.questions.map(q => ({
                id: q.id,
                text: q.text,
                options: {
                    a: q.option_a,
                    b: q.option_b,
                    c: q.option_c,
                    d: q.option_d
                }
            }));
        })
        .catch(error => console.error("Error fetching questions:", error));
    },
    submitQuiz() {
      const quizId = this.$route.params.quizId;
      const userId = localStorage.getItem("user_id");
      const duration = Math.floor((Date.now() - this.startTime) / 1000); // Calculate time taken

      if (!userId) {
        console.error("User ID is missing!");
        return;
      }

      axios.post(`http://127.0.0.1:5000/user/quiz/${quizId}/submit`, {
          user_id: parseInt(userId),
          duration: duration,
          answers: this.userAnswers
      }, {
          headers: {
              "Authorization": localStorage.getItem("token"),
              "Content-Type": "application/json"
          }
      })
      .then(response => {
          console.log("Server response:", response.data);
          this.score = response.data.score;
          this.correctAnswers = response.data.correct_answers;
          this.totalMarks = response.data.total_marks;
          this.timeTaken = response.data.time_taken;
          this.showResults = true;
      })
      .catch(error => console.error("Error submitting quiz:", error));
    },
      goToHome() {
      this.$router.push("/home");
    },
    goToQuizHistory() {
      this.$router.push("/user/quiz-history");
    },
    goToPerformanceSummary() {
      this.$router.push("/user/performance");
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user_id");
      this.$router.push("/login");
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
  background-image: url("@/assets/card.jpeg");
  background-size: cover;
  }
  .quiz-container {
    padding: 20px;
  }
  
  .question-card {
    background: #f9f9f9;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
  }
  
  h3, h4 {
    margin-bottom: 0;
  }
  
  .b-card {
    border-radius: 8px;
  }

  .logout-button {
  background-color: #f55;
  color: white;
  }

  .nav-btn {
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background 0.3s;
  }

  .link-btn {
  margin: 10px;
  font-weight: bold;
  border-radius: 20px;
  }
  </style>
  
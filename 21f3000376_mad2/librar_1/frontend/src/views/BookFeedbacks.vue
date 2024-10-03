<template>
  <div class="book-feedbacks">
    <h2>Feedbacks for {{ bookName }}</h2>
    <div v-if="feedbacks.length > 0">
      <table class="feedback-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feedback in feedbacks" :key="feedback.id">
            <td>{{ feedback.user.username }}</td>
            <td>{{ feedback.content }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No feedbacks found</p>
    </div>
    <router-link to="/user-dashboard" class="back-button">Back to Dashboard</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      feedbacks: [],
      bookName: ''
    };
  },
  created() {
    this.loadFeedbacks();
  },
  methods: {
    async loadFeedbacks() {
      try {
        const bookId = this.$route.params.bookId;
        console.log('Book ID:', bookId); 

        const feedbackResponse = await axios.get(`http://127.0.0.1:5000/api/feedback/${bookId}`);
        console.log('Feedbacks:', feedbackResponse.data); 
        this.feedbacks = feedbackResponse.data;
        const bookResponse = await axios.get(`http://127.0.0.1:5000/api/book/${bookId}`);
        console.log('Book:', bookResponse.data);
        this.bookName = bookResponse.data.name;
      } catch (error) {
        console.error('Error loading feedbacks:', error);
      }
    }
  }
};
</script>

<style>
.book-feedbacks {
  
  padding: 20px;
}

.feedback-table {
  
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.feedback-table th,
.feedback-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  vertical-align: middle;

}

.feedback-table th {
  background-color: #32a3e4;
  color: rgb(255, 255, 255);
}

.feedback-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.feedback-table tr:hover {
  background-color: #ddd;
}

.back-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #32a3e4;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  text-align: center;
}

.back-button:hover {
  background-color: #258bb5;
}
</style>

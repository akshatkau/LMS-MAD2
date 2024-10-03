<template>
    <div class="book-content-page">
      <h1>{{ book.name }}</h1>
      <p><strong>Author:</strong> {{ book.author }}</p>
      <p><strong>Return Date:</strong> {{ book.return_date }}</p>
      <h3>Content:</h3>
      <p>{{ book.content }}</p>
      <router-link to="/user-dashboard" class="back-button">Back to Dashboard</router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        book: {}
      };
    },
    created() {
      this.loadBookContent();
    },
    methods: {
      async loadBookContent() {
        try {
          const bookId = this.$route.params.bookId;
          const response = await axios.get(`http://127.0.0.1:5000/api/book/${bookId}`);
          this.book = response.data;
        } catch (error) {
          console.error('Error loading book content:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .book-content-page {
    padding: 20px;
  }
  
  .back-button {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #32a3e4;
    color: white;
    text-decoration: none;
    border-radius: 4px;
  }
  
  .back-button:hover {
    background-color: #258bb5;
  }
  </style>
  
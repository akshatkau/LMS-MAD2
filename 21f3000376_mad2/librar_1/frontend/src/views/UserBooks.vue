<template>
  <div class="user-books">
    <h1>My Books</h1>
    <div v-if="groupedBooks.length > 0">
      <div v-for="section in groupedBooks" :key="section.section_id" class="section">
        <h2>Section: {{ section.section_name }}</h2>
        <div class="book-cards">
          <div v-for="book in section.books" :key="book.book_id" class="book-card">
            <img :src="`https://picsum.photos/seed/${book.book_id}/200/300`" alt="Book Image" class="book-image"/>
            <h3>{{ book.book_name }}</h3>
            <p><strong>Author:</strong> {{ book.book_author }}</p>
            <button @click="goToBookContentPage(book.book_id)" class="view-content-button">View Content</button>
            <p><strong>Return Date:</strong> {{ book.return_date }}</p>
            <div v-if="book.status === 'accepted'" class="feedback-section">
              <h4>Give Feedback:</h4>
              <textarea v-model="feedbackContent[book.book_id]" placeholder="Enter your feedback"></textarea>
              <button @click="submitFeedback(book.book_id)" class="submit-feedback-button">Submit Feedback</button>
            </div>
            <button v-if="book.status === 'accepted'" @click="goToPaymentPage(book.book_id)" class="download-pdf-button">Get PDF</button>
            <button @click="returnBook(book.book_id)" class="return-book-button">Return Book</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No books found</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      books: [],
      user_id: JSON.parse(localStorage.getItem('user')).id,
      dialogVisible: false,
      selectedBook: {},
      feedbackContent: {},
      groupedBooks: []
    };
  },
  created() {
    this.loadBooks();
  },
  watch: {
    books: 'groupBooksBySection'
  },
  methods: {
    async loadBooks() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/request/user/${this.user_id}`);
        console.log('API Response:', response.data);
        this.books = response.data.map(request => ({
          book_id: request.book_id,
          book_name: request.book_name,
          book_author: request.book_author,
          content: request.book ? request.book.content : '', // Ensure this field is populated
          issue_date: request.issue_date,
          return_date: request.return_date,
          status: request.status,
          section_id: request.book.section_id,
          section_name: request.book.section_name
        }));
      } catch (error) {
        console.error('Error loading books:', error);
      }
    },
    groupBooksBySection() {
      const grouped = this.books.reduce((acc, book) => {
        if (book.status === 'accepted') {
          const section = acc.find(s => s.section_id === book.section_id);
          if (section) {
            section.books.push(book);
          } else {
            acc.push({ section_id: book.section_id, section_name: book.section_name, books: [book] });
          }
        }
        return acc;
      }, []);
      this.groupedBooks = grouped;
      console.log('Grouped Books:', this.groupedBooks);
    },
    goToBookContentPage(bookId) {
      this.$router.push({ name: 'BookContent', params: { bookId } });
    },
    async returnBook(bookId) {
      const toast = useToast();
      try {
        const response = await axios.put(`http://127.0.0.1:5000/api/request/return/${bookId}`, {
          user_id: this.user_id
        });
        console.log(response.data);
        toast.success('Book returned successfully');
        this.loadBooks();
      } catch (error) {
        toast.error('Failed to return book');
        console.error('Error returning book:', error);
      }
    },
    async submitFeedback(bookId) {
      const toast = useToast();
      try {
        const response = await axios.post(`http://127.0.0.1:5000/api/feedback`, {
          user_id: this.user_id,
          book_id: bookId,
          content: this.feedbackContent[bookId]
        });
        console.log(response.data);
        this.feedbackContent[bookId] = '';
        toast.success('Feedback submitted successfully');
      } catch (error) {
        toast.error('Failed to submit feedback');
        console.error('Error submitting feedback:', error);
      }
    },
    goToPaymentPage(bookId) {
      this.$router.push({ name: 'PaymentPage', params: { bookId } });
    }
  }
};
</script>

<style>
.user-books {
  padding: 20px;
}

.book-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; 
  gap: 20px; 
}

.book-card {
  border: 1px solid #ccc;
  padding: 20px;
  margin: 10px;
  width: 200px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-card img {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
}

.book-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.book-card p {
  margin: 5px 0;
}

.book-card button,
.book-card .router-link {
  display: block;
  width: 100%;
  margin-top: 10px;
  padding: 8px 12px;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.book-card .view-content-button {
  background-color: #32a3e4; 
  color: white;
}

.book-card .submit-feedback-button {
  background-color: #ffa500; 
  color: white;
}

.book-card .return-book-button {
  background-color: #dc3545; 
  color: white;
}

.book-card .download-pdf-button {
  background-color: #28a745; 
  color: white;
}

.book-card button:hover,
.book-card .router-link:hover {
  opacity: 0.9;
}

.feedback-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feedback-section textarea {
  width: 100%;
  margin-top: 10px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
  text-align: center;
}

.book-title {
  font-size: 18px;
  font-weight: bold;
}

.book-author {
  font-size: 14px;
}

.book-content {
  font-size: 20px;
  margin-top: -20px; 
}

.close-dialog-button {
  background-color: #32a3e4;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.close-dialog-button:hover {
  background-color: #0056b3;
}
</style>

<template>
  <div class="user-dashboard">
    <h2>Welcome, {{ username }}</h2>
    <h2>Library Sections</h2>
    
    <h3>Search:</h3>
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search books, authors, sections"
        @input="filterSections"
      />
    </div>

    <div v-for="section in filteredSections" :key="section.id" class="section">
      <h2>Books in Section: {{ section.name }}</h2>
      <div class="book-cards">
        <div v-for="book in section.books" :key="book.id" class="book-card">
          <h4>{{ book.name }}</h4>
          <p><strong>Author:</strong> {{ book.author }}</p>
          <img :src="getPicsumImage(book.id)" alt="Book Image" />
          <p v-if="book.status === 'accepted'"><strong>Issue Date:</strong> {{ book.issue_date }}</p>
          <p v-if="book.status === 'accepted'"><strong>Return Date:</strong> {{ book.return_date }}</p>
          <button v-if="book.status === 'accepted'" @click="showContentDialog(book)">View Content</button>
          <button v-if="book.status !== 'accepted'" @click="addToRequestList(book.id)" class="request-button">Add to Request List</button>
          <button @click="viewFeedbacks(book.id)" class="feedback-button">View Feedbacks</button>
        </div>
      </div>
    </div>
    <div v-if="dialogVisible" class="dialog-overlay">
      <div class="dialog">
        <h3>{{ selectedBook.name }}</h3>
        <p><strong>Author:</strong> {{ selectedBook.author }}</p>
        <h5>Content:</h5>
        <p class="book-content">{{ selectedBook.content }}</p>
        <button @click="dialogVisible = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      sections: [],
      filteredSections: [],
      searchQuery: '',
      user_id: JSON.parse(localStorage.getItem('user')).id,
      username: JSON.parse(localStorage.getItem('user')).username, 
      requests: [],
      dialogVisible: false,
      selectedBook: {}
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  mounted() {
    this.loadSectionsWithBooks();
    this.loadRequests();
  },
  methods: {
    async loadSectionsWithBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/section');
        const sections = response.data;
        for (let section of sections) {
          for (let book of section.books) {
            const feedbackResponse = await axios.get(`http://127.0.0.1:5000/api/feedback/${book.id}`);
            book.feedbacks = feedbackResponse.data;
          }
        }
        this.sections = sections;
        this.filteredSections = sections;
      } catch (error) {
        console.error(error);
      }
    },
    async loadRequests() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/request/user/${this.user_id}`);
        this.requests = response.data;
        this.updateBookRequestStatus();
      } catch (error) {
        console.error(error);
      }
    },
    async addToRequestList(bookId) {
      const toast = useToast();
      try {
        await axios.post('http://127.0.0.1:5000/api/request', {
          user_id: this.user_id,
          book_id: bookId
        });
        toast.success('Book request added successfully');
        this.loadSectionsWithBooks();
        this.loadRequests();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          toast.error(error.response.data.message);
        } else {
          toast.error('Failed to add book request');
        }
        console.error(error);
      }
    },
    updateBookRequestStatus() {
      this.sections.forEach(section => {
        section.books.forEach(book => {
          const request = this.requests.find(r => r.book_id === book.id);
          if (request) {
            book.status = request.status;
            book.issue_date = request.issue_date || 'N/A';
            book.return_date = request.return_date || 'N/A';
            book.feedbacks = request.feedbacks || [];
          } else {
            book.status = 'available';
            book.issue_date = 'N/A';
            book.return_date = 'N/A';
          }
        });
      });
    },
    filterSections() {
      const query = this.searchQuery.toLowerCase();

      this.filteredSections = this.sections.filter(section => {
        const sectionMatch = section.name.toLowerCase().includes(query);
        const booksMatch = section.books.some(book => 
          book.name.toLowerCase().includes(query) || 
          book.author.toLowerCase().includes(query)
        );

        if (sectionMatch) {
          return true;
        } else if (booksMatch) {
          section.books = section.books.filter(book => 
            book.name.toLowerCase().includes(query) || 
            book.author.toLowerCase().includes(query)
          );
          return true;
        }
        return false;
      });
    },
    showContentDialog(book) {
      this.selectedBook = book;
      this.dialogVisible = true;
    },
    viewFeedbacks(bookId) {
      this.$router.push({ name: 'BookFeedbacks', params: { bookId } });
    },
    getPicsumImage(bookId) {
      return `https://picsum.photos/seed/${bookId}/200/300`;
    }
  }
};
</script>


<style>
.user-dashboard {
  padding: 20px;
}

.search-container {
  margin-bottom: 60px;
  display: flex;
  justify-content: center;
}

.search-container input {
  padding: 10px;
  width: 60%; 
  border-radius: 5px;
  border: 1px solid #ccc;
}

.section {
  margin-bottom: 40px;
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

.book-card h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.book-card p {
  margin: 5px 0;
}

.book-card img {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
}

.book-card button,
.book-card .router-link {
  display: block;
  width: 80%;
  margin-top: 10px;
  padding: 8px 12px;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.book-card .request-button {
  background-color: #32a3e4; 
  color: white;
}

.book-card .feedback-button {
  background-color: #ffa500; 
  color: white;
  text-decoration: none;
}

.book-card button:hover,
.book-card .router-link:hover {
  opacity: 0.9;
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
}

.dialog h3 {
  font-size: 18px;
  font-weight: bold;
}

.dialog p {
  font-size: 14px;
}

.dialog h5 {
  font-size: 16px;
  margin-top: 10px;
}

.dialog .book-content {
  font-size: 20px;
}
</style>

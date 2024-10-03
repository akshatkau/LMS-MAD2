<template>
  <div class="section-books">
    <h2>Books in Section: {{ section.name }}</h2>
    <router-link to="/admin-dashboard" class="back-button">Back to Dashboard</router-link>
    <table v-if="books.length > 0" class="styled-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Book Name</th>
          <th>Author</th>
          <th>Content</th>
          <th>Create Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.id }}</td>
          <td>
            <input type="text" v-model="book.name" :disabled="book.id !== editingBookId">
          </td>
          <td>
            <input type="text" v-model="book.author" :disabled="book.id !== editingBookId">
          </td>
          <td>
            <textarea v-model="book.content" :disabled="book.id !== editingBookId"></textarea>
          </td>
          <td>
            <input type="date" v-model="book.issue_date" :disabled="book.id !== editingBookId">
          </td>
          <td>
            <button v-if="book.id !== editingBookId" @click="startEditing(book)" class="edit-button">Edit</button>
            <button v-else @click="saveBook(book)" class="save-button">Save</button>
            <button @click="deleteBook(book)" class="delete-button">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No books found in this section</p>
    </div>
    <div class="book-management">
      <h3>Add Book to Section: {{ section.name }}</h3>
      <form @submit.prevent="addBook" class="add-book-form">
        <input type="text" v-model="newBookName" placeholder="Enter book name" required>
        <input type="text" v-model="newBookAuthor" placeholder="Enter book author">
        <textarea v-model="newBookContent" placeholder="Enter book content"></textarea>
        <input type="date" v-model="newBookIssueDate" placeholder="Enter issue date (optional)">
        <button type="submit" class="add-book-button">Add Book</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      section: {},
      books: [],
      newBookName: '',
      newBookAuthor: '',
      newBookContent: '',
      newBookIssueDate: '',
      newBookReturnDate: '',
      editingBookId: null
    };
  },
  created() {
    this.loadSection();
    this.loadBooks();
  },
  methods: {
    async loadSection() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/section/${this.$route.params.sectionId}`);
        this.section = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async loadBooks() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/book?section_id=${this.$route.params.sectionId}`);
        this.books = response.data.filter(book => book.section_id === parseInt(this.$route.params.sectionId));
      } catch (error) {
        console.error(error);
      }
    },
    async addBook() {
      const toast = useToast();
      try {
        await axios.post('http://127.0.0.1:5000/api/book', {
          name: this.newBookName,
          author: this.newBookAuthor,
          content: this.newBookContent,
          section_id: this.$route.params.sectionId,
          user_id: 1, 
          issue_date: this.newBookIssueDate || new Date().toISOString().split('T')[0],
          return_date: this.newBookReturnDate || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        });
        toast.success('Book added successfully');
        this.newBookName = '';
        this.newBookAuthor = '';
        this.newBookContent = '';
        this.newBookIssueDate = '';
        this.newBookReturnDate = '';
        this.loadBooks();
      } catch (error) {
        toast.error('Failed to add book');
        console.error(error);
      }
    },
    async saveBook(book) {
      const toast = useToast();
      try {
        await axios.put('http://127.0.0.1:5000/api/book', {
          id: book.id,
          name: book.name,
          author: book.author,
          content: book.content,
          section_id: this.$route.params.sectionId,
          user_id: 1, 
          issue_date: book.issue_date,
          return_date: book.return_date
        });
        toast.success('Book updated successfully');
        this.editingBookId = null;
        this.loadBooks();
      } catch (error) {
        toast.error('Failed to update book');
        console.error(error);
      }
    },
    async deleteBook(book) {
      const toast = useToast();
      try {
        await axios.delete('http://127.0.0.1:5000/api/book', { data: { id: book.id } });
        toast.success('Book deleted successfully');
        this.loadBooks();
      } catch (error) {
        toast.error('Failed to delete book');
        console.error(error);
      }
    },
    startEditing(book) {
      this.editingBookId = book.id;
    }
  }
};
</script>

<style>
.section-books {
  padding: 20px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  text-align: center;
}

.styled-table th, .styled-table td {
  border: 1px solid #ccc;
  padding: 10px;
}

.styled-table th {
  background-color: #32a3e4;
  color: rgb(255, 255, 255);
}

.styled-table tr:nth-child(even) {
  background-color: #e0f7fa;
}

.styled-table tr:nth-child(odd) {
  background-color: #ffffff;
}

.edit-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.edit-button:hover {
  background-color: #0056b3;
}

.save-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.save-button:hover {
  background-color: #218838;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.delete-button:hover {
  background-color: #c82333;
}

.book-management {
  margin-top: 20px;
}

.book-management h3 {
  text-align: center;
}

.add-book-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.add-book-form input,
.add-book-form textarea {
  padding: 10px;
  width: 60%;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.add-book-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-book-button:hover {
  background-color: #0056b3;
}
</style>

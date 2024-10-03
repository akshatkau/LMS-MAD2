<template>
  <div class="section-management">
    <h2>Welcome, {{ username }}</h2>
    <button @click="exportcsv"> Download Report </button>

    <h1>Section Management</h1>
    <h3> Search Sections:</h3>

    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search sections"
        @input="filterSections"
      />
    </div>
    
    <h3>Add a New Section:</h3>
    <form @submit.prevent="addSection" class="add-section-bar">
      <input type="text" v-model="newSectionName" placeholder="Enter section name" required>
      <button type="submit" class="add-section-button">Add Section</button>
    </form>
    
    <table v-if="filteredSections.length > 0" class="section-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Section Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="section in filteredSections" :key="section.id">
          <td>{{ section.id }}</td>
          <td>
            <input type="text" v-model="section.name" :disabled="section.id !== editingSectionId">
          </td>
          <td>
            <button v-if="section.id !== editingSectionId" @click="startEditing(section)" class="edit-button">Edit</button>
            <button v-else @click="saveSection(section)" class="save-button">Save</button>
            <button @click="deleteSection(section)" class="delete-button">Delete</button>
            <router-link :to="{ name: 'section-books', params: { sectionId: section.id } }" class="view-books-button">View Books</router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No sections found</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      sections: [],
      username: JSON.parse(localStorage.getItem('user')).username,
      newSectionName: '',
      editingSectionId: null,
      filteredSections: [],
      searchQuery: ''
    };
  },
  mounted() {
    this.loadSections();
  },
  methods: {
    async loadSections() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/section');
        this.sections = response.data;
        this.filteredSections = this.sections;
      } catch (error) {
        console.error(error);
      }
    },
    filterSections() {
      const query = this.searchQuery.toLowerCase();
      this.filteredSections = this.sections.filter(section => section.name.toLowerCase().includes(query));
    },
    async addSection() {
      const toast = useToast();
      try {
        await axios.post('http://127.0.0.1:5000/api/section', { name: this.newSectionName });
        toast.success('Section added successfully');
        this.newSectionName = '';
        this.loadSections();
      } catch (error) {
        toast.error('Failed to add section');
        console.error(error);
      }
    },
    async deleteSection(section) {
      const toast = useToast();
      console.log(`Attempting to delete section: ${section.id} - ${section.name}`);
      try {
        const response = await axios.delete('http://127.0.0.1:5000/api/section', { data: { id: section.id } });
        console.log(response.data);
        toast.success('Section and its books deleted successfully');
        this.loadSections();
      } catch (error) {
        toast.error('Failed to delete section');
        console.error(error);
      }
    },
    async saveSection(section) {
      const toast = useToast();
      try {
        await axios.put('http://127.0.0.1:5000/api/section', { id: section.id, name: section.name });
        toast.success('Section updated successfully');
        this.editingSectionId = null;
        this.loadSections();
      } catch (error) {
        toast.error('Failed to update section');
        console.error(error);
      }
    },
    startEditing(section) {
      this.editingSectionId = section.id;
    },
    exportcsv(){
      const accessToken = localStorage.getItem('token');
      console.log(accessToken);
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios.post('http://127.0.0.1:5000/exportcsv/1',{},{headers,
        responseType:'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const downloadLink = document.createElement('a');
        downloadLink.href=url;
        downloadLink.setAttribute('download','section_report.csv');
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }
      )
      .catch(error => {
        console.error(error);
        console.log('Error downloading file');
      });
    }
  }
};
</script>

<style>
.section-management {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-bar input {
  padding: 10px;
  width: 30%; 
  border-radius: 5px;
  border: 1px solid #ccc;
}

.add-section-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.add-section-bar input {
  padding: 10px;
  width: 60%;
  margin-right: 10px; 
  border-radius: 5px;
  border: 1px solid #ccc;
}

.add-section-bar button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-section-bar button:hover {
  background-color: #0056b3;
}

h3 {
  text-align: center;
  margin-top: 20px;
}

.section-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  text-align: center;
}

.section-table th, .section-table td {
  border: 1px solid #ccc;
  padding: 10px;
}

.section-table th {
  background-color: #32a3e4;
  color: rgb(255, 255, 255);
}

.section-table tr:nth-child(even) {
  background-color: #e0f7fa; /* Light blue color */
}

.section-table tr:nth-child(odd) {
  background-color: #ffffff; /* White color */
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

.view-books-button {
  background-color: #17a2b8;
  color: white;
  padding: 5px 10px;
  text-decoration: none;
  border-radius: 3px;
}

.view-books-button:hover {
  background-color: #138496;
}
</style>
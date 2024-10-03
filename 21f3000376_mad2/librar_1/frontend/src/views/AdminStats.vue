<template>
  <div class="admin-stats">
    <h2>Library Statistics</h2>
    <div class="stats-boxes">
      <div class="stat-box">
        <h3>Total Books</h3>
        <p>{{ stats.total_books }}</p>
      </div>
      <div class="stat-box">
        <h3>Total Sections</h3>
        <p>{{ stats.total_sections }}</p>
      </div>
      <div class="stat-box">
        <h3>Books Issued</h3>
        <p>{{ stats.total_books_issued }}</p>
      </div>
      <div class="stat-box">
        <h3>Total Users</h3>
        <p>{{ stats.total_users }}</p>
      </div>
    </div>
    <div class="chart-container">
      <h3>Number of Books in Library Section-wise</h3>
      <canvas id="booksInLibraryChart"></canvas>
    </div>
    <br>
    <br>
    
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

export default {
  setup() {
    const stats = ref({
      total_books: 0,
      total_sections: 0,
      total_books_issued: 0,
      total_users: 0
    });

    const booksInLibraryChart = ref(null);

    onMounted(async () => {
      await loadLibraryStats();
      await loadBooksInLibraryChart();
    });

    const loadLibraryStats = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/stats/library');
        stats.value = response.data;
        console.log('Library Stats:', stats.value);
      } catch (error) {
        console.error('Error loading library stats:', error);
      }
    };

    const loadBooksInLibraryChart = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/stats/books-in-library');
        const data = response.data;
        console.log('Books In Library Data:', data);

        const ctx = document.getElementById('booksInLibraryChart').getContext('2d');
        booksInLibraryChart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.sections,
            datasets: [{
              label: 'Books in Library',
              data: data.counts,
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      } catch (error) {
        console.error('Error loading books in library chart:', error);
      }
    };

    

    return {
      stats,
      booksInLibraryChart,
      
    };
  }
};
</script>

<style>
.admin-stats {
  padding: 20px;
}

.stats-boxes {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-box {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 20%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.stat-box h3 {
  margin-bottom: 10px;
  font-size: 18px;
}

.stat-box p {
  font-size: 24px;
  font-weight: bold;
}

.chart-container {
  width: 60%;
  height: 400px;
  margin: 20px auto;
}



</style>

<template>
    <div class="payment-page">
      <h1>Payment for PDF</h1>
      <div v-if="book">
        <h2>{{ book.name }}</h2>
        <p><strong>Author:</strong> {{ book.author }}</p>
        <p><strong>Price:</strong> ₹50</p>
        <button @click="downloadPdf" class="pay-button">Pay ₹50 to Download PDF</button>
      </div>
      <div v-else>
        <p>Loading book details...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useToast } from 'vue-toastification';
  
  export default {
    data() {
      return {
        book: null,
      };
    },
    created() {
      this.loadBookDetails();
    },
    methods: {
      async loadBookDetails() {
        const bookId = this.$route.params.bookId;
        console.log('Fetching details for book ID:', bookId);
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/book/${bookId}`);
          console.log('Book details response:', response.data);
          this.book = response.data;
        } catch (error) {
          console.error('Error loading book details:', error);
        }
      },
      downloadPdf() {
        const toast = useToast();
        try {
          const pdfUrl = `${window.location.origin}/demo.pdf`; // Path to the PDF in the public folder
          const link = document.createElement('a');
          link.href = pdfUrl;
          link.setAttribute('download', 'demo.pdf'); // Or use this.book.name + '.pdf'
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          toast.success('Payment successful and PDF downloaded');
        } catch (error) {
          toast.error('Failed to download PDF');
          console.error('Error downloading PDF:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .payment-page {
    padding: 20px;
    text-align: center;
  }
  
  .pay-button {
    padding: 10px 20px;
    background-color: #28a745; /* Green color */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .pay-button:hover {
    background-color: #218838;
  }
  </style>
  
// Fungsi untuk format angka ke format rupiah
function formatRupiah(angka) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR'
    }).format(angka);
}

// Handler untuk form submit
function handleFormSubmit(event) {
    event.preventDefault();
    
    // Tampilkan loading state
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Ambil data dari form
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = parseFloat(value);
    });

    // Kirim request ke API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Sembunyikan loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
        
        // Tampilkan hasil
        displayResults(result);
        
        // Tampilkan section hasil
        document.getElementById('resultsSection').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loadingSpinner').style.display = 'none';
        alert('Terjadi kesalahan saat melakukan analisis. Silakan coba lagi.');
    });
}

// Fungsi untuk menampilkan hasil
function displayResults(result) {
    // Tampilkan prediksi
    document.getElementById('predictionResult').innerHTML = `
        <p><strong>Prediksi Penggunaan Dana:</strong> ${formatRupiah(result.prediksi)}</p>
    `;
    
    // Tampilkan sisa dana
    document.getElementById('sisaDana').innerHTML = `
        <p><strong>Sisa Dana:</strong> ${formatRupiah(result.sisa_dana)}</p>
    `;
    
    // Tampilkan efisiensi
    document.getElementById('efisiensi').innerHTML = `
        <p><strong>Efisiensi Penggunaan:</strong> ${result.efisiensi.toFixed(2)}%</p>
    `;
    
    // Tampilkan analisis detail
    document.getElementById('analysisResult').innerHTML = `
        <div class="analysis-chart">
            <h5>Distribusi Penggunaan Dana:</h5>
            <div class="progress-container">
                <div class="progress mb-3">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${result.analisis.persentase_operasional}%" 
                         aria-valuenow="${result.analisis.persentase_operasional}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        Operasional (${result.analisis.persentase_operasional.toFixed(1)}%)
                    </div>
                </div>
                <div class="progress mb-3">
                    <div class="progress-bar bg-success" role="progressbar" 
                         style="width: ${result.analisis.persentase_gaji}%" 
                         aria-valuenow="${result.analisis.persentase_gaji}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        Gaji & Honor (${result.analisis.persentase_gaji.toFixed(1)}%)
                    </div>
                </div>
                <div class="progress mb-3">
                    <div class="progress-bar bg-info" role="progressbar" 
                         style="width: ${result.analisis.persentase_pembelajaran}%" 
                         aria-valuenow="${result.analisis.persentase_pembelajaran}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        Pembelajaran (${result.analisis.persentase_pembelajaran.toFixed(1)}%)
                    </div>
                </div>
                <div class="progress mb-3">
                    <div class="progress-bar bg-warning" role="progressbar" 
                         style="width: ${result.analisis.persentase_perawatan}%" 
                         aria-valuenow="${result.analisis.persentase_perawatan}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        Perawatan (${result.analisis.persentase_perawatan.toFixed(1)}%)
                    </div>
                </div>
                <div class="progress mb-3">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: ${result.analisis.persentase_pengembangan}%" 
                         aria-valuenow="${result.analisis.persentase_pengembangan}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        Pengembangan (${result.analisis.persentase_pengembangan.toFixed(1)}%)
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Tampilkan informasi model
    document.getElementById('modelInfo').innerHTML = `
        <div class="model-info">
            <h5>Informasi Model:</h5>
            <p><strong>Arsitektur Model:</strong> ${result.model_info.layer_sizes.join(' → ')}</p>
            <p><strong>Jumlah Parameter:</strong> ${result.model_info.num_parameters.toLocaleString()}</p>
        </div>
    `;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysisForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Input validation
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });
});
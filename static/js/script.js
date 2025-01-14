fetch('/service', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        jumlah_siswa: 139,
        dana_diterima: 221010000,
        // tambahkan data lainnya
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

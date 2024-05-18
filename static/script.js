document.addEventListener('DOMContentLoaded', function() {
    const customerSelect = document.getElementById('customer-select');
    const customerDetails = document.getElementById('customer-details');

    // Fetch customer names to populate the dropdown menu
    fetch('/get_customers')
        .then(response => response.json())
        .then(data => {
            data.forEach(customer => {
                const option = document.createElement('option');
                option.value = customer.customer_id;
                option.textContent = `${customer.first_name} ${customer.last_name}`;
                customerSelect.appendChild(option);
            });
        });

    // Event listener for when a customer is selected
    customerSelect.addEventListener('change', function() {
        const customerId = customerSelect.value;
        if (customerId) {
            fetch(`/get_customer_details/${customerId}`)
                .then(response => response.json())
                .then(data => {
                    let ordersHtml = '';
                    if (data.orders && data.orders.length > 0) {
                        ordersHtml = '<h3>Orders</h3><ul>';
                        data.orders.forEach(order => {
                            ordersHtml += `<li>${order.item} - $${order.amount}</li>`;
                        });
                        ordersHtml += '</ul>';
                    } else {
                        ordersHtml = '<h3>Orders</h3><p>No orders found.</p>';
                    }

                    let shippingsHtml = '';
                    if (data.shippings && data.shippings.length > 0) {
                        shippingsHtml = '<h3>Shippings</h3><ul>';
                        data.shippings.forEach(shipping => {
                            shippingsHtml += `<li>${shipping.status}</li>`;
                        });
                        shippingsHtml += '</ul>';
                    } else {
                        shippingsHtml = '<h3>Shippings</h3><p>No shipping information found.</p>';
                    }

                    customerDetails.innerHTML = `
                        <h2>${data.first_name} ${data.last_name}</h2>
                        <p>Age: ${data.age}</p>
                        <p>Country: ${data.country}</p>
                        ${ordersHtml}
                        ${shippingsHtml}
                    `;
                });
        } else {
            customerDetails.innerHTML = '';
        }
    });
});

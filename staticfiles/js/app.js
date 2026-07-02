document.addEventListener('DOMContentLoaded', function() {
    
    // ----------------------------------------------------
    // 1. Data Purchase Network Filtering & Selection
    // ----------------------------------------------------
    const networkOptions = document.querySelectorAll('.network-option');
    const planCards = document.querySelectorAll('.plan-card');
    const planInput = document.getElementById('selected-plan-input');
    const networkInput = document.getElementById('selected-network-input');
    const phoneInput = document.getElementById('phone-number-input');

    if (networkOptions.length > 0 && planCards.length > 0) {
        // Handle click on network buttons
        networkOptions.forEach(opt => {
            opt.addEventListener('click', function() {
                const network = this.dataset.network;
                
                // Set active class
                networkOptions.forEach(o => o.classList.remove('active'));
                this.classList.add('active');
                
                // Update hidden inputs
                if (networkInput) networkInput.value = network;
                if (planInput) planInput.value = ''; // Reset plan selection

                // Filter plans
                let firstPlanSet = false;
                planCards.forEach(card => {
                    card.classList.remove('active');
                    if (card.dataset.network === network) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // Handle click on plan cards
        planCards.forEach(card => {
            card.addEventListener('click', function() {
                planCards.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                if (planInput) planInput.value = this.dataset.planId;
            });
        });
        
        // Auto-detect network from phone number prefix in Nigeria
        // MTN: 0803, 0806, 0703, 0706, 0813, 0816, 0810, 0814, 0903, 0906, 0913, 0916
        // Airtel: 0802, 0808, 0708, 0701, 0812, 0902, 0907, 0901, 0912
        // Glo: 0805, 0807, 0705, 0815, 0905, 0915
        // 9mobile: 0809, 0817, 0818, 0909, 0908
        if (phoneInput) {
            phoneInput.addEventListener('input', function() {
                const val = this.value.trim();
                if (val.length >= 4) {
                    const prefix = val.substring(0, 4);
                    let detectedNetwork = null;
                    
                    const mtnPrefixes = ['0803', '0806', '0703', '0706', '0813', '0816', '0810', '0814', '0903', '0906', '0913', '0916'];
                    const airtelPrefixes = ['0802', '0808', '0708', '0701', '0812', '0902', '0907', '0901', '0912'];
                    const gloPrefixes = ['0805', '0807', '0705', '0815', '0905', '0915'];
                    const nineMobilePrefixes = ['0809', '0817', '0818', '0909', '0908'];
                    
                    if (mtnPrefixes.includes(prefix)) detectedNetwork = 'MTN';
                    else if (airtelPrefixes.includes(prefix)) detectedNetwork = 'Airtel';
                    else if (gloPrefixes.includes(prefix)) detectedNetwork = 'Glo';
                    else if (nineMobilePrefixes.includes(prefix)) detectedNetwork = '9Mobile';
                    
                    if (detectedNetwork) {
                        const targetOption = document.querySelector(`.network-option[data-network="${detectedNetwork}"]`);
                        if (targetOption && !targetOption.classList.contains('active')) {
                            targetOption.click();
                        }
                    }
                }
            });
        }
        
        // Trigger initial filter (default to first active network option)
        const activeNetwork = document.querySelector('.network-option.active');
        if (activeNetwork) {
            activeNetwork.click();
        }
    }

    // ----------------------------------------------------
    // 2. Tabs for Bill Payments (Pay Bills View)
    // ----------------------------------------------------
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const activeTabInput = document.getElementById('active-bill-type');

    if (tabBtns.length > 0 && tabContents.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const targetTab = this.dataset.tab;
                
                // Update active tab buttons
                tabBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Update active contents
                tabContents.forEach(c => c.classList.remove('active'));
                const targetContent = document.getElementById(`${targetTab}-tab`);
                if (targetContent) targetContent.classList.add('active');
                
                // Update form field indicating active tab type
                if (activeTabInput) activeTabInput.value = targetTab;
            });
        });
    }

    // ----------------------------------------------------
    // 3. Checkout Simulator UI Card Formatter
    // ----------------------------------------------------
    const cardInput = document.getElementById('card-number');
    const expiryInput = document.getElementById('card-expiry');
    const cvvInput = document.getElementById('card-cvv');

    if (cardInput) {
        cardInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formatted = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formatted += ' ';
                }
                formatted += value[i];
            }
            e.target.value = formatted.substring(0, 19);
        });
    }

    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formatted = '';
            if (value.length > 2) {
                formatted = value.substring(0, 2) + '/' + value.substring(2, 4);
            } else {
                formatted = value;
            }
            e.target.value = formatted.substring(0, 5);
        });
    }

    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').substring(0, 3);
        });
    }
});

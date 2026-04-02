document.addEventListener('DOMContentLoaded', () => {


    // ==========================================
    // Navbar Scroll Effect
    // ==========================================
    const navbar = document.querySelector('.custom-navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // ==========================================
    // Filter Dropdowns
    // ==========================================
    const filterDropdownItems = document.querySelectorAll('.custom-filter-dropdown .dropdown-item');
    filterDropdownItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const text = this.innerText;
            const dropdown = this.closest('.custom-filter-dropdown');
            const selectedValue = dropdown ? dropdown.querySelector('.selected-value') : null;
            if (selectedValue) selectedValue.innerText = text;
        });
    });

    // ==========================================
    // Tour Categories Arch Carousel
    // ==========================================
    const archCarouselEl = document.querySelector('.custom-arch-carousel');
    if (archCarouselEl && typeof $.fn.owlCarousel !== 'undefined') {
        const archCarousel = $(archCarouselEl);
        const dotsContainer = $('.custom-arch-dots');
        const totalItems = archCarousel.children('.item').length;

        dotsContainer.empty();
        for (let i = 0; i < totalItems; i++) {
            const activeClass = i === 0 ? 'active' : '';
            dotsContainer.append(`<button class="custom-dot ${activeClass}" data-index="${i}" aria-label="Slide ${i + 1}"></button>`);
        }

        function updateArchStyles(e) {
            const items = archCarousel.find('.owl-item');
            items.removeClass('item-center item-left-1 item-left-2 item-right-1 item-right-2');
            let centerItem;
            let relativeIndex = 0;
            if (e && e.item && e.item.index != null) {
                centerItem = items.eq(e.item.index);
                if (e.relatedTarget) {
                    relativeIndex = e.relatedTarget.relative(e.item.index);
                }
            } else {
                centerItem = archCarousel.find('.owl-item.center');
                if (centerItem.length) {
                    relativeIndex = centerItem.index() % totalItems;
                }
            }
            if (centerItem && centerItem.length) {
                centerItem.addClass('item-center');
                centerItem.prev().addClass('item-left-1');
                centerItem.prev().prev().addClass('item-left-2');
                centerItem.next().addClass('item-right-1');
                centerItem.next().next().addClass('item-right-2');
            }
            if (e && e.relatedTarget) {
                $('.custom-dot').removeClass('active');
                $(`.custom-dot[data-index="${relativeIndex}"]`).addClass('active');
            }
        }

        archCarousel.on('translate.owl.carousel initialized.owl.carousel', updateArchStyles);

        archCarousel.owlCarousel({
            center: true,
            items: 5,
            loop: true,
            margin: 15,
            nav: false,
            dots: false,
            smartSpeed: 800,
            autoplay: true,
            autoplayTimeout: 4000,
            autoplayHoverPause: true,
            responsive: {
                0: { items: 1.5, center: true, margin: 10 },
                576: { items: 3, center: true, margin: 15 },
                992: { items: 5, center: true, margin: 15 },
                1200: { items: 5, center: true, margin: 15 }
            }
        });

        dotsContainer.on('click', '.custom-dot', function () {
            const index = $(this).data('index');
            archCarousel.trigger('to.owl.carousel', [index, 800]);
        });
    }

    // ==========================================
    // Testimonial Carousel
    // ==========================================
    if (document.querySelector('.testimonial-carousel') && typeof $.fn.owlCarousel !== 'undefined') {
        $('.testimonial-carousel').owlCarousel({
            loop: true,
            margin: 20,
            nav: false,
            dots: false,
            autoplay: true,
            autoplayTimeout: 4000,
            autoplayHoverPause: true,
            responsive: {
                0: { items: 1, margin: 10 },
                768: { items: 2, margin: 15 },
                992: { items: 3, margin: 20 }
            }
        });
    }

    // ==========================================
    // Gallery Carousel
    // ==========================================
    if (document.querySelector('.gallery-carousel') && typeof $.fn.owlCarousel !== 'undefined') {
        $('.gallery-carousel').owlCarousel({
            loop: true,
            margin: 0,
            nav: false,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            responsive: {
                0: { items: 3 },
                768: { items: 3 },
                1200: { items: 5 }
            }
        });
    }

    // ==========================================
    // Fancybox
    // ==========================================
    if (typeof Fancybox !== 'undefined') {
        Fancybox.bind("[data-fancybox]", { Hash: false });
    }



    





    // ==========================================
// Customize Your Trip Overlay Logic
// ==========================================
const overlay = document.getElementById('customize-trip-overlay');
if (!overlay) return; // Guard: overlay must exist

const startBtns = document.querySelectorAll('.start-planning-btn');
const closeBtn = document.querySelector('.btn-close-overlay');
const nextBtn = document.querySelector('.next-step-btn');
const prevBtn = document.querySelector('.prev-step-btn');
const formSteps = document.querySelectorAll('.form-step');
const navItems = document.querySelectorAll('.step-nav-item');
const progressBar = document.getElementById('overlay-progress-bar');
const totalSteps = formSteps.length;
let currentStepIdx = 1;

// ── Destination Carousel (inside overlay, initialized lazily) ──
let destCarouselInitialized = false;

function initDestCarousel() {
    if (destCarouselInitialized) return;
    const destCarouselEl = document.querySelector('.destination-selection-carousel');
    if (destCarouselEl && typeof $.fn.owlCarousel !== 'undefined') {
        $(destCarouselEl).owlCarousel({
            loop: false,
            margin: 20,
            nav: true,
            dots: false,
            autoplay: false,
            mouseDrag: true,
            touchDrag: true,
            navText: [
                '<i class="fa-solid fa-chevron-left"></i>',
                '<i class="fa-solid fa-chevron-right"></i>'
            ],
            responsive: {
                0: { items: 1 },
                576: { items: 2 },
                992: { items: 3 }
            }
        });
        destCarouselInitialized = true;
    }
}

// ── Step Update Function ──
function updateStep() {
    formSteps.forEach(step => step.classList.remove('active'));

    const currentStepEl = document.querySelector(`.form-step[data-step="${currentStepIdx}"]`);
    if (currentStepEl) currentStepEl.classList.add('active');

    navItems.forEach(item => {
        const step = parseInt(item.dataset.step);
        item.classList.toggle('active', step === currentStepIdx);
    });

    if (progressBar) {
        const progress = (currentStepIdx / totalSteps) * 100;
        progressBar.style.width = `${progress}%`;
    }

    if (prevBtn) {
        const hidePrev = currentStepIdx === 1 || currentStepIdx === totalSteps;
        prevBtn.classList.toggle('opacity-0', hidePrev);
        prevBtn.disabled = hidePrev;
    }

    if (nextBtn) {
        if (currentStepIdx === 7 || currentStepIdx === 8) {
            nextBtn.classList.add('d-none');
        } else if (currentStepIdx === totalSteps) {
            nextBtn.innerHTML = 'Close <i class="bi bi-check-lg ms-2"></i>';
            nextBtn.classList.remove('d-none');
        } else {
            nextBtn.innerHTML = 'Next <i class="bi bi-chevron-right ms-2"></i>';
            nextBtn.classList.remove('d-none');
        }
    }

    if (currentStepIdx === 2) setTimeout(initDestCarousel, 100);
    if (currentStepIdx === 6) generateDayPlanningFields();
    if (currentStepIdx === 7) updateReviewStepSummary();
}

// ── Open Overlay ──
function openOverlay() {
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    currentStepIdx = 1;
    updateStep();
}

// ── Close Overlay ──
function closeOverlay() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// ── Button Listeners ──
startBtns.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openOverlay();
}));

if (closeBtn) closeBtn.addEventListener('click', closeOverlay);

if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        if (currentStepIdx === totalSteps) { closeOverlay(); return; }
        if (currentStepIdx < totalSteps) { currentStepIdx++; updateStep(); }
    });
}

if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        if (currentStepIdx > 1) { currentStepIdx--; updateStep(); }
    });
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('active')) closeOverlay();
});


// ==========================================
// Step 1: Travelers — Dynamic Member Input
// ==========================================
const travelerRadios = document.querySelectorAll('.traveler-type-radio');
const memberWrapper = document.getElementById('member-count-wrapper');
const memberInput = document.getElementById('member-count-input');
const memberOverlayHome = document.querySelector('.step-travelers .traveler-cards-wrap');

function positionMemberOverlay(activeRadio) {
    if (!memberWrapper || !activeRadio) return;
    const activeCard = activeRadio.closest('.traveler-selection-card');
    const imgWrap = activeCard ? activeCard.querySelector('.card-img-wrapper') : null;
    if (!imgWrap) return;
    if (memberWrapper.parentElement !== imgWrap) imgWrap.appendChild(memberWrapper);
    memberWrapper.style.left = '50%';
}

travelerRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        const val = radio.value;
        if (!memberWrapper || !memberInput) return;
        if (val === 'Solo') {
            memberWrapper.classList.add('d-none');
            memberInput.value = 1;
            if (memberOverlayHome && memberWrapper.parentElement !== memberOverlayHome)
                memberOverlayHome.appendChild(memberWrapper);
        } else if (val === 'Couple') {
            memberWrapper.classList.add('d-none');
            memberInput.value = 2;
            if (memberOverlayHome && memberWrapper.parentElement !== memberOverlayHome)
                memberOverlayHome.appendChild(memberWrapper);
        } else {
            memberWrapper.classList.remove('d-none');
            memberInput.value = (val === 'Family') ? 4 : 5;
            positionMemberOverlay(radio);
            memberInput.focus();
        }
    });
});

window.addEventListener('resize', () => {
    const active = document.querySelector('.traveler-type-radio:checked');
    const val = active ? active.value : '';
    if (val === 'Family' || val === 'Friends') positionMemberOverlay(active);
});


// ==========================================
// Step 4: Airport Selection
// ==========================================
const airportItems = document.querySelectorAll('.airport-item');
airportItems.forEach(item => {
    item.addEventListener('click', () => {
        airportItems.forEach(i => i.classList.remove('selected'));
        item.classList.add('selected');
        const step4 = document.querySelector('.form-step[data-step="4"]');
        if (step4) step4.dataset.selectedAirport = item.dataset.value;
    });
});


// ==========================================
// Step 5: Travel Date — Dynamic Calendar UI
// ==========================================
(function initTravelDateCalendar() {
    const step5 = document.querySelector('.form-step[data-step="5"]');
    if (!step5) return;

    const input = step5.querySelector('input[name="travel_date"]');
    const monthLabel = step5.querySelector('.trip-date-month');
    const daysGrid = step5.querySelector('.trip-date-days');
    const prevBtn = step5.querySelector('.trip-date-nav.prev');
    const nextBtn = step5.querySelector('.trip-date-nav.next');
    if (!input || !monthLabel || !daysGrid || !prevBtn || !nextBtn) return;

    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const pad2 = (n) => String(n).padStart(2, '0');
    const toISODate = (d) => `${d.getFullYear()}-${pad2(d.getMonth()+1)}-${pad2(d.getDate())}`;
    const parseISO = (s) => {
        if (!s) return null;
        const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s).trim());
        if (!m) return null;
        const dt = new Date(Number(m[1]), Number(m[2])-1, Number(m[3]));
        return isNaN(dt.getTime()) ? null : dt;
    };

    let selected = parseISO(input.value);
    const today = new Date(); today.setHours(0,0,0,0);
    let viewYear = (selected || today).getFullYear();
    let viewMonth = (selected || today).getMonth();

    function render() {
        monthLabel.textContent = `${monthNames[viewMonth]} ${viewYear}`;
        daysGrid.innerHTML = '';
        const firstOfMonth = new Date(viewYear, viewMonth, 1);
        const startDow = firstOfMonth.getDay();
        const start = new Date(viewYear, viewMonth, 1 - startDow);
        for (let i = 0; i < 42; i++) {
            const d = new Date(start); d.setDate(start.getDate() + i);
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'trip-date-day';
            btn.textContent = String(d.getDate());
            btn.setAttribute('role', 'gridcell');
            btn.dataset.date = toISODate(d);
            if (d.getMonth() !== viewMonth) btn.classList.add('is-outside');
            if (selected && toISODate(d) === toISODate(selected)) btn.classList.add('is-selected');
            btn.addEventListener('click', () => {
                selected = new Date(d.getFullYear(), d.getMonth(), d.getDate());
                input.value = toISODate(selected);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                viewYear = selected.getFullYear();
                viewMonth = selected.getMonth();
                render();
            });
            daysGrid.appendChild(btn);
        }
    }

    prevBtn.addEventListener('click', () => {
        viewMonth -= 1;
        if (viewMonth < 0) { viewMonth = 11; viewYear -= 1; }
        render();
    });
    nextBtn.addEventListener('click', () => {
        viewMonth += 1;
        if (viewMonth > 11) { viewMonth = 0; viewYear += 1; }
        render();
    });
    input.addEventListener('change', () => {
        const dt = parseISO(input.value);
        if (!dt) return;
        selected = dt; viewYear = dt.getFullYear(); viewMonth = dt.getMonth();
        render();
    });
    render();
})();


// ==========================================
// Step 7: Review Summary
// ==========================================
function updateReviewStepSummary() {
    const travelersEl   = document.getElementById('review-travelers');
    const destinationEl = document.getElementById('review-destination');
    const durationEl    = document.getElementById('review-duration');
    const dateEl        = document.getElementById('review-date');
    if (!travelersEl || !destinationEl || !durationEl || !dateEl) return;

    const travelerType   = document.querySelector('input[name="traveler_type"]:checked')?.value || '';
    const travelersCount = document.querySelector('input[name="travelers"]')?.value || '';
    const destination    = document.querySelector('input[name="destination"]:checked')?.value || '';
    const duration       = document.querySelector('input[name="duration"]:checked')?.value || '';
    const travelDate     = document.querySelector('input[name="travel_date"]')?.value || '';

    let travelerLabel = 'Not selected';
    if (travelerType) {
        travelerLabel = travelersCount
            ? `${travelerType} • ${travelersCount} traveler${Number(travelersCount) > 1 ? 's' : ''}`
            : travelerType;
    }

    travelersEl.textContent   = travelerLabel;
    destinationEl.textContent = destination || 'Not selected';
    durationEl.textContent    = duration ? `${duration} Days` : 'Not selected';
    dateEl.textContent        = travelDate
        ? new Date(travelDate).toLocaleDateString('en-US', { day:'numeric', month:'long', year:'numeric' })
        : 'Not selected';
}


// ==========================================
// Step 6: City Planning — helpers + fetch
// ==========================================

function getDurationMaxDays() {
    const checked = document.querySelector('input[name="duration"]:checked');
    const val = checked ? parseInt(checked.value, 10) : 5;
    return isNaN(val) ? 5 : val;
}

/**
 * FIX: Instead of replacing selectDiv.innerHTML (which destroys the chevron
 * and all event listeners), we manage a separate tags-container <div> INSIDE
 * the selectDiv, and only update that child. The chevron <i> stays untouched.
 *
 * Structure rendered once in generateDayPlanningFields:
 *   <div class="city-multi-select">
 *     <div class="city-tags-container">   ← we only touch this
 *       <span class="selected-city-tag">…</span>
 *       <span class="text-muted placeholder-text">…</span>
 *     </div>
 *     <i class="bi bi-chevron-down daily-select-chevron"></i>  ← never touched
 *   </div>
 */
function updateSelectUI(tagsContainer, selectedCities, hiddenInput) {
    tagsContainer.innerHTML = '';

    if (selectedCities.length === 0) {
        const placeholder = document.createElement('span');
        placeholder.className = 'text-muted placeholder-text';
        placeholder.textContent = 'Choose itinerary points...';
        tagsContainer.appendChild(placeholder);
    } else {
        selectedCities.forEach(city => {
            const tag = document.createElement('span');
            tag.className = 'selected-city-tag';
            tag.dataset.city = city;
            tag.innerHTML = `${city}<button type="button" class="city-tag-remove" title="Remove ${city}">&times;</button>`;

            // Remove on × click
            tag.querySelector('.city-tag-remove').addEventListener('click', (e) => {
                e.stopPropagation();
                const idx = selectedCities.indexOf(city);
                if (idx > -1) selectedCities.splice(idx, 1);

                // Deselect the matching dropdown option
                const card = tagsContainer.closest('.day-plan-card');
                if (card) {
                    const opt = card.querySelector(`.city-option[data-city="${city}"]`);
                    if (opt) opt.classList.remove('selected');
                }
                updateSelectUI(tagsContainer, selectedCities, hiddenInput);
            });

            tagsContainer.appendChild(tag);
        });
    }

    // Always keep hidden input in sync — this is what gets submitted
    if (hiddenInput) hiddenInput.value = selectedCities.join(',');
}


async function generateDayPlanningFields() {
    const container = document.getElementById('city-planning-container');
    if (!container) return;

    const maxDays  = getDurationMaxDays();
    const checkedDest = document.querySelector('input[name="destination"]:checked');
    const destTitle   = checkedDest ? checkedDest.value : '';
    const destSlug    = checkedDest ? checkedDest.dataset.slug : '';

    // Loading state
    container.innerHTML = `
        <div class="text-center py-5 text-muted">
            <div class="spinner-border spinner-border-sm me-2" role="status"></div>
            Loading itinerary options...
        </div>`;

    // Fetch itineraries from backend
    let itineraries = [];
    if (destSlug) {
        try {
            const res  = await fetch(`/api/destination-itineraries/?slug=${encodeURIComponent(destSlug)}`);
            const json = await res.json();
            itineraries = json.itineraries || [];
        } catch (err) {
            console.error('Failed to load itineraries:', err);
        }
    }

    container.innerHTML = '';

    const dayLabels = [
        'ARRIVAL & DISCOVERY', 'EXPLORATION', 'CULTURE & HERITAGE',
        'LEISURE DAY', 'ADVENTURE', 'LOCAL IMMERSION', 'COASTAL RETREAT',
        'MOUNTAIN ESCAPE', 'FREE EXPLORATION', 'DEPARTURE DAY',
        'EXTENDED STAY', 'GRAND FINALE'
    ];

    for (let i = 1; i <= maxDays; i++) {
        const col    = document.createElement('div');
        col.className = 'daily-plan-col';
        const dayTag = dayLabels[i - 1] || `DAY ${i} PLAN`;

        const optionsHTML = itineraries.length
            ? itineraries.map(it =>
                `<div class="city-option" data-city="${it.title}" title="${it.description || ''}">${it.title}</div>`
              ).join('')
            : `<div class="city-option disabled text-muted" style="pointer-events:none;">No itinerary points found</div>`;

        // NOTE: city-multi-select now has two children:
        //   1. .city-tags-container  — managed by updateSelectUI
        //   2. .daily-select-chevron — never touched
        col.innerHTML = `
            <div class="day-plan-card daily-day-card">
                <div class="daily-card-left">
                    <span class="daily-day-tag">${dayTag}</span>
                    <h4 class="daily-day-number">Day ${String(i).padStart(2, '0')}</h4>
                    <p class="daily-day-dest mb-0">
                        <i class="bi bi-geo-alt-fill me-1"></i>${destTitle || 'Select Destination'}
                    </p>
                </div>
                <div class="daily-card-right">
                    <label class="daily-select-label">Select Itinerary Points</label>
                    <div class="city-multi-select" id="day-${i}-select" role="button" tabindex="0">
                        <div class="city-tags-container">
                            <span class="text-muted placeholder-text">Choose itinerary points...</span>
                        </div>
                        <i class="bi bi-chevron-down daily-select-chevron"></i>
                    </div>
                    <div class="city-dropdown-menu" id="day-${i}-menu">
                        ${optionsHTML}
                    </div>
                    <input type="hidden" name="day_${i}_cities" id="day-${i}-input">
                </div>
            </div>
        `;
        container.appendChild(col);

        const selectDiv    = col.querySelector('.city-multi-select');
        const tagsContainer = col.querySelector('.city-tags-container');  // ← target for updates
        const menuDiv      = col.querySelector('.city-dropdown-menu');
        const hiddenInput  = col.querySelector('input[type="hidden"]');
        const selectedCities = [];  // mutable array — passed by reference into closures

        // Toggle dropdown open/close
        selectDiv.addEventListener('click', (e) => {
            e.stopPropagation();
            document.querySelectorAll('.city-dropdown-menu').forEach(m => {
                if (m !== menuDiv) m.classList.remove('active');
            });
            menuDiv.classList.toggle('active');
        });

        // City option click — add/remove from selection
        menuDiv.querySelectorAll('.city-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const city = option.dataset.city;
                if (!city) return;

                if (selectedCities.includes(city)) {
                    selectedCities.splice(selectedCities.indexOf(city), 1);
                    option.classList.remove('selected');
                } else {
                    selectedCities.push(city);
                    option.classList.add('selected');
                }

                // Pass tagsContainer (not selectDiv) — safe, no chevron destruction
                updateSelectUI(tagsContainer, selectedCities, hiddenInput);
            });
        });
    }
}

// Close all dropdowns when clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.city-dropdown-menu').forEach(m => m.classList.remove('active'));
});


// ==========================================
// Step 7: Build Itinerary CTA Button
// ==========================================
const buildItineraryBtn = document.querySelector('.build-itinerary-btn');
if (buildItineraryBtn) {
    buildItineraryBtn.addEventListener('click', () => {
        currentStepIdx = 8;
        updateStep();
    });
}




// ==========================================
// Step 8: Form Submit → Save to backend + Generate Itinerary Output (Step 9)
// ==========================================
const tripForm = document.getElementById('customize-trip-form');
if (tripForm) {
    tripForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(tripForm);
        const data     = Object.fromEntries(formData.entries());
        const output   = document.getElementById('itinerary-output');
        if (!output) return;

        const dayCards  = document.querySelectorAll('.day-plan-card');
        const totalDays = dayCards.length;

        // ── POST to Django to save the lead ──
        const payload = {
            traveler_type     : data.traveler_type || '',
            travelers         : data.travelers || '1',
            destination       : data.destination || '',
            duration_days     : totalDays,
            departure_airport : document.querySelector('.airport-item.selected')?.dataset?.value || '',
            travel_date       : data.travel_date || '',
            first_name        : data.first_name || '',
            last_name         : data.last_name || '',
            email             : data.email || '',
            phone             : data.phone || '',
            notes             : data.notes || '',
        };

        // Add each day's selected itinerary points
        dayCards.forEach((card, idx) => {
            const i = idx + 1;
            const hiddenInput = document.getElementById(`day-${i}-input`);
            payload[`day_${i}_cities`] = hiddenInput ? hiddenInput.value : '';
        });

        try {
            await fetch('/api/submit-trip/', {
                method  : 'POST',
                headers : { 'Content-Type': 'application/json' },
                body    : JSON.stringify(payload),
            });
        } catch (err) {
            console.error('Failed to save inquiry:', err);
        }

        // ── Build the itinerary display (unchanged logic) ──
        let dayItineraryHTML = '';
        dayCards.forEach((card, idx) => {
            const i = idx + 1;
            const hiddenInput = document.getElementById(`day-${i}-input`);
            const citiesRaw   = hiddenInput ? hiddenInput.value : '';
            const cityList    = citiesRaw ? citiesRaw.split(',').map(c => c.trim()).filter(Boolean) : [];

            dayItineraryHTML += `
                <div class="itin-day-card">
                    <div class="itin-day-header">
                        <span class="itin-day-badge">Day ${i}</span>
                    </div>
                    <ul class="itin-city-list">
                        ${cityList.length
                            ? cityList.map(c => `<li><i class="bi bi-geo-alt-fill"></i>${c}</li>`).join('')
                            : '<li class="no-city"><i class="bi bi-dash"></i>No itinerary points planned</li>'
                        }
                    </ul>
                </div>`;
        });

        const rawDate       = data.travel_date || '';
        const formattedDate = rawDate
            ? new Date(rawDate).toLocaleDateString('en-US', { day:'numeric', month:'long', year:'numeric' })
            : '—';
        const travelerCount  = data.travelers || '1';
        const travelerType   = data.traveler_type || '';
        const travelersLabel = travelerType ? `${travelerCount} (${travelerType})` : travelerCount;
        const departure      = document.querySelector('.airport-item.selected')?.dataset?.value || '—';
        const destination    = data.destination || 'Not Selected';
        const durationLabel  = `${totalDays} Days`;

        output.innerHTML = `
            <div class="itin-document mx-auto">
                <div class="itin-header">
                    <div class="itin-logo-line">
                        <img src="{% static 'images/Group_1.png' %}" alt="Govolo Tours" class="itin-logo">
                        <span class="itin-tag">Travel Itinerary</span>
                    </div>
                    <h1 class="itin-destination-name">${destination}</h1>
                    <div class="itin-meta-pills">
                        <span><i class="bi bi-calendar3"></i> ${formattedDate}</span>
                        <span><i class="bi bi-clock"></i> ${durationLabel}</span>
                        <span><i class="bi bi-people"></i> ${travelersLabel}</span>
                    </div>
                </div>

                <div class="itin-divider-dashed"></div>

                <div class="itin-overview-card">
                    <div class="itin-from-to">
                        <div class="itin-from-col">
                            <span class="itin-label">FROM</span>
                            <span class="itin-value">${departure}</span>
                        </div>
                        <div class="itin-plane-icon"><i class="bi bi-airplane-fill"></i></div>
                        <div class="itin-to-col">
                            <span class="itin-label">TO</span>
                            <span class="itin-value">${destination}</span>
                        </div>
                    </div>
                    <div class="itin-overview-details">
                        <div>
                            <span class="itin-label">TRAVELER</span>
                            <span class="itin-value">${data.first_name || ''} ${data.last_name || ''}</span>
                        </div>
                        <div>
                            <span class="itin-label">DATE</span>
                            <span class="itin-value">${formattedDate}</span>
                        </div>
                        <div>
                            <span class="itin-label">DURATION</span>
                            <span class="itin-value">${durationLabel}</span>
                        </div>
                    </div>
                </div>

                <div class="itin-section">
                    <h3 class="itin-section-title"><i class="bi bi-map"></i> Day-by-Day Plan</h3>
                    <div class="itin-days-grid">${dayItineraryHTML}</div>
                </div>

                <div class="itin-section">
                    <h3 class="itin-section-title"><i class="bi bi-person-circle"></i> Traveler Details</h3>
                    <div class="itin-traveler-details">
                        <div class="itin-detail-row">
                            <span class="itin-label">Name</span>
                            <span class="itin-value">${data.first_name || ''} ${data.last_name || ''}</span>
                        </div>
                        <div class="itin-detail-row">
                            <span class="itin-label">Email</span>
                            <span class="itin-value">${data.email || '—'}</span>
                        </div>
                        <div class="itin-detail-row">
                            <span class="itin-label">Phone</span>
                            <span class="itin-value">${data.phone || '—'}</span>
                        </div>
                    </div>
                </div>

                <div class="itin-footer">
                    <p class="itin-footer-note">
                        Our travel experts will be in touch within 24 hours to confirm your itinerary.
                    </p>
                </div>
            </div>`;

        currentStepIdx = 9;
        updateStep();
    });
}



                        // <button type="button" class="btn itin-download-btn">
                        //     <i class="bi bi-download me-2"></i>Download PDF
                        // </button>
});
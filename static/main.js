let currentTab = 'total';

// 🍺 Add Beers
async function addBeer(user, amount) {
  const res = await fetch('/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: user, count: amount })
  });

  if (res.ok) {
    const data = await res.json();
    const userCard = document.querySelector(`[data-user="${user}"]`);
    const countEl = userCard.querySelector('.beer-count');
    countEl.textContent = data.new_total;

    addToToastFeed(user, amount);

    if (amount === 5) showWoman();

    updateLeaderboard();
    updateTotalBeers();
  }
}

// 🍻 Toast Feed
let toastFeed = [];

function addToToastFeed(name, count) {
  const now = new Date();
  const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const date = now.toLocaleDateString();

  const last = toastFeed[toastFeed.length - 1];
  if (last && last.name === name && (now - last.timestamp < 10000)) {
    last.count += count;
    last.timestamp = now;
  } else {
    toastFeed.push({
      name,
      count,
      timestamp: now,
      time,
      date
    });

    if (toastFeed.length > 10) {
      toastFeed.shift();
    }
  }

  renderToastFeed();
}

function renderToastFeed() {
  const list = document.getElementById('toast-list');
  if (!list) return;

  list.innerHTML = '';
  toastFeed.slice().reverse().forEach(toast => {
    const li = document.createElement('li');
    li.innerHTML = `${toast.name} has logged <strong>${toast.count}</strong> beers<br><span class="toast-time">${toast.date} @ ${toast.time}</span>`;
    list.appendChild(li);
  });
}

// 🏆 Leaderboard
function updateLeaderboard() {
  const leaderboard = [];

  document.querySelectorAll('.user-card').forEach(card => {
    const name = card.getAttribute('data-user');
    const beers = parseInt(card.querySelector('.beer-count').textContent);
    leaderboard.push({ name, beers });
  });

  leaderboard.sort((a, b) => {
    if (b.beers !== a.beers) return b.beers - a.beers;
    return a.name.localeCompare(b.name);
  });

  const container = document.getElementById('leaderboard-container');
  container.innerHTML = '';

  const maxBeers = leaderboard[0]?.beers || 1;

  leaderboard.forEach((user, i) => {
    const row = document.createElement('div');
    row.className = 'leaderboard-row';

    const xpBarWidth = Math.round((user.beers / maxBeers) * 100);
    const title = getTitle(i, user.beers);

    row.innerHTML = `
      <div class="left">
        <div class="name">${user.name}</div>
        <span class="title-tag">${title}</span>
        <div class="count">${user.beers} 🍺</div>
        <div class="bar-wrapper"><div class="bar" style="width: ${xpBarWidth}%"></div></div>
      </div>
      <div class="buttons">
        <button onclick="addBeer('${user.name}', 1)">+1</button>
        <button onclick="addBeer('${user.name}', 5)">+5</button>
      </div>
    `;

    container.appendChild(row);
  });
}

function getTitle(rank, beers) {
  if (beers === 0) return "Virgin";
  if (rank === 0) return "Alcoholic in Chief";
  if (rank === 1) return "Deputy Degenerate";
  if (rank === 2) return "Brewskeeter";
  if (rank === 3) return "Pilsner Prodigy";
  if (rank === 4) return "Certified Sipper";
  return "Weekend Warrior";
}

// 📊 Update Progress Bar
function updateTotalBeers() {
  let total = 0;
  document.querySelectorAll('.beer-count').forEach(el => {
    total += parseInt(el.textContent);
  });

  const totalLabel = document.getElementById('total-beers');
  const barFill = document.getElementById('progress-bar-fill');
  const progressLabel = document.getElementById('progress-label');

  if (totalLabel) totalLabel.textContent = total;

  const percent = (total / 1000000) * 100;
  if (barFill) barFill.style.width = `${percent}%`;
  if (progressLabel) {
    progressLabel.textContent = `${total.toLocaleString()} / 1,000,000 Beers (${percent.toFixed(2)}%)`;
  }
}

// 💃 Woman animation for +5
function showWoman() {
  const woman = document.getElementById('woman-container');
  woman.innerText = '💃🍺🍺🍺🍺🍺';
  woman.classList.add('show');
  const audio = new Audio('https://www.myinstants.com/media/sounds/alcoholic.mp3');
  audio.play();
  setTimeout(() => {
    woman.classList.remove('show');
  }, 1500);
}

// 🔐 Admin Panel Toggle (Ctrl + `)
window.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === '`') {
    const panel = document.getElementById('admin-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
  }
});

// 🔐 Submit custom beer change
async function submitBeerAdjustment() {
  const name = document.getElementById('admin-name').value.trim();
  const amount = parseInt(document.getElementById('admin-amount').value);

  if (!name || isNaN(amount)) {
    alert("Please enter both a name and number.");
    return;
  }

  const res = await fetch('/admin/adjust', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: name, count: amount })
  });

  if (res.ok) {
    alert(`Successfully adjusted ${name} by ${amount} beers!`);
    location.reload();
  } else {
    alert("Failed to apply change.");
  }
}

// 👑 Submit Alcoholic of the Week update
async function submitAOTW() {
  const name = document.getElementById('aotw-name-input').value.trim();
  const image = document.getElementById('aotw-image-input').value.trim();
  const message = document.getElementById('aotw-message-input').value.trim();

  if (!name || !image || !message) {
    alert("Please fill in all AOTW fields.");
    return;
  }

  const res = await fetch('/admin/set_aotw', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, image, message })
  });

  if (res.ok) {
    alert("Alcoholic of the Week updated!");
    location.reload();
  } else {
    alert("Failed to update AOTW.");
  }
}

// 🏁 Initialize
window.onload = () => {
  updateLeaderboard();
  updateTotalBeers();
};
